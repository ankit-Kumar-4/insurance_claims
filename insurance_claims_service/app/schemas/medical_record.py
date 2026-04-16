"""Medical Record schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.medical import RecordType


class MedicalRecordBase(BaseSchema):
    """Base medical record schema"""
    policy_id: int = Field(..., gt=0)
    record_type: RecordType
    record_date: date
    diagnosis: str = Field(..., min_length=1, max_length=500)
    treatment: Optional[str] = Field(None, max_length=1000)
    provider_name: str = Field(..., min_length=1, max_length=200)
    notes: Optional[str] = Field(None, max_length=2000)


class MedicalRecordCreate(MedicalRecordBase):
    """Schema for creating a medical record"""
    pass


class MedicalRecordUpdate(BaseSchema):
    """Schema for updating a medical record"""
    record_date: Optional[date] = None
    diagnosis: Optional[str] = Field(None, min_length=1, max_length=500)
    treatment: Optional[str] = Field(None, max_length=1000)
    provider_name: Optional[str] = Field(None, min_length=1, max_length=200)
    notes: Optional[str] = Field(None, max_length=2000)


class MedicalRecordResponse(MedicalRecordBase, ResponseSchema):
    """Schema for medical record response"""
    pass


class MedicalRecordInDB(MedicalRecordResponse):
    """Schema for medical record in database"""
    pass
