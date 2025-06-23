from flask import Flask, render_template, session, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import re, os

app = Flask(__name__)
app.secret_key = 'thisIsSecret'

# Environment variables for database connection
MYSQL_ROOT_USER = os.getenv('MYSQL_ROOT_USER', 'root')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'admin')
MYSQL_ROOT_HOST = os.getenv('MYSQL_ROOT_HOST', 'mysql-service.default.svc.cluster.local')
MYSQL_ROOT_PORT = os.getenv('MYSQL_ROOT_PORT', '3306')
MYSQL_ROOT_DB = os.getenv('MYSQL_ROOT_DB', 'mydb')
FLASK_APP_PORT = os.getenv('FLASK_APP_PORT', '5000')

# Configure SQLAlchemy for MySQL with PyMySQL driver
# Format: mysql+pymysql://user:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_ROOT_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_ROOT_HOST}:{MYSQL_ROOT_PORT}/{MYSQL_ROOT_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to disable to save memory

db = SQLAlchemy(app) # Initialize SQLAlchemy

# Define your database model (for the 'accounts' table)
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Account {self.username}>'

# --- Ensure database tables are created on app startup ---
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = 'Welcome!'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        try:
            account = Account.query.filter_by(username=username, password=password).first()

            if account:
                session['loggedin'] = True
                session['id'] = account.id
                session['username'] = account.username
                return redirect('/home')
            else:
                msg = 'Incorrect username/password!'
        except Exception as e:
            print(f"Database query error in login: {e}")
            msg = f"A database error occurred during login: {e}. Please check server logs."

    return render_template('index.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Welcome'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            existing_account_user = Account.query.filter_by(username=username).first()
            existing_account_email = Account.query.filter_by(email=email).first()

            if existing_account_user:
                msg = 'Account already exists!'
            elif existing_account_email:
                msg = 'Email already registered!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                new_account = Account(username=username, password=password, email=email)
                db.session.add(new_account)
                db.session.commit()
                msg = 'You have successfully registered!'
        except Exception as e:
            print(f"Database query error in register: {e}")
            msg = f"A database error occurred during registration: {e}. Please check server logs."

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/home')
def home():
    # Corrected for universal cluster access
    # This redirects to the '/arcade' path on the *same external hostname/IP* the user accessed the login app from.
    return redirect('/arcade')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=int(FLASK_APP_PORT))