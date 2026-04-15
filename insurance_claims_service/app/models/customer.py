"""Customer model for policyholders"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Enum as SQLEnum, Text, Numeric, Index
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.customer import CustomerType, RiskProfile, CustomerStatus, IdentificationType
from app.enums.common import Gender


class Customer(BaseModel):
    """
    Customer model - represents individuals or organizations purchasing insurance
    """
    
    __tablename__ = "customers"
    
    # Customer identification
    customer_type = Column(SQLEnum(CustomerType), nullable=False, default=CustomerType.INDIVIDUAL, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(SQLEnum(Gender), nullable=True)
    
    # Contact information
    email = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    alternate_phone = Column(String(20), nullable=True)
    
    # Professional information
    occupation = Column(String(100), nullable=True)
    annual_income = Column(Numeric(15, 2), nullable=True)
    
    # Address (Foreign Key)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    
    # Identification
    identification_type = Column(SQLEnum(IdentificationType), nullable=True)
    identification_number = Column(String(100), nullable=True, index=True)
    
    # Risk assessment
    risk_profile = Column(SQLEnum(RiskProfile), nullable=False, default=RiskProfile.MEDIUM, index=True)
    
    # Account information
    customer_since = Column(DateTime, nullable=True)
    status = Column(SQLEnum(CustomerStatus), nullable=False, default=CustomerStatus.ACTIVE, index=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    
    # Relationships
    address = relationship("Address", foreign_keys=[address_id])
    policies = relationship("Policy", back_populates="customer", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="claimant")
    quotes = relationship("Quote", back_populates="customer")
    medical_records = relationship("MedicalRecord", back_populates="customer")
    
    # Indexes
    __table_args__ = (
        Index('idx_customer_email', 'email'),
        Index('idx_customer_type_status', 'customer_type', 'status'),
        Index('idx_customer_risk_profile', 'risk_profile'),
        Index('idx_customer_identification', 'identification_type', 'identification_number'),
    )
    
    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, name={self.full_name}, type={self.customer_type})>"
    
    @property
    def full_name(self) -> str:
        """Return customer's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> int:
        """Calculate customer's age"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
