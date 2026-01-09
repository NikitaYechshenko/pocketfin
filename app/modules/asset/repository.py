from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.asset.models import Asset


class AssetRepository:
    """Repository for Asset data access - handles all DB operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, portfolio_id: int, symbol: str, amount, operation_type: str, operation_time=None) -> Asset:
        """Create a new asset in the database."""
        asset = Asset(
            user_id=user_id,
            portfolio_id=portfolio_id,
            symbol=symbol,
            amount=amount,
            operation_type=operation_type,
            operation_time=operation_time
        )
        self.session.add(asset)
        await self.session.flush()
        await self.session.refresh(asset)
        return asset

    async def get_by_id(self, asset_id: int) -> Asset | None:
        """Get asset by ID from database."""
        query = select(Asset).where(Asset.id == asset_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id_and_user(self, asset_id: int, user_id: int) -> Asset | None:
        """Get asset by ID with user ownership check."""
        query = select(Asset).where(
            Asset.id == asset_id,
            Asset.user_id == user_id,
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_portfolio(self, portfolio_id: int) -> list[Asset]:
        """Get all assets for a specific portfolio from database."""
        query = select(Asset).where(Asset.portfolio_id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_user(self, user_id: int) -> list[Asset]:
        """Get all assets for a specific user from database."""
        query = select(Asset).where(Asset.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, asset: Asset, **kwargs) -> Asset:
        """Update asset fields."""
        for key, value in kwargs.items():
            if hasattr(asset, key) and value is not None:
                setattr(asset, key, value)
        
        await self.session.flush()
        await self.session.refresh(asset)
        return asset

    async def delete(self, asset: Asset) -> None:
        """Delete an asset from database."""
        await self.session.delete(asset)
        await self.session.flush()
    
    

