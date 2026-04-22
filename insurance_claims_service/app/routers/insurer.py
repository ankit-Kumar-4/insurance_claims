"""
Insurer management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import insurer as insurer_crud
from app.schemas.insurer import (
    InsurerCreate,
    InsurerUpdate,
    InsurerResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/insurers", tags=["insurers"])


@router.get("/", response_model=PaginatedResponse[InsurerResponse])
async def list_insurers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of insurers with pagination
    """
    items = await insurer_crud.get_multi(db, skip=skip, limit=limit)
    total = await insurer_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=InsurerResponse)
async def get_insurer(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific insurer by ID
    """
    item = await insurer_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurer not found"
        )
    return item


@router.post("/", response_model=InsurerResponse, status_code=status.HTTP_201_CREATED)
async def create_insurer(
    item_in: InsurerCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new insurer
    """
    item = await insurer_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=InsurerResponse)
async def update_insurer(
    item_id: int,
    item_update: InsurerUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing insurer
    """
    item = await insurer_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurer not found"
        )
    
    updated_item = await insurer_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_insurer(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete insurer
    """
    item = await insurer_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insurer not found"
        )
    
    await insurer_crud.remove(db, id=item_id)
    return SuccessResponse(message="Insurer deleted successfully")
