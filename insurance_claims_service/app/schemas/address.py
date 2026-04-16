"""Address schemas for API validation and serialization"""

from typing import Optional
from decimal import Decimal
from pydantic import Field, field_validator

from app.schemas.base import BaseSchema, ResponseSchema


class AddressBase(BaseSchema):
    """Base address schema with common fields"""
    street_address: str = Field(..., min_length=1, max_length=255, description="Street address")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    state: str = Field(..., min_length=2, max_length=100, description="State or province")
    postal_code: str = Field(..., min_length=1, max_length=20, description="Postal or ZIP code")
    country: str = Field(default="USA", min_length=2, max_length=100, description="Country name")
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    
    @field_validator('postal_code')
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        """Validate and normalize postal code"""
        return v.strip().upper()
    
    @field_validator('state', 'city')
    @classmethod
    def capitalize_location(cls, v: str) -> str:
        """Capitalize location names"""
        return v.strip().title()


class AddressCreate(AddressBase):
    """Schema for creating a new address"""
    pass


class AddressUpdate(BaseSchema):
    """Schema for updating an address"""
    street_address: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)


class AddressResponse(AddressBase, ResponseSchema):
    """Schema for address response"""
    pass


class AddressInDB(AddressResponse):
    """Schema for address as stored in database"""
    pass
