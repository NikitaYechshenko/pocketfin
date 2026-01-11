# SETUP

Instructions for running the project locally (Backend + Frontend + PostgreSQL + pgAdmin).

---
## 0. Change .env.example to .env

---

## 1. Infrastructure startup (Docker)

Start PostgreSQL and pgAdmin in detached mode:

```bash
docker compose up -d
```

Verify that containers are running (**2 containers expected**):

```bash
docker ps
```

docker compose down -v # down

Expected result:

* PostgreSQL container
* pgAdmin container

---

## 2. Backend setup (Python)

### 2.1 Create a virtual environment

```bash
python -m venv venv
```

### 2.2 Activate the virtual environment (Windows)

```bash
.\\venv\\Scripts\\activate
```

### 2.3 Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Alembic (database migrations)

### 3.1 Create migrations directory (if missing)

Required to avoid `FileNotFoundError`.

```bash
mkdir alembic/versions
```

### 3.2 Generate initial migration

Alembic compares SQLAlchemy models with the current database schema and generates migration scripts.

```bash
alembic revision --autogenerate -m "Initial migration"
```

### 3.3 Apply migrations

Creates tables in PostgreSQL (inside the Docker container):

```bash
alembic upgrade head
```

---

## 4. Run Backend

```bash
uvicorn app.main:app --reload
```

Notes:

* `--reload` enables auto-restart on code changes
* Backend is available at `http://localhost:8000` by default

---

## 5. Run Frontend

In a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

Frontend is started via Vite. The address will be shown in the console (usually `http://localhost:5173`).

---

## 6. Environment variables

All sensitive variables are stored in:

```text
.env
```

⚠️ If you change:

* `POSTGRES_USER`
* `POSTGRES_PASSWORD`
* `POSTGRES_DB` (Maintenance DB)

You must **also update the same values** in:

```text
/servers.json
```

Otherwise, the database will **not be automatically added** to pgAdmin.

---

## 7. pgAdmin

pgAdmin access:

* URL: [http://localhost:8080](http://localhost:8080)
* Email: `admin@admin.com`
* Password: `admin`

The `servers.json` file is used to automatically register the PostgreSQL server in pgAdmin on first container startup.

---

## 7.1 Swagger UI (API documentation)

FastAPI automatically provides interactive API documentation via Swagger UI:

* URL: [http://localhost:8000/docs](http://localhost:8000/docs)

This interface allows you to:

* explore all available endpoints
* inspect request/response schemas
* send test requests directly from the browser

---

## 8. Docker shutdown and restart

### 8.1 Stop containers

To stop all running containers defined in `docker-compose.yml`:

```bash
docker compose down
```

This will:

* stop PostgreSQL and pgAdmin containers
* preserve database data if volumes are configured

---

### 8.2 Start containers again

To start the containers again in detached mode:

```bash
docker compose up -d
```

After restart:

* PostgreSQL will be available with existing data
* pgAdmin will keep registered servers (if volumes are used)

---

## 9. Architecture overv

* **Docker** — infrastructure (PostgreSQL + pgAdmin)
* **FastAPI + Uvicorn** — Backend
* **Alembic** — database migrations
* **Vite + npm** — Frontend

---

If issues occur, check:

* `.env`
* `docker-compose.yml`
* `alembic.ini`
* `servers.json`
