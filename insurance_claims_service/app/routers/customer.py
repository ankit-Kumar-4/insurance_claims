"""
Customer management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import customer as customer_crud
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=PaginatedResponse[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of customers with pagination
    """
    items = await customer_crud.get_multi(db, skip=skip, limit=limit)
    total = await customer_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=CustomerResponse)
async def get_customer(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific customer by ID
    """
    item = await customer_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return item


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    item_in: CustomerCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new customer
    """
    item = await customer_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=CustomerResponse)
async def update_customer(
    item_id: int,
    item_update: CustomerUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing customer
    """
    item = await customer_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    updated_item = await customer_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_customer(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete customer
    """
    item = await customer_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    await customer_crud.remove(db, id=item_id)
    return SuccessResponse(message="Customer deleted successfully")
