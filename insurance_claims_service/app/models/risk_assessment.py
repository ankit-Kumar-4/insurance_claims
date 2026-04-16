"""Risk Assessment model for evaluating policy and claim risks"""

from sqlalchemy import Boolean, Column, String, Integer, Date, ForeignKey, Numeric, Index, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class RiskAssessment(BaseModel):
    """
    Risk Assessment model - evaluates risk for policies and claims
    """
    
    __tablename__ = "risk_assessments"
    
    # Related entities
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True, index=True)
    assessed_by_id = Column(Integer, ForeignKey("underwriters.id"), nullable=False, index=True)
    
    # Assessment type
    assessment_type = Column(String(50), nullable=False, index=True)  # initial, renewal, claim, modification
    
    # Risk scores (0-100 scale)
    overall_risk_score = Column(Numeric(5, 2), nullable=False, index=True)  # 0.00 to 100.00
    financial_risk_score = Column(Numeric(5, 2), nullable=True)
    health_risk_score = Column(Numeric(5, 2), nullable=True)
    behavior_risk_score = Column(Numeric(5, 2), nullable=True)
    
    # Risk factors
    risk_factors = Column(Text, nullable=True)  # JSON or comma-separated list
    
    # Assessment details
    assessment_date = Column(Date, nullable=False, index=True)
    assessment_notes = Column(Text, nullable=True)
    
    # Recommendations
    recommended_premium_adjustment = Column(Numeric(5, 2), nullable=True)  # percentage
    recommended_coverage_limit = Column(Numeric(15, 2), nullable=True)
    recommendations = Column(Text, nullable=True)
    
    # Approval
    is_approved = Column(Boolean, default=False, nullable=False)
    approval_date = Column(Date, nullable=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="risk_assessments")
    customer = relationship("Customer", foreign_keys=[customer_id])
    underwriter = relationship("Underwriter", back_populates="risk_assessments")
    
    # Indexes
    __table_args__ = (
        Index('idx_risk_assessment_policy', 'policy_id'),
        Index('idx_risk_assessment_customer', 'customer_id'),
        Index('idx_risk_assessment_underwriter', 'assessed_by_id'),
        Index('idx_risk_assessment_type', 'assessment_type'),
        Index('idx_risk_assessment_score', 'overall_risk_score'),
        Index('idx_risk_assessment_date', 'assessment_date'),
    )
    
    def __repr__(self) -> str:
        return f"<RiskAssessment(id={self.id}, score={self.overall_risk_score}, policy_id={self.policy_id})>"
    
    @property
    def risk_level(self) -> str:
        """Determine risk level based on score"""
        if self.overall_risk_score <= 25:
            return "low"
        elif self.overall_risk_score <= 50:
            return "medium"
        elif self.overall_risk_score <= 75:
            return "high"
        else:
            return "very_high"
