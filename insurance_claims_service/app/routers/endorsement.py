"""
Endorsement management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import endorsement as endorsement_crud
from app.schemas.endorsement import (
    EndorsementCreate,
    EndorsementUpdate,
    EndorsementResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/endorsements", tags=["endorsements"])


@router.get("/", response_model=PaginatedResponse[EndorsementResponse])
async def list_endorsements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of endorsements with pagination
    """
    items = await endorsement_crud.get_multi(db, skip=skip, limit=limit)
    total = await endorsement_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=EndorsementResponse)
async def get_endorsement(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific endorsement by ID
    """
    item = await endorsement_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endorsement not found"
        )
    return item


@router.post("/", response_model=EndorsementResponse, status_code=status.HTTP_201_CREATED)
async def create_endorsement(
    item_in: EndorsementCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new endorsement
    """
    item = await endorsement_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=EndorsementResponse)
async def update_endorsement(
    item_id: int,
    item_update: EndorsementUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing endorsement
    """
    item = await endorsement_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endorsement not found"
        )
    
    updated_item = await endorsement_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_endorsement(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete endorsement
    """
    item = await endorsement_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endorsement not found"
        )
    
    await endorsement_crud.remove(db, id=item_id)
    return SuccessResponse(message="Endorsement deleted successfully")
