"""Property schemas for API validation and serialization"""

from typing import Optional
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.property import PropertyType, PropertyCondition


class PropertyBase(BaseSchema):
    """Base property schema"""
    policy_id: int = Field(..., gt=0)
    property_type: PropertyType
    address_id: int = Field(..., gt=0)
    square_feet: int = Field(..., gt=0)
    year_built: int = Field(..., ge=1800, le=2100)
    condition: PropertyCondition
    market_value: Decimal = Field(..., gt=0, decimal_places=2)


class PropertyCreate(PropertyBase):
    """Schema for creating a property"""
    pass


class PropertyUpdate(BaseSchema):
    """Schema for updating a property"""
    square_feet: Optional[int] = Field(None, gt=0)
    condition: Optional[PropertyCondition] = None
    market_value: Optional[Decimal] = Field(None, gt=0, decimal_places=2)


class PropertyResponse(PropertyBase, ResponseSchema):
    """Schema for property response"""
    pass


class PropertyInDB(PropertyResponse):
    """Schema for property in database"""
    pass
