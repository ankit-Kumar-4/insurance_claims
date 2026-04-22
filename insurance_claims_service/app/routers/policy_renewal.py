"""
Policy Renewal management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import policy_renewal as policy_renewal_crud
from app.schemas.policy_renewal import (
    PolicyRenewalCreate,
    PolicyRenewalUpdate,
    PolicyRenewalResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/policy-renewals", tags=["policy-renewals"])


@router.get("/", response_model=PaginatedResponse[PolicyRenewalResponse])
async def list_policy_renewals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of policy-renewals with pagination
    """
    items = await policy_renewal_crud.get_multi(db, skip=skip, limit=limit)
    total = await policy_renewal_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=PolicyRenewalResponse)
async def get_policy_renewal(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific policy_renewal by ID
    """
    item = await policy_renewal_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PolicyRenewal not found"
        )
    return item


@router.post("/", response_model=PolicyRenewalResponse, status_code=status.HTTP_201_CREATED)
async def create_policy_renewal(
    item_in: PolicyRenewalCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new policy_renewal
    """
    item = await policy_renewal_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=PolicyRenewalResponse)
async def update_policy_renewal(
    item_id: int,
    item_update: PolicyRenewalUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing policy_renewal
    """
    item = await policy_renewal_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PolicyRenewal not found"
        )
    
    updated_item = await policy_renewal_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_policy_renewal(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete policy_renewal
    """
    item = await policy_renewal_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PolicyRenewal not found"
        )
    
    await policy_renewal_crud.remove(db, id=item_id)
    return SuccessResponse(message="PolicyRenewal deleted successfully")
