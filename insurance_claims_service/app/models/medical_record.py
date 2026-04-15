"""Medical Record model for health insurance"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Index, Enum as SQLEnum, Text, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.medical import MedicalRecordType, SmokingStatus, AlcoholConsumption


class MedicalRecord(BaseModel):
    """
    Medical Record model - stores health information for insurance purposes
    """
    
    __tablename__ = "medical_records"
    
    # Record identification
    record_type = Column(SQLEnum(MedicalRecordType), nullable=False, index=True)
    
    # Patient information
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    
    # Record date
    record_date = Column(Date, nullable=False, index=True)
    
    # Medical details
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    
    # Provider information
    healthcare_provider = Column(String(255), nullable=True)
    hospital_name = Column(String(255), nullable=True)
    doctor_name = Column(String(255), nullable=True)
    
    # Lifestyle factors
    height = Column(String(20), nullable=True)  # e.g., "5'10\""
    weight = Column(String(20), nullable=True)  # e.g., "150 lbs"
    blood_pressure = Column(String(20), nullable=True)  # e.g., "120/80"
    smoking_status = Column(SQLEnum(SmokingStatus), nullable=True, index=True)
    alcohol_consumption = Column(SQLEnum(AlcoholConsumption), nullable=True)
    
    # Pre-existing conditions
    has_chronic_conditions = Column(Boolean, default=False, nullable=False)
    chronic_conditions = Column(Text, nullable=True)
    
    # Allergies
    has_allergies = Column(Boolean, default=False, nullable=False)
    allergies = Column(Text, nullable=True)
    
    # Previous surgeries
    has_previous_surgeries = Column(Boolean, default=False, nullable=False)
    previous_surgeries = Column(Text, nullable=True)
    
    # Related policy
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    
    # Verification
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_date = Column(Date, nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="medical_records")
    policy = relationship("Policy", foreign_keys=[policy_id])
    verified_by = relationship("User", foreign_keys=[verified_by_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_medical_record_type', 'record_type'),
        Index('idx_medical_record_customer', 'customer_id'),
        Index('idx_medical_record_date', 'record_date'),
        Index('idx_medical_record_policy', 'policy_id'),
        Index('idx_medical_record_smoking', 'smoking_status'),
    )
    
    def __repr__(self) -> str:
        return f"<MedicalRecord(id={self.id}, type={self.record_type}, customer_id={self.customer_id})>"
