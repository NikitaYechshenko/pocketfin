from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    # for Telegram integration
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=True)
    telegram_username = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")