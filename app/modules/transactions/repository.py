from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.transactions.models import Transaction


class TransactionRepository:
    """Repository for Transaction data access - handles all DB operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        portfolio_id: int,
        symbol: str,
        amount,
        price,
        operation_type: str,
        operation_time=None
    ) -> Transaction:
        """Create a new transaction in the database."""
        transaction = Transaction(
            portfolio_id=portfolio_id,
            symbol=symbol,
            amount=amount,
            price=price,
            operation_type=operation_type,
            operation_time=operation_time
        )
        self.session.add(transaction)
        await self.session.flush()
        await self.session.refresh(transaction)
        return transaction

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        """Get transaction by ID from database."""
        query = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_portfolio(self, portfolio_id: int) -> list[Transaction]:
        """Get all transactions for a specific portfolio from database."""
        query = select(Transaction).where(Transaction.portfolio_id == portfolio_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, transaction: Transaction, **kwargs) -> Transaction:
        """Update transaction fields."""
        for key, value in kwargs.items():
            if hasattr(transaction, key) and value is not None:
                setattr(transaction, key, value)

        await self.session.flush()
        await self.session.refresh(transaction)
        return transaction

    async def delete(self, transaction: Transaction) -> None:
        """Delete a transaction from database."""
        await self.session.delete(transaction)
        await self.session.flush()

    
    

