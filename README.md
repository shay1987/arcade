# Arcade

![Arcade Logo](logo.png)

Arcade is a browser-accessible collection of classic TUI games served over the web via [ttyd](https://github.com/tsl0922/ttyd).
It includes a full authentication layer (register, login, forgot password, admin console) backed by MySQL, and can be run via Docker Compose, plain Kubernetes manifests, or a Helm chart.

---

## Architecture

```
Browser
  │
  ├── /          → Login App (FastAPI + MySQL)
  └── /arcade/   → Arcade terminal (ttyd)
```

Three containers sit behind a single Nginx reverse proxy (Docker Compose) or nginx Ingress (Kubernetes):

| Container | Image | Purpose |
|-----------|-------|---------|
| `login` | `shay1987/login` | FastAPI auth app — register, login, forgot password, admin console |
| `arcade` | `shay1987/arcade` | ttyd serving the bash game menu |
| `mysql` | `mysql:8.0` | User accounts and admin credentials |

---

## Games Included

| # | Game | Description |
|---|------|-------------|
| 1 | Bastet | Tetris with the worst pieces |
| 2 | Ninvaders | Space Invaders clone |
| 3 | Nsnake | Classic snake |
| 4 | Greed | Eat numbers, don't get trapped |
| 5 | Pacman4console | Pac-Man in the terminal |
| 6 | Nethack | Roguelike dungeon crawler |
| 7 | Moon-buggy | Drive and jump over craters |
| 8 | Nudoku | Sudoku puzzle |
| 9 | Tennis | Two-player bash tennis game |

---

## Configuration

Copy `.env.sample` to `.env` and adjust before starting:

```bash
cp .env.sample .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_ROOT_PASSWORD` | `admin` | MySQL root password |
| `SECRET_KEY` | `change-this-in-production` | Flask session signing key |
| `NGINX_PORT` | `80` | Host port exposed by Nginx |
| `ADMIN_USER` | `admin` | Seed admin username |
| `ADMIN_PASSWORD` | `admin` | Seed admin password |

---

## Run with Docker Compose

```bash
cp .env.sample .env          # configure ports and passwords
docker compose up --build -d
```

| URL | Service |
|-----|---------|
| `http://localhost/` | Login page |
| `http://localhost/arcade/` | Arcade terminal |

Stop everything:
```bash
docker compose down
```

---

## Deploy to Kubernetes (kubectl)

### Prerequisites
- `kubectl` connected to a cluster
- Nginx Ingress controller (`minikube addons enable ingress` for Minikube)

### Apply manifests

```bash
kubectl apply -f secret.yaml
kubectl apply -f mysql.yaml
kubectl apply -f login.yaml
kubectl apply -f arcade_game/deployment.yaml
kubectl apply -f ingress.yaml
```

### Access (Minikube)

```bash
minikube ip   # e.g. 192.168.49.2
```

Open `http://<MINIKUBE_IP>/` in your browser.

### Tear down

```bash
kubectl delete -f secret.yaml -f mysql.yaml -f login.yaml \
               -f arcade_game/deployment.yaml -f ingress.yaml
```

---

## Deploy to Kubernetes (Helm)

### Install

```bash
helm install arcade helm-chart/arcade
```

### Upgrade after changes

```bash
helm upgrade arcade helm-chart/arcade
```

### Override values

```bash
helm install arcade helm-chart/arcade \
  --set mysql.rootPassword=mysecret \
  --set loginApp.secretKey=mysessionkey \
  --set ingress.className=nginx
```

### Verify

```bash
kubectl get pods
kubectl get ingress
```

### Uninstall

```bash
helm uninstall arcade
```

---

## Admin Console

An admin account is seeded automatically on first startup using `ADMIN_USER` / `ADMIN_PASSWORD` from the environment.

To access the admin console, click the small **Admin** link at the bottom of the login page, or navigate directly to `/admin`.

From the console you can:
- Change any user's password
- Change the admin password (no restart needed)

---

## CI/CD

GitHub Actions (`.github/workflows/docker-image.yml`) builds and pushes both Docker images on every push:

| Branch | Tags pushed |
|--------|------------|
| `dev` | `shay1987/arcade:<version>`, `shay1987/login:<version>` |
| `master` | `shay1987/arcade:latest` + version, `shay1987/login:latest` + version |

Required GitHub secrets: `DOCKER_USER`, `DOCKER_PASSWORD`.

---

## Contributing

Pull requests are welcome. To add a game:
1. Add the package install to `Dockerfile`
2. Add the menu entry and case handler to `run.sh`
3. Rebuild and test

## License

MIT License.
