from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric,Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Asset(Base):
    """Portfolios asset."""
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    #info about asset
    symbol = Column(String(10), nullable=False, unique=False)

    amount = Column(Numeric(precision=18, scale=15), nullable=False)

    operation_type = Column(String(10), nullable=False)  # buy or sell

    operation_time = Column(Date, nullable=True)
    # back_populates links this model to the field in User model
    portfolio = relationship("Portfolio", back_populates="assets")
    user = relationship("User", back_populates="assets")






