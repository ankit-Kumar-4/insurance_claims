"""
Coverage management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import coverage as coverage_crud
from app.schemas.coverage import (
    CoverageCreate,
    CoverageUpdate,
    CoverageResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/coverages", tags=["coverages"])


@router.get("/", response_model=PaginatedResponse[CoverageResponse])
async def list_coverages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of coverages with pagination
    """
    items = await coverage_crud.get_multi(db, skip=skip, limit=limit)
    total = await coverage_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=CoverageResponse)
async def get_coverage(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific coverage by ID
    """
    item = await coverage_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coverage not found"
        )
    return item


@router.post("/", response_model=CoverageResponse, status_code=status.HTTP_201_CREATED)
async def create_coverage(
    item_in: CoverageCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new coverage
    """
    item = await coverage_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=CoverageResponse)
async def update_coverage(
    item_id: int,
    item_update: CoverageUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing coverage
    """
    item = await coverage_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coverage not found"
        )
    
    updated_item = await coverage_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_coverage(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete coverage
    """
    item = await coverage_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coverage not found"
        )
    
    await coverage_crud.remove(db, id=item_id)
    return SuccessResponse(message="Coverage deleted successfully")
