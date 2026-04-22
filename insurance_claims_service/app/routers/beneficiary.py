"""
Beneficiary management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import beneficiary as beneficiary_crud
from app.schemas.beneficiary import (
    BeneficiaryCreate,
    BeneficiaryUpdate,
    BeneficiaryResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/beneficiaries", tags=["beneficiaries"])


@router.get("/", response_model=PaginatedResponse[BeneficiaryResponse])
async def list_beneficiaries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of beneficiaries with pagination
    """
    items = await beneficiary_crud.get_multi(db, skip=skip, limit=limit)
    total = await beneficiary_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=BeneficiaryResponse)
async def get_beneficiary(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific beneficiary by ID
    """
    item = await beneficiary_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Beneficiary not found"
        )
    return item


@router.post("/", response_model=BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_beneficiary(
    item_in: BeneficiaryCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new beneficiary
    """
    item = await beneficiary_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=BeneficiaryResponse)
async def update_beneficiary(
    item_id: int,
    item_update: BeneficiaryUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing beneficiary
    """
    item = await beneficiary_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Beneficiary not found"
        )
    
    updated_item = await beneficiary_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_beneficiary(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete beneficiary
    """
    item = await beneficiary_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Beneficiary not found"
        )
    
    await beneficiary_crud.remove(db, id=item_id)
    return SuccessResponse(message="Beneficiary deleted successfully")
