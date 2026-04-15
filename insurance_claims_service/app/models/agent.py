"""Agent model for insurance sales representatives"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.common import Status


class Agent(BaseModel):
    """
    Agent/Broker model - represents insurance sales representatives
    """
    
    __tablename__ = "agents"
    
    # Agent identification
    agent_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), nullable=False)
    
    # License information
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    license_expiry_date = Column(Date, nullable=True)
    
    # Professional information
    specialization = Column(String(100), nullable=True)  # life, health, auto, property, commercial
    agency_name = Column(String(200), nullable=True)
    commission_rate = Column(Numeric(5, 2), nullable=True)  # percentage
    
    # Address (Foreign Key)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    
    # Performance metrics
    performance_rating = Column(Numeric(3, 2), nullable=True)  # 0.00 to 5.00
    total_policies_sold = Column(Integer, default=0, nullable=False)
    active_policies_count = Column(Integer, default=0, nullable=False)
    
    # Employment information
    status = Column(SQLEnum(Status), nullable=False, default=Status.ACTIVE, index=True)
    hire_date = Column(Date, nullable=True)
    
    # Relationships
    address = relationship("Address", foreign_keys=[address_id])
    policies = relationship("Policy", back_populates="agent")
    quotes = relationship("Quote", back_populates="agent")
    commissions = relationship("Commission", back_populates="agent")
    
    # Indexes
    __table_args__ = (
        Index('idx_agent_code', 'agent_code'),
        Index('idx_agent_email', 'email'),
        Index('idx_agent_license', 'license_number'),
        Index('idx_agent_status', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<Agent(id={self.id}, code={self.agent_code}, name={self.full_name})>"
    
    @property
    def full_name(self) -> str:
        """Return agent's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_license_valid(self) -> bool:
        """Check if agent's license is still valid"""
        if self.license_expiry_date:
            from datetime import date
            return self.license_expiry_date > date.today()
        return False
