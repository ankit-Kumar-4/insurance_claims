"""Commission schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.commission import CommissionType, CommissionStatus


class CommissionBase(BaseSchema):
    """Base commission schema"""
    agent_id: int = Field(..., gt=0)
    policy_id: int = Field(..., gt=0)
    commission_type: CommissionType
    amount: Decimal = Field(..., gt=0)
    rate: Decimal = Field(..., ge=0, le=100)
    status: CommissionStatus = CommissionStatus.PENDING


class CommissionCreate(CommissionBase):
    """Schema for creating a commission"""
    pass


class CommissionUpdate(BaseSchema):
    """Schema for updating a commission"""
    amount: Optional[Decimal] = Field(None, gt=0)
    status: Optional[CommissionStatus] = None
    paid_date: Optional[date] = None


class CommissionResponse(CommissionBase, ResponseSchema):
    """Schema for commission response"""
    paid_date: Optional[date] = None


class CommissionInDB(CommissionResponse):
    """Schema for commission in database"""
    pass
