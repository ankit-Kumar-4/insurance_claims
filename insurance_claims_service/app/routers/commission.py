"""
Commission management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import commission as commission_crud
from app.schemas.commission import (
    CommissionCreate,
    CommissionUpdate,
    CommissionResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/commissions", tags=["commissions"])


@router.get("/", response_model=PaginatedResponse[CommissionResponse])
async def list_commissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of commissions with pagination
    """
    items = await commission_crud.get_multi(db, skip=skip, limit=limit)
    total = await commission_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=CommissionResponse)
async def get_commission(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific commission by ID
    """
    item = await commission_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )
    return item


@router.post("/", response_model=CommissionResponse, status_code=status.HTTP_201_CREATED)
async def create_commission(
    item_in: CommissionCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new commission
    """
    item = await commission_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=CommissionResponse)
async def update_commission(
    item_id: int,
    item_update: CommissionUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing commission
    """
    item = await commission_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )
    
    updated_item = await commission_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_commission(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete commission
    """
    item = await commission_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )
    
    await commission_crud.remove(db, id=item_id)
    return SuccessResponse(message="Commission deleted successfully")
