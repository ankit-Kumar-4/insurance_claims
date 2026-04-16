"""Agent schemas for API validation and serialization"""

from typing import Optional
from decimal import Decimal
from pydantic import Field, EmailStr

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.common import Gender


class AgentBase(BaseSchema):
    """Base agent schema"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    license_number: str = Field(..., min_length=1, max_length=50)
    commission_rate: Decimal = Field(..., ge=0, le=100, decimal_places=2, description="Commission percentage")
    is_active: bool = Field(default=True)


class AgentCreate(AgentBase):
    """Schema for creating an agent"""
    pass


class AgentUpdate(BaseSchema):
    """Schema for updating an agent"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    license_number: Optional[str] = Field(None, min_length=1, max_length=50)
    commission_rate: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    is_active: Optional[bool] = None


class AgentResponse(AgentBase, ResponseSchema):
    """Schema for agent response"""
    total_sales: Optional[Decimal] = None
    total_commission: Optional[Decimal] = None


class AgentInDB(AgentResponse):
    """Schema for agent in database"""
    pass
