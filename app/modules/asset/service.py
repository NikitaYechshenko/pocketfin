# Service layer for Asset operations.
#
# Same purpose as PortfolioService:
# - Access control (asset ownership checks),
# - Data conversion to Pydantic schemas for API,
# - Database operations delegated to AssetRepository.

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.asset.repository import AssetRepository
from app.modules.asset.schemas import AssetCreate, AssetRead, AssetUpdate


class AssetService:
    """Service for asset business logic - uses Repository for DB access."""

    def __init__(self, session: AsyncSession):
        self.repository = AssetRepository(session)

    async def create_asset(
        self, user_id: int, asset_data: AssetCreate
    ) -> AssetRead:
        """Create a new asset in the specified portfolio for the user.
        
        Note:
        - portfolio_id is taken from asset_data (AssetCreate schema).
        - Portfolio ownership check should be done at the router level
          (or add a check here via PortfolioRepository).
        """
        asset = await self.repository.create(
            user_id=user_id,
            portfolio_id=asset_data.portfolio_id,
            symbol=asset_data.symbol,
            amount=asset_data.amount,
            operation_type=asset_data.operation_type,
            operation_time=asset_data.operation_time
        )
        return AssetRead.model_validate(asset)

    async def get_user_assets(self, user_id: int) -> list[AssetRead]:
        """Return all assets for the user (from all their portfolios)."""
        assets = await self.repository.get_by_user(user_id)
        return [AssetRead.model_validate(a) for a in assets]

    async def get_portfolio_assets(self, portfolio_id: int) -> list[AssetRead]:
        """Return all assets for a specific portfolio.
        
        Note: Portfolio ownership check should be done at the router level.
        """
        assets = await self.repository.get_by_portfolio(portfolio_id)
        return [AssetRead.model_validate(a) for a in assets]

    async def get_asset_by_id(
        self, asset_id: int, user_id: int
    ) -> AssetRead | None:
        """Return an asset by ID only if it belongs to the user."""
        asset = await self.repository.get_by_id_and_user(asset_id, user_id)
        return AssetRead.model_validate(asset) if asset else None

    async def update_asset(
        self, asset_id: int, user_id: int, asset_data: AssetUpdate
    ) -> AssetRead | None:
        """Update an asset (partial update supported)."""
        asset = await self.repository.get_by_id_and_user(asset_id, user_id)
        
        if not asset:
            return None

        update_data = asset_data.model_dump(exclude_unset=True)
        asset = await self.repository.update(asset, **update_data)
        return AssetRead.model_validate(asset)

    async def delete_asset(self, asset_id: int, user_id: int) -> bool:
        """Delete an asset if it belongs to the user."""
        asset = await self.repository.get_by_id_and_user(asset_id, user_id)
        
        if not asset:
            return False

        await self.repository.delete(asset)
        return True


