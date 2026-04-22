"""
Policy management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent, require_underwriter
from app.crud import policy as policy_crud
from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyInDB
)
from app.schemas.base import PaginatedResponse, SuccessResponse
from app.enums.policy import PolicyStatus, PolicyType

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("/", response_model=PaginatedResponse[PolicyResponse])
async def list_policies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    policy_type: Optional[PolicyType] = None,
    status: Optional[PolicyStatus] = None,
    customer_id: Optional[int] = None,
    agent_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of policies with pagination and filters
    """
    filters = {}
    if policy_type:
        filters["policy_type"] = policy_type
    if status:
        filters["status"] = status
    if customer_id:
        filters["customer_id"] = customer_id
    if agent_id:
        filters["agent_id"] = agent_id
    
    policies = await policy_crud.get_multi(db, skip=skip, limit=limit, filters=filters)
    total = await policy_crud.count(db, filters=filters)
    
    return PaginatedResponse(
        items=policies,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific policy by ID
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    return policy


@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_in: PolicyCreate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new policy (requires agent role)
    """
    policy = await policy_crud.create(db, obj_in=policy_in)
    return policy


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: int,
    policy_update: PolicyUpdate,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Update existing policy (requires agent role)
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    updated_policy = await policy_crud.update(db, db_obj=policy, obj_in=policy_update)
    return updated_policy


@router.delete("/{policy_id}", response_model=SuccessResponse)
async def delete_policy(
    policy_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete policy (requires agent role)
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    await policy_crud.remove(db, id=policy_id)
    return SuccessResponse(message="Policy deleted successfully")


# Custom operations

@router.post("/{policy_id}/activate", response_model=PolicyResponse)
async def activate_policy(
    policy_id: int,
    current_user: User = Depends(require_underwriter),
    db: AsyncSession = Depends(get_db)
):
    """
    Activate a policy (requires underwriter role)
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    if policy.status == PolicyStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Policy is already active"
        )
    
    updated_policy = await policy_crud.update(
        db, 
        db_obj=policy, 
        obj_in=PolicyUpdate(status=PolicyStatus.ACTIVE)
    )
    return updated_policy


@router.post("/{policy_id}/cancel", response_model=PolicyResponse)
async def cancel_policy(
    policy_id: int,
    reason: str = Query(..., min_length=10),
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel a policy (requires agent role)
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    if policy.status == PolicyStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Policy is already cancelled"
        )
    
    updated_policy = await policy_crud.update(
        db,
        db_obj=policy,
        obj_in=PolicyUpdate(status=PolicyStatus.CANCELLED)
    )
    return updated_policy


@router.post("/{policy_id}/suspend", response_model=PolicyResponse)
async def suspend_policy(
    policy_id: int,
    reason: str = Query(..., min_length=10),
    current_user: User = Depends(require_underwriter),
    db: AsyncSession = Depends(get_db)
):
    """
    Suspend a policy (requires underwriter role)
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    updated_policy = await policy_crud.update(
        db,
        db_obj=policy,
        obj_in=PolicyUpdate(status=PolicyStatus.SUSPENDED)
    )
    return updated_policy


@router.get("/{policy_id}/coverage", response_model=List[dict])
async def get_policy_coverage(
    policy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all coverage items for a policy
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # TODO: Implement coverage retrieval
    return []


@router.get("/{policy_id}/claims", response_model=List[dict])
async def get_policy_claims(
    policy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all claims for a policy
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # TODO: Implement claims retrieval
    return []


@router.get("/{policy_id}/payments", response_model=List[dict])
async def get_policy_payments(
    policy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all payments for a policy
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # TODO: Implement payments retrieval
    return []


@router.get("/{policy_id}/beneficiaries", response_model=List[dict])
async def get_policy_beneficiaries(
    policy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all beneficiaries for a policy
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # TODO: Implement beneficiaries retrieval
    return []


@router.get("/{policy_id}/documents", response_model=List[dict])
async def get_policy_documents(
    policy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all documents for a policy
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # TODO: Implement documents retrieval
    return []


@router.post("/{policy_id}/renew", response_model=PolicyResponse)
async def renew_policy(
    policy_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Initiate policy renewal process (requires agent role)
    """
    policy = await policy_crud.get(db, id=policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    if policy.status != PolicyStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active policies can be renewed"
        )
    
    # TODO: Implement renewal logic
    return policy


@router.get("/customer/{customer_id}", response_model=List[PolicyResponse])
async def get_customer_policies(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all policies for a specific customer
    """
    policies = await policy_crud.get_multi(
        db,
        filters={"customer_id": customer_id}
    )
    return policies


@router.get("/expiring-soon", response_model=List[PolicyResponse])
async def get_expiring_policies(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Get policies expiring within specified days (requires agent role)
    """
    # TODO: Implement expiration date filtering
    return []
