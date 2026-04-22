"""
Risk Assessment management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import risk_assessment as risk_assessment_crud
from app.schemas.risk_assessment import (
    RiskAssessmentCreate,
    RiskAssessmentUpdate,
    RiskAssessmentResponse,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/risk-assessments", tags=["risk-assessments"])


@router.get("/", response_model=PaginatedResponse[RiskAssessmentResponse])
async def list_risk_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of risk-assessments with pagination
    """
    items = await risk_assessment_crud.get_multi(db, skip=skip, limit=limit)
    total = await risk_assessment_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{item_id}", response_model=RiskAssessmentResponse)
async def get_risk_assessment(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific risk_assessment by ID
    """
    item = await risk_assessment_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RiskAssessment not found"
        )
    return item


@router.post("/", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_assessment(
    item_in: RiskAssessmentCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new risk_assessment
    """
    item = await risk_assessment_crud.create(db, obj_in=item_in)
    return item


@router.put("/{item_id}", response_model=RiskAssessmentResponse)
async def update_risk_assessment(
    item_id: int,
    item_update: RiskAssessmentUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing risk_assessment
    """
    item = await risk_assessment_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RiskAssessment not found"
        )
    
    updated_item = await risk_assessment_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{item_id}", response_model=SuccessResponse)
async def delete_risk_assessment(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete risk_assessment
    """
    item = await risk_assessment_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RiskAssessment not found"
        )
    
    await risk_assessment_crud.remove(db, id=item_id)
    return SuccessResponse(message="RiskAssessment deleted successfully")
