"""Payment schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.payment import PaymentMethod, PaymentStatus, PaymentType


class PaymentBase(BaseSchema):
    """Base payment schema"""
    payment_type: PaymentType
    policy_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    payment_method: PaymentMethod
    payment_date: date
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = Field(None, max_length=100)
    reference_number: Optional[str] = Field(None, max_length=100)


class PaymentCreate(PaymentBase):
    """Schema for creating a payment"""
    pass


class PaymentUpdate(BaseSchema):
    """Schema for updating a payment"""
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = Field(None, max_length=100)
    reference_number: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class PaymentResponse(PaymentBase, ResponseSchema):
    """Schema for payment response"""
    processed_date: Optional[date] = None
    notes: Optional[str] = None


class PaymentInDB(PaymentResponse):
    """Schema for payment in database"""
    pass
