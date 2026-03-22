from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.modules.portfolio.models import Portfolio


class PortfolioRepository:
    """Repository for Portfolio data access - handles all DB operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, name: str) -> Portfolio:
        """Create a new portfolio in the database."""
        portfolio = Portfolio(name=name, user_id=user_id)
        self.session.add(portfolio)
        await self.session.flush()
        await self.session.refresh(portfolio)
        return portfolio

    async def get_by_id(self, portfolio_id: int) -> Portfolio | None:
        """Get portfolio by ID from database."""
        query = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_user_id(self, user_id: int) -> list[Portfolio]:
        """Get all portfolios for a specific user from database."""
        query = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id_and_user(self, portfolio_id: int, user_id: int) -> Portfolio | None:
        """Get portfolio by ID with user ownership check."""
        query = select(Portfolio).where(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == user_id,
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id_and_user_with_assets(self, portfolio_id: int, user_id: int) -> Portfolio | None:
        """Get portfolio by ID with user ownership check and eagerly load assets."""
        query = (
            select(Portfolio)
            .options(selectinload(Portfolio.transactions))  # Eagerly load transactions (assets)
            .where(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id,
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, portfolio: Portfolio, **kwargs) -> Portfolio:
        """Update portfolio fields."""
        for key, value in kwargs.items():
            if hasattr(portfolio, key) and value is not None:
                setattr(portfolio, key, value)
        
        await self.session.flush()
        await self.session.refresh(portfolio)
        return portfolio

    async def delete(self, portfolio: Portfolio) -> None:
        """Delete a portfolio from database."""
        await self.session.delete(portfolio)
        await self.session.flush()

