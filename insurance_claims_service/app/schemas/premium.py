"""Premium schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.policy import PremiumFrequency


class PremiumBase(BaseSchema):
    """Base premium schema"""
    policy_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0)
    due_date: date
    frequency: PremiumFrequency
    is_paid: bool = Field(default=False)


class PremiumCreate(PremiumBase):
    """Schema for creating a premium"""
    pass


class PremiumUpdate(BaseSchema):
    """Schema for updating a premium"""
    amount: Optional[Decimal] = Field(None, gt=0)
    due_date: Optional[date] = None
    is_paid: Optional[bool] = None
    paid_date: Optional[date] = None


class PremiumResponse(PremiumBase, ResponseSchema):
    """Schema for premium response"""
    paid_date: Optional[date] = None


class PremiumInDB(PremiumResponse):
    """Schema for premium in database"""
    pass
