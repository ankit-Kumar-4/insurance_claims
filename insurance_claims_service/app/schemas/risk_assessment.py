"""Risk Assessment schemas for API validation and serialization"""

from typing import Optional
from decimal import Decimal
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema


class RiskAssessmentBase(BaseSchema):
    """Base risk assessment schema"""
    policy_id: int = Field(..., gt=0)
    risk_score: int = Field(..., ge=0, le=100)
    risk_factors: str = Field(..., min_length=10, max_length=2000)
    assessment_notes: Optional[str] = Field(None, max_length=2000)
    recommended_premium: Decimal = Field(..., gt=0)


class RiskAssessmentCreate(RiskAssessmentBase):
    """Schema for creating a risk assessment"""
    pass


class RiskAssessmentUpdate(BaseSchema):
    """Schema for updating a risk assessment"""
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    risk_factors: Optional[str] = Field(None, min_length=10, max_length=2000)
    assessment_notes: Optional[str] = Field(None, max_length=2000)
    recommended_premium: Optional[Decimal] = Field(None, gt=0)


class RiskAssessmentResponse(RiskAssessmentBase, ResponseSchema):
    """Schema for risk assessment response"""
    pass


class RiskAssessmentInDB(RiskAssessmentResponse):
    """Schema for risk assessment in database"""
    pass
