from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

from app.modules.asset.schemas import AssetRead


class PortfolioBase(BaseModel):
    """Base schema for Portfolio."""
    name: str = Field(..., min_length=1, max_length=50, description="Portfolio name")


class PortfolioCreate(PortfolioBase):
    """Schema for creating a new portfolio."""
    pass


class PortfolioUpdate(BaseModel):
    """Schema for updating a portfolio."""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Portfolio name")


class PortfolioRead(PortfolioBase):
    """Schema for reading portfolio data."""
    id: int = Field(..., description="Portfolio ID")
    user_id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class PortfolioWithAssetsRead(PortfolioRead):
    """Schema for reading portfolio data with associated assets."""
    assets: list[AssetRead] = Field(default_factory=list, description="List of assets in the portfolio")




