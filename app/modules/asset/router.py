from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.modules.users.manager import fastapi_users
from app.modules.users.models import User
from app.modules.asset.schemas import AssetCreate, AssetRead, AssetUpdate
from app.modules.asset.service import AssetService

router = APIRouter(prefix="/assets", tags=["assets"])

# Dependency to get the currently authenticated user
current_user = fastapi_users.current_user()


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new asset in portfolio for the current user."""
    service = AssetService(session)
    asset = await service.create_asset(user.id, asset_data)
    await session.commit()
    return asset


@router.get("", response_model=list[AssetRead])
async def get_assets(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all assets for the current user."""
    service = AssetService(session)
    assets = await service.get_user_assets(user.id)
    return assets


@router.get("/{asset_id}", response_model=AssetRead)
async def get_asset(
    asset_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get a specific asset by ID."""
    service = AssetService(session)
    asset = await service.get_asset_by_id(asset_id, user.id)

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    return asset


@router.patch("/{asset_id}", response_model=AssetRead)
async def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update an asset."""
    service = AssetService(session)
    asset = await service.update_asset(asset_id, user.id, asset_data)

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    await session.commit()
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete an asset."""
    service = AssetService(session)
    deleted = await service.delete_asset(asset_id, user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    await session.commit()


