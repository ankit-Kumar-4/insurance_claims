"""Vehicle schemas for API validation and serialization"""

from typing import Optional
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.vehicle import VehicleType, VehicleCondition


class VehicleBase(BaseSchema):
    """Base vehicle schema"""
    policy_id: int = Field(..., gt=0)
    make: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    vin: str = Field(..., min_length=17, max_length=17)
    vehicle_type: VehicleType
    condition: VehicleCondition
    mileage: Optional[int] = Field(None, ge=0)


class VehicleCreate(VehicleBase):
    """Schema for creating a vehicle"""
    pass


class VehicleUpdate(BaseSchema):
    """Schema for updating a vehicle"""
    make: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    condition: Optional[VehicleCondition] = None
    mileage: Optional[int] = Field(None, ge=0)


class VehicleResponse(VehicleBase, ResponseSchema):
    """Schema for vehicle response"""
    pass


class VehicleInDB(VehicleResponse):
    """Schema for vehicle in database"""
    pass
