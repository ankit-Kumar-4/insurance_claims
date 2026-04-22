"""
Premium management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import premium as premium_crud
from app.schemas.premium import (
    PremiumCreate,
    PremiumUpdate,
    PremiumResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/premiums", tags=["premiums"])


@router.get("/", response_model=PaginatedResponse[PremiumResponse])
async def list_premiums(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of premiums with pagination
    """
    items = await premium_crud.get_multi(db, skip=skip, limit=limit)
    total = await premium_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=PremiumResponse)
async def get_premium(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific premium by ID
    """
    item = await premium_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Premium not found"
        )
    return item


@router.post("/", response_model=PremiumResponse, status_code=status.HTTP_201_CREATED)
async def create_premium(
    item_in: PremiumCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new premium
    """
    item = await premium_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=PremiumResponse)
async def update_premium(
    item_id: int,
    item_update: PremiumUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing premium
    """
    item = await premium_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Premium not found"
        )
    
    updated_item = await premium_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_premium(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete premium
    """
    item = await premium_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Premium not found"
        )
    
    await premium_crud.remove(db, id=item_id)
    return SuccessResponse(message="Premium deleted successfully")
