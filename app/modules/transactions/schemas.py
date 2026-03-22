from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional, Literal
from decimal import Decimal


class TransactionBase(BaseModel):
    """Base schema for Transaction."""
    symbol: str = Field(..., min_length=1, max_length=10, description="Asset symbol, e.g. BTC, AAPL")
    amount: Decimal = Field(..., gt=0, description="Quantity of the asset")
    price: Decimal = Field(..., gt=0, description="Price per unit at operation time")
    operation_type: Literal["buy", "sell"] = Field(..., description="Operation type: 'buy' or 'sell'")


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    portfolio_id: int = Field(..., description="ID of the portfolio to add the transaction to")
    operation_time: Optional[date] = Field(None, description="Date of the operation")


class TransactionUpdate(BaseModel):
    """Schema for updating an existing transaction."""
    symbol: Optional[str] = Field(None, min_length=1, max_length=10, description="Transaction symbol")
    amount: Optional[Decimal] = Field(None, gt=0, description="Quantity of the transaction")
    price: Optional[Decimal] = Field(None, gt=0, description="Price per unit")
    operation_type: Optional[Literal["buy", "sell"]] = Field(None, description="Operation type")
    operation_time: Optional[date] = Field(None, description="Date of the operation")


class TransactionRead(TransactionBase):
    """Schema returned from the API for a transaction."""
    id: int = Field(..., description="Transaction ID")
    portfolio_id: int = Field(..., description="Portfolio ID")
    operation_time: Optional[date] = Field(None, description="Date of the operation")

    model_config = ConfigDict(from_attributes=True)







