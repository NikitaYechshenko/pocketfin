from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, Literal
from decimal import Decimal


class AssetBase(BaseModel):
    """Base schema for Asset."""
    symbol: str = Field(..., min_length=1, max_length=10, description="Asset symbol, e.g. BTC")
    amount: Decimal = Field(..., gt=0, description="Amount of the asset")
    operation_type: Literal["buy", "sell"] = Field(..., description="Operation type: 'buy' or 'sell'")


class AssetCreate(AssetBase):
    """Schema for creating a new asset."""
    portfolio_id: int = Field(..., description="ID of the portfolio to add the asset to")
    operation_time: Optional[date] = Field(None, description="Date of the operation")


class AssetUpdate(BaseModel):
    """Schema for updating an existing asset."""
    symbol: Optional[str] = Field(None, min_length=1, max_length=10, description="Asset symbol")
    amount: Optional[Decimal] = Field(None, gt=0, description="Amount of the asset")
    operation_type: Optional[Literal["buy", "sell"]] = Field(None, description="Operation type")


class AssetRead(AssetBase):
    """Schema returned from the API for an asset."""
    id: int = Field(..., description="Asset ID")
    portfolio_id: int = Field(..., description="Portfolio ID")
    user_id: int = Field(..., description="Owner user ID")
    operation_time: Optional[date] = Field(None, description="Date/time of the operation")

    model_config = ConfigDict(from_attributes=True)






