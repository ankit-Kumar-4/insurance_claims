"""Customer schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from pydantic import Field, EmailStr

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.customer import CustomerType, RiskProfile, CustomerStatus
from app.enums.common import Gender


class CustomerBase(BaseSchema):
    """Base customer schema"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    date_of_birth: date
    gender: Gender
    customer_type: CustomerType
    risk_profile: RiskProfile = RiskProfile.MEDIUM
    status: CustomerStatus = CustomerStatus.ACTIVE


class CustomerCreate(CustomerBase):
    """Schema for creating a customer"""
    address_id: Optional[int] = Field(None, gt=0)


class CustomerUpdate(BaseSchema):
    """Schema for updating a customer"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    gender: Optional[Gender] = None
    customer_type: Optional[CustomerType] = None
    risk_profile: Optional[RiskProfile] = None
    status: Optional[CustomerStatus] = None


class CustomerResponse(CustomerBase, ResponseSchema):
    """Schema for customer response"""
    address_id: Optional[int] = None


class CustomerInDB(CustomerResponse):
    """Schema for customer in database"""
    pass
