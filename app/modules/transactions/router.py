from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.modules.users.deps import get_current_user
from app.modules.users.models import User
from app.modules.transactions.schemas import TransactionCreate, TransactionRead, TransactionUpdate
from app.modules.transactions.service import TransactionService
from app.core.exceptions import (
    PortfolioNotFoundError,
    PortfolioAccessDeniedError,
    TransactionNotFoundError,
    TransactionAccessDeniedError
)

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new transaction in a portfolio.

    The user must own the portfolio to add transactions to it.
    """
    service = TransactionService(session)
    try:
        transaction = await service.create_transaction(user.id, transaction_data)
        await session.commit()
        return transaction
    except (PortfolioNotFoundError, PortfolioAccessDeniedError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("", response_model=list[TransactionRead])
async def get_user_transactions(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all transactions for the current user across all portfolios."""
    service = TransactionService(session)
    transactions = await service.get_user_transactions(user.id)
    return transactions


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get a specific transaction by ID."""
    service = TransactionService(session)
    try:
        transaction = await service.get_transaction_by_id(transaction_id, user.id)
        return transaction
    except (TransactionNotFoundError, TransactionAccessDeniedError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update a transaction."""
    service = TransactionService(session)
    try:
        transaction = await service.update_transaction(transaction_id, user.id, transaction_data)
        await session.commit()
        return transaction
    except (TransactionNotFoundError, TransactionAccessDeniedError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a transaction."""
    service = TransactionService(session)
    try:
        await service.delete_transaction(transaction_id, user.id)
        await session.commit()
    except (TransactionNotFoundError, TransactionAccessDeniedError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
