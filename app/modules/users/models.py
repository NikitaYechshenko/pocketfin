# from sqlalchemy import Column, Integer, String, Boolean, DateTime
# from sqlalchemy.sql import func
# from app.core.database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(100), unique=True, nullable=False, index=True)
#     hashed_password = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from app.core.database import Base

# Наследуемся от Base (наш) и SQLAlchemyBaseUserTable (от библиотеки)
class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # email, hashed_password, is_active, is_superuser, is_verified 
    # уже есть внутри SQLAlchemyBaseUserTable, писать их не нужно!
    
    # Можем добавить свои поля, если захотим, например:
    # phone = Column(String, nullable=True)