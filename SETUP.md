# 🚀 Global-Asset-Tracker: Setup Guide

This document describes how to set up and run the **Global-Asset-Tracker** project locally from scratch.

## 📋 Prerequisites

Ensure you have the following installed on your machine:
* **Docker & Docker Compose** (for the database)
* **Python 3.10+** (for the backend)
* **Node.js 18+** (for the frontend)
* **Git**

---

## 1️⃣ Database Setup (Docker)

We use Docker to run PostgreSQL in an isolated environment to avoid messing with your local system.

1.  **Start the container:**
    ```bash
    docker compose up -d
    ```

2.  **Verify it's running:**
    ```bash
    docker ps
    ```
    *You should see a container running. Note that the internal port `5432` is mapped to **`5433`** on your host machine.*

---

## 2️⃣ Backend Setup (FastAPI)

1.  **Navigate to the project root directory.**

2.  **Create and activate a virtual environment:**

    * **Windows:**
        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **Mac/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    * Create a `.env` file in the root directory.
    * Copy the content from `.env.example` into it.
    * Ensure the `DATABASE_URL` matches the Docker port (5433):
    ```ini
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/gat_db
    SECRET_KEY=your_secure_random_key_here
    ```

5.  **Apply Database Migrations:**
    This command creates the necessary tables (Users, Portfolios, Assets) in the empty database.
    ```bash
    alembic upgrade head
    ```

6.  **Start the Backend Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    * **API URL:** `http://localhost:8000`
    * **Swagger Docs:** `http://localhost:8000/docs`

---

## 3️⃣ Frontend Setup (React)

1.  **Open a new terminal window** (leave the backend running).

2.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

3.  **Install dependencies:**
    ```bash
    npm install
    ```

4.  **Start the Development Server:**
    ```bash
    npm run dev
    ```
    * **App URL:** `http://localhost:3000`

---

## 🛠 Useful Commands & Troubleshooting

### Database Management
* **Stop Database:**
    ```bash
    docker compose down
    ```
* **Hard Reset (⚠ Delete all data):**
    If you need to completely wipe the database and start over:
    ```bash
    docker compose down -v
    docker compose up -d
    alembic upgrade head
    ```

### Migrations (Alembic)
* **Create a new migration:**
    If you modify `models.py`, run this to generate a migration file:
    ```bash
    alembic revision --autogenerate -m "description_of_changes"
    ```
* **Apply changes:**
    ```bash
    alembic upgrade head
    ```