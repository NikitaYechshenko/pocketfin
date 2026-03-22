import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password in a thread pool to avoid blocking the event loop."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, pwd_context.verify, plain_password, hashed_password)

async def get_password_hash(password: str) -> str:
    """Hash password in a thread pool to avoid blocking the event loop."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, pwd_context.hash, password)

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire}) 
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")



