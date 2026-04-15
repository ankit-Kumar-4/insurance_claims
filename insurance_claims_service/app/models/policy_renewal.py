"""Policy Renewal model for policy renewals"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.renewal import RenewalType, RenewalStatus, CustomerAction


class PolicyRenewal(BaseModel):
    """
    Policy Renewal model - manages policy renewal workflow
    """
    
    __tablename__ = "policy_renewals"
    
    # Renewal identification
    renewal_number = Column(String(50), unique=True, nullable=False, index=True)
    renewal_type = Column(SQLEnum(RenewalType), nullable=False, index=True)
    
    # Related policies
    original_policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    renewed_policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    
    # Renewal dates
    renewal_initiation_date = Column(DateTime, nullable=False, index=True)
    renewal_due_date = Column(Date, nullable=False, index=True)
    renewal_completion_date = Column(DateTime, nullable=True)
    
    # Previous policy terms
    previous_premium = Column(Numeric(15, 2), nullable=False)
    previous_coverage_amount = Column(Numeric(15, 2), nullable=False)
    
    # New policy terms
    new_premium = Column(Numeric(15, 2), nullable=False)
    new_coverage_amount = Column(Numeric(15, 2), nullable=False)
    premium_change_percentage = Column(Numeric(5, 2), nullable=True)
    
    # Status
    status = Column(SQLEnum(RenewalStatus), nullable=False, default=RenewalStatus.PENDING, index=True)
    
    # Customer response
    customer_action = Column(SQLEnum(CustomerAction), nullable=True, index=True)
    customer_response_date = Column(DateTime, nullable=True)
    
    # Notification tracking
    notification_sent_date = Column(DateTime, nullable=True)
    reminder_count = Column(Integer, default=0, nullable=False)
    last_reminder_date = Column(DateTime, nullable=True)
    
    # Notes and reason
    notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    modification_requests = Column(Text, nullable=True)
    
    # Relationships
    original_policy = relationship("Policy", foreign_keys=[original_policy_id], back_populates="renewals")
    renewed_policy = relationship("Policy", foreign_keys=[renewed_policy_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_renewal_number', 'renewal_number'),
        Index('idx_renewal_original_policy', 'original_policy_id'),
        Index('idx_renewal_status', 'status'),
        Index('idx_renewal_type', 'renewal_type'),
        Index('idx_renewal_due_date', 'renewal_due_date'),
        Index('idx_renewal_customer_action', 'customer_action'),
    )
    
    def __repr__(self) -> str:
        return f"<PolicyRenewal(id={self.id}, number={self.renewal_number}, status={self.status})>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if renewal is overdue"""
        from datetime import date
        return self.status == RenewalStatus.PENDING and self.renewal_due_date < date.today()
    
    @property
    def days_until_due(self) -> int:
        """Calculate days until renewal is due"""
        from datetime import date
        return (self.renewal_due_date - date.today()).days
