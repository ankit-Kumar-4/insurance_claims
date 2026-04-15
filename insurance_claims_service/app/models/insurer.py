"""Insurer model for insurance provider organizations"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.common import Status


class Insurer(BaseModel):
    """
    Insurer model - represents insurance provider companies
    """
    
    __tablename__ = "insurers"
    
    # Company identification
    company_name = Column(String(255), nullable=False, index=True)
    registration_number = Column(String(100), unique=True, nullable=False, index=True)
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    
    # Contact information
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    website = Column(String(255), nullable=True)
    
    # Address (Foreign Key)
    headquarters_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    
    # Financial information
    financial_rating = Column(String(10), nullable=True)  # e.g., A++, A+, A, B++
    total_assets = Column(Numeric(20, 2), nullable=True)
    
    # Company information
    established_date = Column(Date, nullable=True)
    specializations = Column(Text, nullable=True)  # JSON or comma-separated list
    
    # Performance metrics
    claim_settlement_ratio = Column(Numeric(5, 2), nullable=True)  # percentage
    customer_service_rating = Column(Numeric(3, 2), nullable=True)  # 0.00 to 5.00
    
    # Status
    status = Column(SQLEnum(Status), nullable=False, default=Status.ACTIVE, index=True)
    
    # Relationships
    headquarters_address = relationship("Address", foreign_keys=[headquarters_address_id])
    policies = relationship("Policy", back_populates="insurer")
    
    # Indexes
    __table_args__ = (
        Index('idx_insurer_company_name', 'company_name'),
        Index('idx_insurer_registration', 'registration_number'),
        Index('idx_insurer_license', 'license_number'),
        Index('idx_insurer_status', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<Insurer(id={self.id}, company={self.company_name})>"
    
    @property
    def years_in_business(self) -> int:
        """Calculate years the company has been in business"""
        if self.established_date:
            from datetime import date
            today = date.today()
            return today.year - self.established_date.year
        return None
