# Service layer for Portfolio operations.
#
# The Service is where business logic lives:
# - access control (portfolio ownership checks),
# - data preparation for API responses (validation/schemas),
# - database operations are delegated to the repository.

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.portfolio.repository import PortfolioRepository
from app.modules.portfolio.schemas import PortfolioCreate, PortfolioRead, PortfolioUpdate, PortfolioWithTransactionsRead


class PortfolioService:
    """Service for portfolio business logic - uses Repository for DB access.

    Overview:
    - Receives an AsyncSession from the router/dependencies.
    - Creates a repository and calls its methods for DB read/write operations.
    - Returns Pydantic schemas (e.g. `PortfolioRead`) for JSON serialization.
    """

    def __init__(self, session: AsyncSession):
        # Repository is created once and stored as an instance attribute.
        # Benefits:
        # - No need to pass session/repository to each method.
        # - Easy to mock self.repository in tests.
        # - Repository uses the provided session for all operations.
        self.repository = PortfolioRepository(session)

    async def create_portfolio(
        self, user_id: int, portfolio_data: PortfolioCreate
    ) -> PortfolioRead:
        """Create a new portfolio for the user.

        Steps:
        1) Repository creates a DB record with `portfolio_data.name` linked to `user_id`.
        2) Service converts the model to a Pydantic schema (`PortfolioRead.model_validate`)
           for the API response.
        """
        portfolio = await self.repository.create(user_id, portfolio_data.name)
        return PortfolioRead.model_validate(portfolio)

    async def get_user_portfolios(self, user_id: int) -> list[PortfolioRead]:
        """Return all portfolios for a specific user.

        Note:
        - Repository returns SQLAlchemy model objects.
        - Each object is converted to a Pydantic schema for safe serialization.
        """
        portfolios = await self.repository.get_by_user_id(user_id)
        return [PortfolioRead.model_validate(p) for p in portfolios]

    async def get_portfolio_by_id(
        self, portfolio_id: int, user_id: int
    ) -> PortfolioRead | None:
        """Return a portfolio by ID only if it belongs to the user.

        Security check: `get_by_id_and_user` searches with owner filter,
        preventing access to other users' portfolios.
        Returns `None` if not found.
        """
        portfolio = await self.repository.get_by_id_and_user(portfolio_id, user_id)
        return PortfolioRead.model_validate(portfolio) if portfolio else None

    async def update_portfolio(
        self, portfolio_id: int, user_id: int, portfolio_data: PortfolioUpdate
    ) -> PortfolioRead | None:
        """Update a portfolio (partial update supported).

        Steps:
        - First check if the portfolio belongs to the user (get_by_id_and_user).
        - `model_dump(exclude_unset=True)` extracts only fields that were
          actually provided (for PATCH-style partial updates).
        - Pass data to the repository, which saves changes and returns the updated object.
        - Returns `None` if portfolio not found.
        """
        portfolio = await self.repository.get_by_id_and_user(portfolio_id, user_id)
        
        if not portfolio:
            return None

        # Extract only fields that were explicitly provided in the request
        update_data = portfolio_data.model_dump(exclude_unset=True)
        
        portfolio = await self.repository.update(portfolio, **update_data)
        return PortfolioRead.model_validate(portfolio)

    async def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        """Delete a portfolio if it belongs to the user.

        Returns `True` on successful deletion, `False` if portfolio not found
        (e.g., does not belong to the user).
        """
        portfolio = await self.repository.get_by_id_and_user(portfolio_id, user_id)
        
        if not portfolio:
            return False

        await self.repository.delete(portfolio)
        return True
    
    ################################################

    async def get_portfolio_with_assets(self, portfolio_id: int, user_id: int) -> PortfolioWithTransactionsRead:
        """
        Get portfolio with all its assets.
        
        Overview:
        - Load portfolio by ID and verify user ownership.
        - SQLAlchemy eagerly loads related assets via relationship.
        - Returns portfolio in PortfolioWithAssetsRead format (includes assets list).
        
        Args:
            portfolio_id: Portfolio ID
            user_id: User ID (for ownership verification)
            
        Returns:
            PortfolioWithAssets: Portfolio with nested assets list
            
        Raises:
            ValueError: If portfolio not found or user doesn't have access
        """
        portfolio = await self.repository.get_by_id_and_user_with_assets(portfolio_id, user_id)
        
        # Check that portfolio exists and belongs to the user
        if not portfolio:
            raise ValueError(f"Portfolio with id {portfolio_id} not found or access denied")
        
        # Convert to Pydantic schema with nested assets
        # SQLAlchemy has already loaded assets via relationship("Asset", ...)
        return PortfolioWithTransactionsRead.model_validate(portfolio)