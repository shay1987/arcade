from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from mysql.connector.errors import DatabaseError
import bcrypt
import mysql.connector
import os

ARCADE_URL = os.getenv("ARCADE_URL",       "/arcade/")
ADMIN_USER = os.getenv("ADMIN_USER",        "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD",    "admin")

DB = {
    "host":     os.getenv("MYSQL_HOST",     "mysql"),
    "port":     int(os.getenv("MYSQL_PORT", "3306")),
    "user":     os.getenv("MYSQL_USER",     "root"),
    "password": os.getenv("MYSQL_PASSWORD", "admin"),
    "database": os.getenv("MYSQL_DATABASE", "mydb"),
}

SECURITY_QUESTIONS = [
    "What was the name of your first pet?",
    "What city were you born in?",
    "What is your mother's maiden name?",
    "What was the name of your first school?",
    "What is your favorite childhood movie?",
]


def get_db():
    return mysql.connector.connect(**DB)


def _seed_admin():
    """Insert the admin user from env vars if no admin exists yet."""
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT username FROM admins LIMIT 1")
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO admins (username, password) VALUES (%s, %s)",
                (ADMIN_USER, bcrypt.hashpw(ADMIN_PASS.encode(), bcrypt.gensalt()).decode()),
            )
            conn.commit()
        cur.close()
        conn.close()
    except Exception:
        pass  # MySQL may not be ready yet; will seed on first admin login


@asynccontextmanager
async def lifespan(app):
    _seed_admin()
    yield


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "change-this-secret"))
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _login_page(request, msg="", success=False):
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg, "success": success})


def _admin_page(request, users, total, msg="", success=False):
    return templates.TemplateResponse("admin.html", {
        "request": request, "users": users, "total": total, "msg": msg, "success": success
    })


@app.exception_handler(DatabaseError)
async def db_error(request: Request, exc: DatabaseError):
    return _login_page(request, "Database unavailable — please try again shortly.")


# --- Login ---

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return _login_page(request)


@app.post("/", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT password FROM accounts WHERE username = %s", (username,))
    row = cur.fetchone()

    if row and bcrypt.checkpw(password.encode(), row["password"].encode()):
        cur.execute("UPDATE accounts SET last_login = NOW() WHERE username = %s", (username,))
        conn.commit()
        cur.close()
        conn.close()
        request.session["user"] = username
        return RedirectResponse("/home", status_code=303)

    cur.close()
    conn.close()
    return _login_page(request, "Incorrect username or password.")


@app.get("/home")
async def home(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/")
    return RedirectResponse(ARCADE_URL)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


# --- Register ---

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {
        "request": request, "msg": "", "questions": SECURITY_QUESTIONS
    })


@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    security_question: str = Form(...),
    security_answer: str = Form(...),
):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT username FROM accounts WHERE username = %s", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return templates.TemplateResponse("register.html", {
            "request": request, "msg": "Username already taken.", "questions": SECURITY_QUESTIONS
        })

    cur.execute(
        "INSERT INTO accounts (username, full_name, password, security_question, security_answer) "
        "VALUES (%s, %s, %s, %s, %s)",
        (username, full_name, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
         security_question, security_answer.strip().lower()),
    )
    conn.commit()
    cur.close()
    conn.close()
    return _login_page(request, "Account created! Please log in.", success=True)


# --- Forgot password (3-step) ---

@app.get("/forgot", response_class=HTMLResponse)
async def forgot_page(request: Request):
    return templates.TemplateResponse("forgot.html", {
        "request": request, "step": 1, "msg": "", "question": None, "username": None
    })


@app.post("/forgot", response_class=HTMLResponse)
async def forgot_lookup(request: Request, username: str = Form(...)):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT security_question FROM accounts WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return templates.TemplateResponse("forgot.html", {
            "request": request, "step": 1, "msg": "Username not found.", "question": None, "username": None
        })
    return templates.TemplateResponse("forgot.html", {
        "request": request, "step": 2, "msg": "", "question": row["security_question"], "username": username
    })


@app.post("/forgot/verify", response_class=HTMLResponse)
async def forgot_verify(request: Request, username: str = Form(...), answer: str = Form(...)):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT security_question, security_answer FROM accounts WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row or row["security_answer"] != answer.strip().lower():
        return templates.TemplateResponse("forgot.html", {
            "request": request, "step": 2, "msg": "Incorrect answer. Try again.",
            "question": row["security_question"] if row else None, "username": username
        })
    request.session["reset_user"] = username
    return templates.TemplateResponse("forgot.html", {
        "request": request, "step": 3, "msg": "", "question": None, "username": username
    })


@app.post("/forgot/reset", response_class=HTMLResponse)
async def forgot_reset(request: Request, new_password: str = Form(...)):
    username = request.session.pop("reset_user", None)
    if not username:
        return RedirectResponse("/forgot")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE accounts SET password = %s WHERE username = %s",
        (bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode(), username),
    )
    conn.commit()
    cur.close()
    conn.close()
    return _login_page(request, "Password updated! Please log in.", success=True)


# --- Admin ---

def _get_users():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT username, full_name, last_login FROM accounts ORDER BY last_login DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "msg": ""})


@app.post("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    _seed_admin()  # seed if startup seeding failed (MySQL was slow)
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT password FROM admins WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row["password"].encode()):
        request.session["admin"] = username
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse("admin_login.html", {"request": request, "msg": "Invalid credentials."})


@app.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.pop("admin", None)
    return RedirectResponse("/admin/login")


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login")
    users = _get_users()
    return _admin_page(request, users, len(users))


@app.post("/admin/change-password", response_class=HTMLResponse)
async def admin_change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
):
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login")

    users = _get_users()
    admin_username = request.session["admin"]

    if new_password != confirm_password:
        return _admin_page(request, users, len(users), "New passwords do not match.")

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT password FROM admins WHERE username = %s", (admin_username,))
    row = cur.fetchone()

    if not row or not bcrypt.checkpw(current_password.encode(), row["password"].encode()):
        cur.close()
        conn.close()
        return _admin_page(request, users, len(users), "Current password is incorrect.")

    cur.execute(
        "UPDATE admins SET password = %s WHERE username = %s",
        (bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode(), admin_username),
    )
    conn.commit()
    cur.close()
    conn.close()
    return _admin_page(request, users, len(users), "Password changed successfully.", success=True)
