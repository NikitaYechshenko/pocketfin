from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.modules.users.deps import get_current_user
from app.modules.users.models import User
from app.modules.portfolio.schemas import PortfolioCreate, PortfolioRead, PortfolioUpdate, PortfolioWithTransactionsRead
from app.modules.portfolio.service import PortfolioService

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("", response_model=PortfolioRead, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio_data: PortfolioCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new portfolio for the current user."""
    service = PortfolioService(session)
    portfolio = await service.create_portfolio(user.id, portfolio_data)
    await session.commit()
    return portfolio


@router.get("", response_model=list[PortfolioRead])
async def get_portfolios(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all portfolios for the current user."""
    service = PortfolioService(session)
    portfolios = await service.get_user_portfolios(user.id)
    return portfolios


@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def get_portfolio(
    portfolio_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get a specific portfolio by ID."""
    service = PortfolioService(session)
    portfolio = await service.get_portfolio_by_id(portfolio_id, user.id)

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return portfolio


@router.patch("/{portfolio_id}", response_model=PortfolioRead)
async def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update a portfolio."""
    service = PortfolioService(session)
    portfolio = await service.update_portfolio(portfolio_id, user.id, portfolio_data)

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    await session.commit()
    return portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(
    portfolio_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a portfolio."""
    service = PortfolioService(session)
    deleted = await service.delete_portfolio(portfolio_id, user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    await session.commit()


@router.get("/{portfolio_id}/with-assets", response_model=PortfolioWithTransactionsRead , summary="Get portfolio with all assets")
async def get_portfolio_with_assets(
    portfolio_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get portfolio by ID along with a list of all its assets.
    
    Steps:
    - Request portfolio by ID
    - Verify it belongs to the current user
    - Return portfolio with full asset list (symbol, amount, operation_type, etc.)
    
    """
    service = PortfolioService(session)
    try:
        return await service.get_portfolio_with_assets(portfolio_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))