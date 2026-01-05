import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users import router as user
from app.core.database import SessionLocal
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Глобальный обработчик ошибок БД
@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"❌ Ошибка БД: {exc}")
    return JSONResponse(
        status_code=503,
        content={"detail": "База данных недоступна. Попробуйте позже."}
    )

app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В проде здесь будет адрес твоего сайта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

