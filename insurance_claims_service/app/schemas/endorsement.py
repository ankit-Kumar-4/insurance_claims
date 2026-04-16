"""Endorsement schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.endorsement import EndorsementType, EndorsementStatus


class EndorsementBase(BaseSchema):
    """Base endorsement schema"""
    policy_id: int = Field(..., gt=0)
    endorsement_type: EndorsementType
    endorsement_number: str = Field(..., min_length=1, max_length=50)
    effective_date: date
    premium_change: Decimal = Field(default=0, decimal_places=2)
    status: EndorsementStatus = EndorsementStatus.PENDING
    description: str = Field(..., min_length=10, max_length=1000)


class EndorsementCreate(EndorsementBase):
    """Schema for creating an endorsement"""
    pass


class EndorsementUpdate(BaseSchema):
    """Schema for updating an endorsement"""
    effective_date: Optional[date] = None
    premium_change: Optional[Decimal] = Field(None, decimal_places=2)
    status: Optional[EndorsementStatus] = None
    description: Optional[str] = Field(None, min_length=10, max_length=1000)


class EndorsementResponse(EndorsementBase, ResponseSchema):
    """Schema for endorsement response"""
    approved_date: Optional[date] = None


class EndorsementInDB(EndorsementResponse):
    """Schema for endorsement in database"""
    pass
