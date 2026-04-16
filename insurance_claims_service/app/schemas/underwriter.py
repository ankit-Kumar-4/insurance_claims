"""Underwriter schemas for API validation and serialization"""

from typing import Optional
from pydantic import Field, EmailStr

from app.schemas.base import BaseSchema, ResponseSchema


class UnderwriterBase(BaseSchema):
    """Base underwriter schema"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    license_number: str = Field(..., min_length=1, max_length=50)
    specialization: Optional[str] = Field(None, max_length=100)
    is_active: bool = Field(default=True)


class UnderwriterCreate(UnderwriterBase):
    """Schema for creating an underwriter"""
    pass


class UnderwriterUpdate(BaseSchema):
    """Schema for updating an underwriter"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    license_number: Optional[str] = Field(None, min_length=1, max_length=50)
    specialization: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class UnderwriterResponse(UnderwriterBase, ResponseSchema):
    """Schema for underwriter response"""
    pass


class UnderwriterInDB(UnderwriterResponse):
    """Schema for underwriter in database"""
    pass
