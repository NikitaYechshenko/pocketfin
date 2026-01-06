from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

# 2. Создаем фабрику асинхронных сессий
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# 3. Асинхронная зависимость для получения сессии (Dependency)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session