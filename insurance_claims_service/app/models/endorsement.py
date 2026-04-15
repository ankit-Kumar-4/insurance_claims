"""Endorsement model for policy modifications"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.endorsement import EndorsementType, EndorsementStatus, RequestedBy


class Endorsement(BaseModel):
    """
    Endorsement model - represents policy modifications and amendments
    """
    
    __tablename__ = "endorsements"
    
    # Endorsement identification
    endorsement_number = Column(String(50), unique=True, nullable=False, index=True)
    endorsement_type = Column(SQLEnum(EndorsementType), nullable=False, index=True)
    
    # Related policy
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    
    # Request details
    requested_by = Column(SQLEnum(RequestedBy), nullable=False, index=True)
    requested_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    request_date = Column(DateTime, nullable=False, index=True)
    
    # Effective dates
    effective_date = Column(Date, nullable=False, index=True)
    expiry_date = Column(Date, nullable=True)
    
    # Status
    status = Column(SQLEnum(EndorsementStatus), nullable=False, default=EndorsementStatus.REQUESTED, index=True)
    
    # Approval details
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_date = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Changes
    change_description = Column(Text, nullable=False)
    previous_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    
    # Financial impact
    premium_adjustment = Column(Numeric(15, 2), nullable=True)  # positive or negative
    coverage_adjustment = Column(Numeric(15, 2), nullable=True)
    
    # Implementation
    implementation_date = Column(DateTime, nullable=True)
    implemented_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="endorsements")
    requested_by_user = relationship("User", foreign_keys=[requested_by_user_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    implemented_by = relationship("User", foreign_keys=[implemented_by_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_endorsement_number', 'endorsement_number'),
        Index('idx_endorsement_policy', 'policy_id'),
        Index('idx_endorsement_type', 'endorsement_type'),
        Index('idx_endorsement_status', 'status'),
        Index('idx_endorsement_requested_by', 'requested_by'),
        Index('idx_endorsement_effective_date', 'effective_date'),
        Index('idx_endorsement_request_date', 'request_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Endorsement(id={self.id}, number={self.endorsement_number}, type={self.endorsement_type})>"
    
    @property
    def is_active(self) -> bool:
        """Check if endorsement is active"""
        from datetime import date
        today = date.today()
        is_effective = self.effective_date <= today
        not_expired = not self.expiry_date or self.expiry_date >= today
        return self.status == EndorsementStatus.IMPLEMENTED and is_effective and not_expired
