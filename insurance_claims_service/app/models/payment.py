"""Payment model for tracking all financial transactions"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.payment import PaymentType, PaymentMethod, PaymentStatus


class Payment(BaseModel):
    """
    Payment model - tracks all financial transactions in the system
    """
    
    __tablename__ = "payments"
    
    # Payment identification
    payment_number = Column(String(50), unique=True, nullable=False, index=True)
    payment_type = Column(SQLEnum(PaymentType), nullable=False, index=True)
    
    # Related entities
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    
    # Payment details
    amount = Column(Numeric(15, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False, index=True)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False, index=True)
    
    # Status
    status = Column(SQLEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING, index=True)
    
    # Transaction details
    transaction_id = Column(String(255), unique=True, nullable=True, index=True)
    reference_number = Column(String(100), nullable=True)
    
    # Payment gateway
    gateway_name = Column(String(100), nullable=True)  # stripe, paypal, etc.
    gateway_response = Column(Text, nullable=True)  # JSON response
    
    # Dates
    due_date = Column(Date, nullable=True)
    processed_date = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Relationships
    policy = relationship("Policy", foreign_keys=[policy_id])
    claim = relationship("Claim", back_populates="payments", foreign_keys=[claim_id])
    customer = relationship("Customer", foreign_keys=[customer_id])
    
    # Indexes for high-volume table
    __table_args__ = (
        Index('idx_payment_number', 'payment_number'),
        Index('idx_payment_type_status', 'payment_type', 'status'),
        Index('idx_payment_date', 'payment_date'),
        Index('idx_payment_policy', 'policy_id'),
        Index('idx_payment_claim', 'claim_id'),
        Index('idx_payment_customer', 'customer_id'),
        Index('idx_payment_transaction', 'transaction_id'),
        Index('idx_payment_method', 'payment_method'),
    )
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, number={self.payment_number}, amount={self.amount})>"
    
    @property
    def is_successful(self) -> bool:
        """Check if payment was successful"""
        return self.status == PaymentStatus.COMPLETED
    
    @property
    def is_pending(self) -> bool:
        """Check if payment is pending"""
        return self.status in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]
