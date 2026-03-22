from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Transaction(Base):
    """
    Transaction in a portfolio.

    Represents a buy or sell operation for a specific asset (stock, crypto, etc.)
    Each transaction is linked to a portfolio and tracks:
    - Symbol (ticker)
    - Amount (quantity)
    - Price per unit
    - Operation type (buy/sell)
    - Operation date
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)

    # Asset information
    symbol = Column(String(10), nullable=False, comment="Asset symbol/ticker (e.g., BTC, AAPL)")
    amount = Column(Numeric(precision=18, scale=8), nullable=False, comment="Quantity of the asset")
    price = Column(Numeric(precision=18, scale=8), nullable=False, comment="Price per unit at operation time")

    # Operation details
    operation_type = Column(
        String(10),
        nullable=False,
        comment="Type of operation: 'buy' or 'sell'"
    )
    operation_time = Column(Date, nullable=True, comment="Date of the operation")

    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")

    # Table-level constraints
    __table_args__ = (
        CheckConstraint(
            "operation_type IN ('buy', 'sell')",
            name="check_operation_type"
        ),
        CheckConstraint(
            "amount > 0",
            name="check_amount_positive"
        ),
        CheckConstraint(
            "price > 0",
            name="check_price_positive"
        ),
    )







