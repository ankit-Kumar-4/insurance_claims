"""User schemas for API validation and serialization"""

from typing import Optional
from pydantic import Field, EmailStr

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.user import UserRole, UserStatus


class UserBase(BaseSchema):
    """Base user schema"""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=20)
    role: UserRole = Field(..., description="User role")
    status: UserStatus = Field(default=UserStatus.ACTIVE)


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseSchema):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None


class UserResponse(UserBase, ResponseSchema):
    """Schema for user response"""
    is_active: bool
    
class UserInDB(UserResponse):
    """Schema for user in database"""
    hashed_password: str
