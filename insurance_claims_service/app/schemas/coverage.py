"""Coverage schemas for API validation and serialization"""

from typing import Optional
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema


class CoverageBase(BaseSchema):
    """Base coverage schema"""
    policy_id: int = Field(..., gt=0)
    coverage_type: str = Field(..., min_length=1, max_length=100)
    coverage_amount: Decimal = Field(..., gt=0)
    deductible: Decimal = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)


class CoverageCreate(CoverageBase):
    """Schema for creating a coverage"""
    pass


class CoverageUpdate(BaseSchema):
    """Schema for updating a coverage"""
    coverage_type: Optional[str] = Field(None, min_length=1, max_length=100)
    coverage_amount: Optional[Decimal] = Field(None, gt=0)
    deductible: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)


class CoverageResponse(CoverageBase, ResponseSchema):
    """Schema for coverage response"""
    pass


class CoverageInDB(CoverageResponse):
    """Schema for coverage in database"""
    pass
