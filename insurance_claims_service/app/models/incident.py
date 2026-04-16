"""Incident model for events that trigger claims"""

from sqlalchemy import Column, String, Integer, Date, Time, DateTime, ForeignKey, Numeric, Boolean, Index, Enum as SQLEnum, Text, Float
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.incident import IncidentType, IncidentSeverity


class Incident(BaseModel):
    """
    Incident model - represents an event that triggers a claim
    """
    
    __tablename__ = "incidents"
    
    # Incident identification
    incident_type = Column(SQLEnum(IncidentType), nullable=False, index=True)
    
    # Incident timing
    incident_date = Column(Date, nullable=False, index=True)
    incident_time = Column(Time, nullable=True)
    reported_date = Column(DateTime, nullable=False)
    
    # Location
    location_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Incident details
    description = Column(Text, nullable=False)
    severity = Column(SQLEnum(IncidentSeverity), nullable=False, index=True)
    
    # Police report
    police_report_filed = Column(Boolean, default=False, nullable=False)
    police_report_number = Column(String(100), unique=True, nullable=True, index=True)
    
    # Witnesses
    witnesses_count = Column(Integer, default=0, nullable=False)
    
    # Environmental conditions
    weather_conditions = Column(String(200), nullable=True)
    
    # Damage estimation
    estimated_damage = Column(Numeric(15, 2), nullable=True)
    
    # Related entities
    related_policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    related_claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True, index=True)
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    location_address = relationship("Address", foreign_keys=[location_address_id])
    related_policy = relationship("Policy", foreign_keys=[related_policy_id])
    claim = relationship("Claim", back_populates="incidents", foreign_keys=[related_claim_id])
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_incident_type', 'incident_type'),
        Index('idx_incident_date', 'incident_date'),
        Index('idx_incident_severity', 'severity'),
        Index('idx_incident_policy', 'related_policy_id'),
        Index('idx_incident_claim', 'related_claim_id'),
        Index('idx_incident_police_report', 'police_report_number'),
        Index('idx_incident_coordinates', 'latitude', 'longitude'),
    )
    
    def __repr__(self) -> str:
        return f"<Incident(id={self.id}, type={self.incident_type}, date={self.incident_date})>"
    
    @property
    def days_since_incident(self) -> int:
        """Calculate days since incident occurred"""
        from datetime import date
        return (date.today() - self.incident_date).days
