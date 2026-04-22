"""Claim schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.claim import ClaimType, ClaimStatus


class ClaimBase(BaseSchema):
    """Base claim schema"""
    claim_number: str = Field(..., min_length=1, max_length=50)
    claim_type: ClaimType
    policy_id: int = Field(..., gt=0)
    claim_date: date
    incident_date: date
    status: ClaimStatus
    claim_amount: Decimal = Field(..., gt=0)
    description: str = Field(..., min_length=10, max_length=2000)


class ClaimCreate(ClaimBase):
    """Schema for creating a claim"""
    pass


class ClaimUpdate(BaseSchema):
    """Schema for updating a claim"""
    status: Optional[ClaimStatus] = None
    claim_amount: Optional[Decimal] = Field(None, gt=0)
    approved_amount: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    rejection_reason: Optional[str] = None


class ClaimResponse(ClaimBase, ResponseSchema):
    """Schema for claim response"""
    approved_amount: Optional[Decimal] = None
    rejection_reason: Optional[str] = None
    settled_date: Optional[date] = None


class ClaimInDB(ClaimResponse):
    """Schema for claim in database"""
    pass
