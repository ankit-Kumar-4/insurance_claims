"""Policy Renewal schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.renewal import RenewalStatus


class PolicyRenewalBase(BaseSchema):
    """Base policy renewal schema"""
    policy_id: int = Field(..., gt=0)
    renewal_date: date
    new_premium: Decimal = Field(..., gt=0)
    status: RenewalStatus = RenewalStatus.PENDING
    notes: Optional[str] = Field(None, max_length=1000)


class PolicyRenewalCreate(PolicyRenewalBase):
    """Schema for creating a policy renewal"""
    pass


class PolicyRenewalUpdate(BaseSchema):
    """Schema for updating a policy renewal"""
    renewal_date: Optional[date] = None
    new_premium: Optional[Decimal] = Field(None, gt=0)
    status: Optional[RenewalStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)


class PolicyRenewalResponse(PolicyRenewalBase, ResponseSchema):
    """Schema for policy renewal response"""
    processed_date: Optional[date] = None


class PolicyRenewalInDB(PolicyRenewalResponse):
    """Schema for policy renewal in database"""
    pass
