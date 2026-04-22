"""
Property management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import property as property_crud
from app.schemas.property import (
    PropertyCreate,
    PropertyUpdate,
    PropertyResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/", response_model=PaginatedResponse[PropertyResponse])
async def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of properties with pagination
    """
    items = await property_crud.get_multi(db, skip=skip, limit=limit)
    total = await property_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=PropertyResponse)
async def get_property(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific property by ID
    """
    item = await property_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return item


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    item_in: PropertyCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new property
    """
    item = await property_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=PropertyResponse)
async def update_property(
    item_id: int,
    item_update: PropertyUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing property
    """
    item = await property_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    updated_item = await property_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_property(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete property
    """
    item = await property_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    await property_crud.remove(db, id=item_id)
    return SuccessResponse(message="Property deleted successfully")
