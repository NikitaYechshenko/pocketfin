from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship
# Inherit from Base (ours) and SQLAlchemyBaseUserTable (from fastapi-users library)
class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # back_populates links this model to the field in Portfolio model
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan") 
    assets = relationship("Asset", back_populates="user")
    # email, hashed_password, is_active, is_superuser, is_verified
    # are already defined in SQLAlchemyBaseUserTable, no need to add them!
    
    # You can add custom fields if needed, for example:
    # phone = Column(String, nullable=True)
