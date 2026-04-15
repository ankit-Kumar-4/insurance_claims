"""Policy model - core insurance contract entity"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.policy import PolicyType, PolicyStatus, PremiumFrequency


class Policy(BaseModel):
    """
    Policy model - represents the core insurance contract
    """
    
    __tablename__ = "policies"
    
    # Policy identification
    policy_number = Column(String(50), unique=True, nullable=False, index=True)
    policy_type = Column(SQLEnum(PolicyType), nullable=False, index=True)
    
    # Relationships (Foreign Keys)
    policy_holder_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    insurer_id = Column(Integer, ForeignKey("insurers.id"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True, index=True)
    
    # Policy period
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    renewal_date = Column(Date, nullable=True)
    
    # Status
    status = Column(SQLEnum(PolicyStatus), nullable=False, default=PolicyStatus.PENDING, index=True)
    
    # Financial details
    premium_amount = Column(Numeric(15, 2), nullable=False)
    premium_frequency = Column(SQLEnum(PremiumFrequency), nullable=False, default=PremiumFrequency.MONTHLY)
    coverage_amount = Column(Numeric(15, 2), nullable=False)
    deductible = Column(Numeric(15, 2), nullable=True)
    
    # Terms
    terms_and_conditions = Column(Text, nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="policies")
    insurer = relationship("Insurer", back_populates="policies")
    agent = relationship("Agent", back_populates="policies")
    
    claims = relationship("Claim", back_populates="policy", cascade="all, delete-orphan")
    premiums = relationship("Premium", back_populates="policy", cascade="all, delete-orphan")
    coverages = relationship("Coverage", back_populates="policy", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="policy", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="policy")
    vehicles = relationship("Vehicle", back_populates="policy")
    properties = relationship("Property", back_populates="policy")
    endorsements = relationship("Endorsement", back_populates="policy")
    renewals = relationship("PolicyRenewal", back_populates="original_policy", foreign_keys="PolicyRenewal.original_policy_id")
    
    # Indexes
    __table_args__ = (
        Index('idx_policy_number', 'policy_number'),
        Index('idx_policy_holder', 'policy_holder_id'),
        Index('idx_policy_type_status', 'policy_type', 'status'),
        Index('idx_policy_dates', 'start_date', 'end_date'),
        Index('idx_policy_agent', 'agent_id'),
    )
    
    def __repr__(self) -> str:
        return f"<Policy(id={self.id}, number={self.policy_number}, type={self.policy_type})>"
    
    @property
    def is_active(self) -> bool:
        """Check if policy is currently active"""
        return self.status == PolicyStatus.ACTIVE
    
    @property
    def is_expired(self) -> bool:
        """Check if policy has expired"""
        from datetime import date
        return self.end_date < date.today()
    
    @property
    def days_until_expiry(self) -> int:
        """Calculate days until policy expires"""
        from datetime import date
        if self.end_date:
            return (self.end_date - date.today()).days
        return None
