"""Incident schemas for API validation and serialization"""

from typing import Optional
from datetime import date
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.incident import IncidentType, IncidentSeverity


class IncidentBase(BaseSchema):
    """Base incident schema"""
    claim_id: int = Field(..., gt=0)
    incident_type: IncidentType
    incident_date: date
    location: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10, max_length=2000)
    severity: IncidentSeverity
    police_report_number: Optional[str] = Field(None, max_length=100)


class IncidentCreate(IncidentBase):
    """Schema for creating an incident"""
    pass


class IncidentUpdate(BaseSchema):
    """Schema for updating an incident"""
    incident_date: Optional[date] = None
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    severity: Optional[IncidentSeverity] = None
    police_report_number: Optional[str] = Field(None, max_length=100)


class IncidentResponse(IncidentBase, ResponseSchema):
    """Schema for incident response"""
    pass


class IncidentInDB(IncidentResponse):
    """Schema for incident in database"""
    pass
