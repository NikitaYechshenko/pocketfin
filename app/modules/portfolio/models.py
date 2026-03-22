from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Portfolio(Base):
    """User's crypto portfolio."""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # back_populates links this model to the field in User model
    user = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")
