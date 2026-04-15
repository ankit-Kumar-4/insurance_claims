"""Underwriter model for risk assessment professionals"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.common import Status


class Underwriter(BaseModel):
    """
    Underwriter model - professionals who evaluate risk and determine policy terms
    """
    
    __tablename__ = "underwriters"
    
    # Employee identification
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), nullable=False)
    
    # Professional information
    specialization = Column(String(100), nullable=True)  # life, health, property, casualty
    license_number = Column(String(100), unique=True, nullable=True, index=True)
    experience_years = Column(Integer, nullable=True)
    
    # Authorization levels
    risk_assessment_limit = Column(Numeric(15, 2), nullable=True)  # maximum policy value they can underwrite
    
    # Performance metrics
    policies_underwritten_count = Column(Integer, default=0, nullable=False)
    approval_rating = Column(Numeric(3, 2), nullable=True)  # 0.00 to 5.00
    
    # Organization information
    department = Column(String(100), nullable=True)
    supervisor_id = Column(Integer, ForeignKey("underwriters.id"), nullable=True)
    
    # Employment information
    status = Column(SQLEnum(Status), nullable=False, default=Status.ACTIVE, index=True)
    hire_date = Column(Date, nullable=True)
    
    # Relationships
    supervisor = relationship("Underwriter", remote_side=[BaseModel.id], foreign_keys=[supervisor_id])
    subordinates = relationship("Underwriter", back_populates="supervisor")
    risk_assessments = relationship("RiskAssessment", back_populates="underwriter")
    
    # Indexes
    __table_args__ = (
        Index('idx_underwriter_code', 'employee_code'),
        Index('idx_underwriter_email', 'email'),
        Index('idx_underwriter_license', 'license_number'),
        Index('idx_underwriter_status', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<Underwriter(id={self.id}, code={self.employee_code}, name={self.full_name})>"
    
    @property
    def full_name(self) -> str:
        """Return underwriter's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_senior(self) -> bool:
        """Check if underwriter is senior (5+ years experience)"""
        if self.experience_years:
            return self.experience_years >= 5
        return False
