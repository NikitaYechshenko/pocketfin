from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserResponse

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 


    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    async def get_telegram_id_by_user_id(self, user_id: int) -> Optional[int]:
        """Get Telegram ID by user ID"""
        result = await self.session.execute(select(User.telegram_id).where(User.id == user_id))
        return result.scalar_one_or_none()

