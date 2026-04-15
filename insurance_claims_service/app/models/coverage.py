"""Coverage model for specific protection types within a policy"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Boolean, Index, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Coverage(BaseModel):
    """
    Coverage model - represents specific protections provided by a policy
    """
    
    __tablename__ = "coverages"
    
    # Coverage identification
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    
    # Coverage details
    coverage_type = Column(String(100), nullable=False, index=True)  # liability, collision, comprehensive, medical
    coverage_name = Column(String(200), nullable=False)
    coverage_description = Column(Text, nullable=True)
    
    # Financial limits
    coverage_limit = Column(Numeric(15, 2), nullable=False)  # maximum payout
    deductible = Column(Numeric(15, 2), nullable=True)
    coverage_amount = Column(Numeric(15, 2), nullable=False)  # insured amount
    
    # Coverage period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Terms and conditions
    exclusions = Column(Text, nullable=True)  # what's not covered
    conditions = Column(Text, nullable=True)  # conditions for coverage
    is_mandatory = Column(Boolean, default=False, nullable=False)
    
    # Premium allocation
    premium_portion = Column(Numeric(15, 2), nullable=True)  # portion of total premium for this coverage
    
    # Status
    status = Column(String(20), nullable=False, default="active", index=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="coverages")
    
    # Indexes
    __table_args__ = (
        Index('idx_coverage_policy', 'policy_id'),
        Index('idx_coverage_type', 'coverage_type'),
        Index('idx_coverage_status', 'status'),
        Index('idx_coverage_dates', 'start_date', 'end_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Coverage(id={self.id}, type={self.coverage_type}, policy_id={self.policy_id})>"
    
    @property
    def is_active(self) -> bool:
        """Check if coverage is currently active"""
        from datetime import date
        today = date.today()
        return self.status == "active" and self.start_date <= today <= self.end_date
