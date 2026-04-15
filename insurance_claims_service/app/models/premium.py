"""Premium model for insurance payment tracking"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.payment import PaymentStatus
from app.enums.policy import PremiumFrequency


class Premium(BaseModel):
    """
    Premium model - represents payment for insurance coverage
    """
    
    __tablename__ = "premiums"
    
    # Related policy
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    
    # Premium details
    premium_amount = Column(Numeric(15, 2), nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    payment_date = Column(Date, nullable=True)
    
    # Payment status
    payment_status = Column(SQLEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING, index=True)
    payment_method_id = Column(Integer, nullable=True)  # FK to payment method table
    
    # Fees and discounts
    late_fee = Column(Numeric(10, 2), nullable=True, default=0)
    discount_applied = Column(Boolean, default=False, nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=True, default=0)
    net_amount = Column(Numeric(15, 2), nullable=False)
    
    # Payment frequency
    payment_frequency = Column(SQLEnum(PremiumFrequency), nullable=False)
    
    # Grace period
    grace_period_end_date = Column(Date, nullable=True)
    
    # Receipt
    receipt_number = Column(String(100), unique=True, nullable=True, index=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="premiums")
    
    # Indexes
    __table_args__ = (
        Index('idx_premium_policy', 'policy_id'),
        Index('idx_premium_due_date', 'due_date'),
        Index('idx_premium_status', 'payment_status'),
        Index('idx_premium_receipt', 'receipt_number'),
        Index('idx_premium_policy_status', 'policy_id', 'payment_status'),
    )
    
    def __repr__(self) -> str:
        return f"<Premium(id={self.id}, policy_id={self.policy_id}, amount={self.premium_amount})>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if premium is overdue"""
        from datetime import date
        if self.payment_status == PaymentStatus.PENDING:
            grace_date = self.grace_period_end_date or self.due_date
            return date.today() > grace_date
        return False
    
    @property
    def days_overdue(self) -> int:
        """Calculate days overdue"""
        from datetime import date
        if self.is_overdue:
            grace_date = self.grace_period_end_date or self.due_date
            return (date.today() - grace_date).days
        return 0
