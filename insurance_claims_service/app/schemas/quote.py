"""Quote schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.quote import QuoteStatus
from app.enums.policy import PolicyType


class QuoteBase(BaseSchema):
    """Base quote schema"""
    quote_number: str = Field(..., min_length=1, max_length=50)
    customer_id: int = Field(..., gt=0)
    policy_type: PolicyType
    coverage_amount: Decimal = Field(..., gt=0)
    annual_premium: Decimal = Field(..., gt=0)
    valid_until: date
    status: QuoteStatus = QuoteStatus.DRAFT


class QuoteCreate(QuoteBase):
    """Schema for creating a quote"""
    pass


class QuoteUpdate(BaseSchema):
    """Schema for updating a quote"""
    coverage_amount: Optional[Decimal] = Field(None, gt=0)
    annual_premium: Optional[Decimal] = Field(None, gt=0)
    valid_until: Optional[date] = None
    status: Optional[QuoteStatus] = None


class QuoteResponse(QuoteBase, ResponseSchema):
    """Schema for quote response"""
    pass


class QuoteInDB(QuoteResponse):
    """Schema for quote in database"""
    pass
