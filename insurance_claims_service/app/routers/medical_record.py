"""
Medical Record management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import medical_record as medical_record_crud
from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/medical-records", tags=["medical-records"])


@router.get("/", response_model=PaginatedResponse[MedicalRecordResponse])
async def list_medical_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of medical-records with pagination
    """
    items = await medical_record_crud.get_multi(db, skip=skip, limit=limit)
    total = await medical_record_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=MedicalRecordResponse)
async def get_medical_record(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific medical_record by ID
    """
    item = await medical_record_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MedicalRecord not found"
        )
    return item


@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_record(
    item_in: MedicalRecordCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new medical_record
    """
    item = await medical_record_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=MedicalRecordResponse)
async def update_medical_record(
    item_id: int,
    item_update: MedicalRecordUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing medical_record
    """
    item = await medical_record_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MedicalRecord not found"
        )
    
    updated_item = await medical_record_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_medical_record(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete medical_record
    """
    item = await medical_record_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MedicalRecord not found"
        )
    
    await medical_record_crud.remove(db, id=item_id)
    return SuccessResponse(message="MedicalRecord deleted successfully")
