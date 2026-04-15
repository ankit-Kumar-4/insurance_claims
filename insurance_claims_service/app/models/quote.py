"""Quote model for insurance quotations"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.quote import QuoteStatus
from app.enums.policy import PolicyType


class Quote(BaseModel):
    """
    Quote model - represents insurance quote requests before policy creation
    """
    
    __tablename__ = "quotes"
    
    # Quote identification
    quote_number = Column(String(50), unique=True, nullable=False, index=True)
    policy_type = Column(SQLEnum(PolicyType), nullable=False, index=True)
    
    # Related entities
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True, index=True)
    
    # Quote dates
    quote_date = Column(DateTime, nullable=False, index=True)
    expiry_date = Column(Date, nullable=False, index=True)
    
    # Coverage details
    coverage_amount = Column(Numeric(15, 2), nullable=False)
    deductible = Column(Numeric(15, 2), nullable=True)
    
    # Premium calculation
    quoted_premium = Column(Numeric(15, 2), nullable=False)
    discount_applied = Column(Numeric(5, 2), nullable=True)  # percentage
    final_premium = Column(Numeric(15, 2), nullable=False)
    
    # Status
    status = Column(SQLEnum(QuoteStatus), nullable=False, default=QuoteStatus.DRAFT, index=True)
    
    # Customer response
    customer_response_date = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Policy conversion
    converted_policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    conversion_date = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="quotes")
    agent = relationship("Agent", back_populates="quotes")
    converted_policy = relationship("Policy", foreign_keys=[converted_policy_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_quote_number', 'quote_number'),
        Index('idx_quote_customer', 'customer_id'),
        Index('idx_quote_agent', 'agent_id'),
        Index('idx_quote_status', 'status'),
        Index('idx_quote_type', 'policy_type'),
        Index('idx_quote_date', 'quote_date'),
        Index('idx_quote_expiry', 'expiry_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Quote(id={self.id}, number={self.quote_number}, status={self.status})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if quote has expired"""
        from datetime import date
        return self.expiry_date < date.today()
    
    @property
    def days_until_expiry(self) -> int:
        """Calculate days until quote expires"""
        from datetime import date
        return (self.expiry_date - date.today()).days
