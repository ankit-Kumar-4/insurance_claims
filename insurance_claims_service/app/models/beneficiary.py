"""Beneficiary model for policy benefit recipients"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.customer import IdentificationType
from app.enums.common import Status


class Beneficiary(BaseModel):
    """
    Beneficiary model - represents persons entitled to receive policy benefits
    """
    
    __tablename__ = "beneficiaries"
    
    # Policy relationship
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    
    # Beneficiary type
    beneficiary_type = Column(String(50), nullable=False)  # primary, contingent, tertiary
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    relationship_to_policyholder = Column(String(100), nullable=False)  # spouse, child, parent, etc.
    date_of_birth = Column(Date, nullable=True)
    
    # Benefit allocation
    percentage_share = Column(Numeric(5, 2), nullable=False)  # percentage of benefit (e.g., 50.00 for 50%)
    
    # Contact information
    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    
    # Address
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    
    # Identification
    identification_type = Column(SQLEnum(IdentificationType), nullable=True)
    identification_number = Column(String(100), nullable=True)
    
    # Status
    status = Column(SQLEnum(Status), nullable=False, default=Status.ACTIVE, index=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="beneficiaries")
    address = relationship("Address", foreign_keys=[address_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_beneficiary_policy', 'policy_id'),
        Index('idx_beneficiary_type', 'beneficiary_type'),
        Index('idx_beneficiary_status', 'status'),
        Index('idx_beneficiary_policy_type', 'policy_id', 'beneficiary_type'),
    )
    
    def __repr__(self) -> str:
        return f"<Beneficiary(id={self.id}, name={self.full_name}, policy_id={self.policy_id})>"
    
    @property
    def full_name(self) -> str:
        """Return beneficiary's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calculate beneficiary's age"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
