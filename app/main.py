import logging
from fastapi import FastAPI
from app.core.database import check_database_connection
from app.core.health import start_health_check
from app.modules.users.router import router as users_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Asset Tracker")


@app.on_event("startup")
async def startup_event():
    """Проверка БД при запуске приложения"""
    logger.info("🚀 Запуск Asset Tracker...")
    if check_database_connection():
        logger.info("✓ Приложение готово к работе")
        start_health_check(interval=120)  # 2 минуты
    else:
        logger.error("✗ Не удалось подключиться к БД. Проверьте .env")
        raise RuntimeError("Database connection failed on startup")


@app.on_event("shutdown")
async def shutdown_event():
    """Логирование при выключении"""
    logger.info("🛑 Asset Tracker остановлен")


# Регистрация роутеров
app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/health")
async def health_check():
    """Endpoint для проверки здоровья приложения"""
    from app.core.database import check_database_connection
    is_connected = check_database_connection()
    return {
        "status": "ok" if is_connected else "error",
        "database": "connected" if is_connected else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

