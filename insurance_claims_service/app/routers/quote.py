"""
Quote management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import quote as quote_crud
from app.schemas.quote import (
    QuoteCreate,
    QuoteUpdate,
    QuoteResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/", response_model=PaginatedResponse[QuoteResponse])
async def list_quotes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of quotes with pagination
    """
    items = await quote_crud.get_multi(db, skip=skip, limit=limit)
    total = await quote_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=QuoteResponse)
async def get_quote(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific quote by ID
    """
    item = await quote_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    return item


@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(
    item_in: QuoteCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new quote
    """
    item = await quote_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=QuoteResponse)
async def update_quote(
    item_id: int,
    item_update: QuoteUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing quote
    """
    item = await quote_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    updated_item = await quote_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_quote(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete quote
    """
    item = await quote_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    await quote_crud.remove(db, id=item_id)
    return SuccessResponse(message="Quote deleted successfully")
