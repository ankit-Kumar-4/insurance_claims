"""Insurer schemas for API validation and serialization"""

from typing import Optional
from pydantic import Field, EmailStr

from app.schemas.base import BaseSchema, ResponseSchema


class InsurerBase(BaseSchema):
    """Base insurer schema"""
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    license_number: str = Field(..., min_length=1, max_length=50)
    is_active: bool = Field(default=True)


class InsurerCreate(InsurerBase):
    """Schema for creating an insurer"""
    pass


class InsurerUpdate(BaseSchema):
    """Schema for updating an insurer"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    license_number: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None


class InsurerResponse(InsurerBase, ResponseSchema):
    """Schema for insurer response"""
    pass


class InsurerInDB(InsurerResponse):
    """Schema for insurer in database"""
    pass
