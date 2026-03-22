# Service layer for Transaction operations.
#
# Same purpose as PortfolioService:
# - Access control (transaction ownership checks via portfolio ownership),
# - Data conversion to Pydantic schemas for API,
# - Database operations delegated to TransactionRepository.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.transactions.repository import TransactionRepository
from app.modules.transactions.schemas import TransactionCreate, TransactionRead, TransactionUpdate
from app.modules.transactions.models import Transaction
from app.modules.portfolio.models import Portfolio
from app.core.exceptions import PortfolioNotFoundError, PortfolioAccessDeniedError, TransactionNotFoundError, TransactionAccessDeniedError


class TransactionService:
    """Service for transaction business logic - uses Repository for DB access."""

    def __init__(self, session: AsyncSession):
        self.repository = TransactionRepository(session)
        self.session = session

    async def _verify_portfolio_ownership(self, portfolio_id: int, user_id: int) -> Portfolio:
        """
        Verify that the portfolio belongs to the user.

        Args:
            portfolio_id: Portfolio ID to check
            user_id: User ID to verify ownership against

        Returns:
            Portfolio: The portfolio object if ownership is verified

        Raises:
            PortfolioNotFoundError: If portfolio doesn't exist
            PortfolioAccessDeniedError: If portfolio doesn't belong to the user
        """
        query = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await self.session.execute(query)
        portfolio = result.scalars().first()

        if not portfolio:
            raise PortfolioNotFoundError(portfolio_id)

        if portfolio.user_id != user_id:
            raise PortfolioAccessDeniedError()

        return portfolio

    async def _get_transaction_with_ownership_check(self, transaction_id: int, user_id: int) -> Transaction:
        """
        Get transaction and verify user owns it (via portfolio ownership).

        Args:
            transaction_id: Transaction ID
            user_id: User ID

        Returns:
            Transaction: The transaction object

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionAccessDeniedError: If user doesn't own the portfolio containing this transaction
        """
        query = (
            select(Transaction)
            .options(selectinload(Transaction.portfolio))
            .where(Transaction.id == transaction_id)
        )
        result = await self.session.execute(query)
        transaction = result.scalars().first()

        if not transaction:
            raise TransactionNotFoundError(transaction_id)

        if transaction.portfolio.user_id != user_id:
            raise TransactionAccessDeniedError()

        return transaction

    async def create_transaction(
        self, user_id: int, transaction_data: TransactionCreate
    ) -> TransactionRead:
        """
        Create a new transaction in the specified portfolio for the user.

        Security: Verifies that the user owns the portfolio before creating the transaction.

        Args:
            user_id: ID of the user creating the transaction
            transaction_data: Transaction creation data (includes portfolio_id)

        Returns:
            TransactionRead: Created transaction data

        Raises:
            PortfolioNotFoundError: If portfolio doesn't exist
            PortfolioAccessDeniedError: If user doesn't own the portfolio
        """
        # Critical security check: verify user owns the portfolio
        await self._verify_portfolio_ownership(transaction_data.portfolio_id, user_id)

        transaction = await self.repository.create(
            portfolio_id=transaction_data.portfolio_id,
            symbol=transaction_data.symbol,
            amount=transaction_data.amount,
            price=transaction_data.price,
            operation_type=transaction_data.operation_type,
            operation_time=transaction_data.operation_time
        )
        return TransactionRead.model_validate(transaction)

    async def get_portfolio_transactions(self, portfolio_id: int, user_id: int) -> list[TransactionRead]:
        """
        Return all transactions for a specific portfolio.

        Security: Verifies that the user owns the portfolio.

        Args:
            portfolio_id: Portfolio ID
            user_id: User ID

        Returns:
            List of transactions in the portfolio

        Raises:
            PortfolioNotFoundError: If portfolio doesn't exist
            PortfolioAccessDeniedError: If user doesn't own the portfolio
        """
        # Verify ownership
        await self._verify_portfolio_ownership(portfolio_id, user_id)

        transactions = await self.repository.get_by_portfolio(portfolio_id)
        return [TransactionRead.model_validate(t) for t in transactions]

    async def get_user_transactions(self, user_id: int) -> list[TransactionRead]:
        """
        Return all transactions for the user (from all their portfolios).

        Args:
            user_id: User ID

        Returns:
            List of all user's transactions across all portfolios
        """
        # Get all user's portfolios
        query = select(Portfolio.id).where(Portfolio.user_id == user_id)
        result = await self.session.execute(query)
        portfolio_ids = result.scalars().all()

        # Get all transactions from these portfolios
        if not portfolio_ids:
            return []

        query = select(Transaction).where(Transaction.portfolio_id.in_(portfolio_ids))
        result = await self.session.execute(query)
        transactions = result.scalars().all()

        return [TransactionRead.model_validate(t) for t in transactions]

    async def get_transaction_by_id(
        self, transaction_id: int, user_id: int
    ) -> TransactionRead:
        """
        Return a transaction by ID only if it belongs to the user.

        Args:
            transaction_id: Transaction ID
            user_id: User ID

        Returns:
            TransactionRead: Transaction data

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionAccessDeniedError: If user doesn't own the transaction
        """
        transaction = await self._get_transaction_with_ownership_check(transaction_id, user_id)
        return TransactionRead.model_validate(transaction)

    async def update_transaction(
        self, transaction_id: int, user_id: int, transaction_data: TransactionUpdate
    ) -> TransactionRead:
        """
        Update a transaction (partial update supported).

        Args:
            transaction_id: Transaction ID
            user_id: User ID
            transaction_data: Update data

        Returns:
            TransactionRead: Updated transaction data

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionAccessDeniedError: If user doesn't own the transaction
        """
        transaction = await self._get_transaction_with_ownership_check(transaction_id, user_id)

        update_data = transaction_data.model_dump(exclude_unset=True)
        transaction = await self.repository.update(transaction, **update_data)
        return TransactionRead.model_validate(transaction)

    async def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        """
        Delete a transaction if it belongs to the user.

        Args:
            transaction_id: Transaction ID
            user_id: User ID

        Raises:
            TransactionNotFoundError: If transaction doesn't exist
            TransactionAccessDeniedError: If user doesn't own the transaction
        """
        transaction = await self._get_transaction_with_ownership_check(transaction_id, user_id)
        await self.repository.delete(transaction)



