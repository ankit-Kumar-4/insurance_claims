"""Policy schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.policy import PolicyType, PolicyStatus, PremiumFrequency


class PolicyBase(BaseSchema):
    """Base policy schema"""
    policy_number: str = Field(..., min_length=1, max_length=50)
    policy_type: PolicyType
    policy_holder_id: int = Field(..., gt=0)
    insurer_id: int = Field(..., gt=0)
    start_date: date
    end_date: date
    status: PolicyStatus
    premium_amount: Decimal = Field(..., gt=0)
    coverage_amount: Decimal = Field(..., gt=0)
    deductible: Decimal = Field(..., ge=0)
    premium_frequency: Optional[PremiumFrequency] = PremiumFrequency.ANNUALLY


class PolicyCreate(PolicyBase):
    """Schema for creating a policy"""
    pass


class PolicyUpdate(BaseSchema):
    """Schema for updating a policy"""
    policy_number: Optional[str] = Field(None, min_length=1, max_length=50)
    policy_type: Optional[PolicyType] = None
    status: Optional[PolicyStatus] = None
    premium_amount: Optional[Decimal] = Field(None, gt=0)
    coverage_amount: Optional[Decimal] = Field(None, gt=0)
    deductible: Optional[Decimal] = Field(None, ge=0)
    end_date: Optional[date] = None


class PolicyResponse(PolicyBase, ResponseSchema):
    """Schema for policy response"""
    renewal_date: Optional[date] = None


class PolicyInDB(PolicyResponse):
    """Schema for policy in database"""
    pass
