import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.users.schemas import UserRead, UserCreate, UserUpdate
from app.modules.users.manager import auth_backend, fastapi_users

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Жизненный цикл (замена on_event startup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Тут можно добавить проверку БД при старте
    logger.info("🚀 Starting Asset Tracker (Async)...")
    yield
    logger.info("🛑 Asset Tracker stopped")

app = FastAPI(title="Asset Tracker", lifespan=lifespan)

# CORS (Обязательно для фронтенда!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В проде укажите конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ПОДКЛЮЧЕНИЕ РОУТЕРОВ FastAPI Users ===

# 1. Login / Logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# 2. Регистрация
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# 3. Управление пользователями (получить текущего, обновить профиль и т.д.)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "mode": "async"}