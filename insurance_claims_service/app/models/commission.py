"""Commission model for agent compensation"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.commission import CommissionType, CommissionPaymentStatus


class Commission(BaseModel):
    """
    Commission model - tracks agent commissions and compensation
    """
    
    __tablename__ = "commissions"
    
    # Commission identification
    commission_number = Column(String(50), unique=True, nullable=False, index=True)
    commission_type = Column(SQLEnum(CommissionType), nullable=False, index=True)
    
    # Related entities
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    
    # Commission calculation
    commission_rate = Column(Numeric(5, 2), nullable=False)  # percentage
    base_amount = Column(Numeric(15, 2), nullable=False)  # amount commission is calculated on
    commission_amount = Column(Numeric(15, 2), nullable=False)
    
    # Payment details
    payment_status = Column(
        SQLEnum(CommissionPaymentStatus), 
        nullable=False, 
        default=CommissionPaymentStatus.PENDING,
        index=True
    )
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String(50), nullable=True)
    transaction_reference = Column(String(255), nullable=True)
    
    # Period
    commission_period_start = Column(Date, nullable=False, index=True)
    commission_period_end = Column(Date, nullable=False)
    earned_date = Column(Date, nullable=False, index=True)
    
    # Additional details
    notes = Column(Text, nullable=True)
    dispute_reason = Column(Text, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="commissions")
    policy = relationship("Policy", foreign_keys=[policy_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_commission_number', 'commission_number'),
        Index('idx_commission_agent', 'agent_id'),
        Index('idx_commission_policy', 'policy_id'),
        Index('idx_commission_type', 'commission_type'),
        Index('idx_commission_status', 'payment_status'),
        Index('idx_commission_earned_date', 'earned_date'),
        Index('idx_commission_period', 'commission_period_start', 'commission_period_end'),
    )
    
    def __repr__(self) -> str:
        return f"<Commission(id={self.id}, number={self.commission_number}, amount={self.commission_amount})>"
    
    @property
    def is_paid(self) -> bool:
        """Check if commission has been paid"""
        return self.payment_status == CommissionPaymentStatus.PAID
