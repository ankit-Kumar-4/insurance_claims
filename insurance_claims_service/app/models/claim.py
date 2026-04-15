"""Claim model for insurance compensation requests"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.claim import ClaimType, ClaimStatus


class Claim(BaseModel):
    """
    Claim model - represents a request for compensation under a policy
    """
    
    __tablename__ = "claims"
    
    # Claim identification
    claim_number = Column(String(50), unique=True, nullable=False, index=True)
    claim_type = Column(SQLEnum(ClaimType), nullable=False, index=True)
    
    # Relationships
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    claimant_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    assigned_adjuster_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # Claim dates
    claim_date = Column(DateTime, nullable=False, index=True)
    incident_date = Column(DateTime, nullable=False, index=True)
    settlement_date = Column(Date, nullable=True)
    payment_date = Column(Date, nullable=True)
    
    # Claim amounts
    claim_amount = Column(Numeric(15, 2), nullable=False)
    approved_amount = Column(Numeric(15, 2), nullable=True)
    
    # Status
    status = Column(SQLEnum(ClaimStatus), nullable=False, default=ClaimStatus.SUBMITTED, index=True)
    
    # Description and reasoning
    description = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="claims")
    claimant = relationship("Customer", back_populates="claims")
    assigned_adjuster = relationship("User", foreign_keys=[assigned_adjuster_id])
    
    documents = relationship("Document", back_populates="claim", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="claim")
    payments = relationship("Payment", back_populates="claim")
    
    # Indexes for performance (claims table will be high-volume)
    __table_args__ = (
        Index('idx_claim_number', 'claim_number'),
        Index('idx_claim_policy', 'policy_id'),
        Index('idx_claim_claimant', 'claimant_id'),
        Index('idx_claim_status', 'status'),
        Index('idx_claim_type_status', 'claim_type', 'status'),
        Index('idx_claim_dates', 'claim_date', 'incident_date'),
        Index('idx_claim_adjuster', 'assigned_adjuster_id'),
    )
    
    def __repr__(self) -> str:
        return f"<Claim(id={self.id}, number={self.claim_number}, status={self.status})>"
    
    @property
    def is_pending(self) -> bool:
        """Check if claim is pending review"""
        return self.status in [ClaimStatus.SUBMITTED, ClaimStatus.UNDER_REVIEW, ClaimStatus.PENDING_DOCUMENTS]
    
    @property
    def is_resolved(self) -> bool:
        """Check if claim has been resolved"""
        return self.status in [ClaimStatus.APPROVED, ClaimStatus.REJECTED, ClaimStatus.SETTLED, ClaimStatus.CLOSED]
    
    @property
    def processing_days(self) -> int:
        """Calculate days since claim was filed"""
        from datetime import datetime
        return (datetime.utcnow() - self.claim_date).days
