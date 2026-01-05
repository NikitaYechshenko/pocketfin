import logging
from fastapi import FastAPI
from app.core.database import check_database_connection
from app.core.health import start_health_check
from app.modules.users.router import router as users_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Asset Tracker")

app.include_router(users_router)


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Asset Tracker...")
    if check_database_connection():
        logger.info("✓ Application is ready")
        start_health_check(interval=120)
    else:
        logger.error("✗ Failed to connect to database")
        raise RuntimeError("Database connection failed on startup")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Asset Tracker stopped")


@app.get("/health")
async def health_check():
    from app.core.database import check_database_connection
    is_connected = check_database_connection()
    return {
        "status": "ok" if is_connected else "error",
        "database": "connected" if is_connected else "disconnected"
    }

