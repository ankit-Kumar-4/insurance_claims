"""
Underwriter management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import underwriter as underwriter_crud
from app.schemas.underwriter import (
    UnderwriterCreate,
    UnderwriterUpdate,
    UnderwriterResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/underwriters", tags=["underwriters"])


@router.get("/", response_model=PaginatedResponse[UnderwriterResponse])
async def list_underwriters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of underwriters with pagination
    """
    items = await underwriter_crud.get_multi(db, skip=skip, limit=limit)
    total = await underwriter_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=UnderwriterResponse)
async def get_underwriter(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific underwriter by ID
    """
    item = await underwriter_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Underwriter not found"
        )
    return item


@router.post("/", response_model=UnderwriterResponse, status_code=status.HTTP_201_CREATED)
async def create_underwriter(
    item_in: UnderwriterCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new underwriter
    """
    item = await underwriter_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=UnderwriterResponse)
async def update_underwriter(
    item_id: int,
    item_update: UnderwriterUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing underwriter
    """
    item = await underwriter_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Underwriter not found"
        )
    
    updated_item = await underwriter_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_underwriter(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete underwriter
    """
    item = await underwriter_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Underwriter not found"
        )
    
    await underwriter_crud.remove(db, id=item_id)
    return SuccessResponse(message="Underwriter deleted successfully")
