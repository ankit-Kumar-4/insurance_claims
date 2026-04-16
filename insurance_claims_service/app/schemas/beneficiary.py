"""Beneficiary schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.common import Gender, RelationshipType


class BeneficiaryBase(BaseSchema):
    """Base beneficiary schema"""
    policy_id: int = Field(..., gt=0)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    relationship: RelationshipType
    date_of_birth: date
    gender: Gender
    percentage_share: int = Field(..., ge=0, le=100)


class BeneficiaryCreate(BeneficiaryBase):
    """Schema for creating a beneficiary"""
    pass


class BeneficiaryUpdate(BaseSchema):
    """Schema for updating a beneficiary"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    relationship: Optional[RelationshipType] = None
    percentage_share: Optional[int] = Field(None, ge=0, le=100)


class BeneficiaryResponse(BeneficiaryBase, ResponseSchema):
    """Schema for beneficiary response"""
    pass


class BeneficiaryInDB(BeneficiaryResponse):
    """Schema for beneficiary in database"""
    pass
