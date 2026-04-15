"""Vehicle model for auto insurance"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.vehicle import BodyType, FuelType, VehicleUsageType, VehicleStatus


class Vehicle(BaseModel):
    """
    Vehicle model - represents vehicles covered by auto insurance policies
    """
    
    __tablename__ = "vehicles"
    
    # Vehicle identification
    vin = Column(String(17), unique=True, nullable=False, index=True)  # Vehicle Identification Number
    license_plate = Column(String(20), unique=True, nullable=False, index=True)
    
    # Vehicle details
    make = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False, index=True)
    color = Column(String(50), nullable=True)
    
    # Vehicle type
    body_type = Column(SQLEnum(BodyType), nullable=False, index=True)
    fuel_type = Column(SQLEnum(FuelType), nullable=False)
    
    # Specifications
    engine_capacity = Column(String(50), nullable=True)  # e.g., "2.0L"
    transmission = Column(String(50), nullable=True)  # automatic, manual
    seating_capacity = Column(Integer, nullable=True)
    
    # Value
    purchase_price = Column(Numeric(15, 2), nullable=True)
    current_market_value = Column(Numeric(15, 2), nullable=True)
    
    # Usage
    usage_type = Column(SQLEnum(VehicleUsageType), nullable=False, index=True)
    annual_mileage = Column(Integer, nullable=True)
    
    # Registration
    registration_date = Column(Date, nullable=True)
    registration_expiry = Column(Date, nullable=True)
    
    # Status
    status = Column(SQLEnum(VehicleStatus), nullable=False, default=VehicleStatus.ACTIVE, index=True)
    
    # Related entities
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    
    # Relationships
    policy = relationship("Policy", back_populates="vehicles")
    owner = relationship("Customer", foreign_keys=[owner_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_vehicle_vin', 'vin'),
        Index('idx_vehicle_license_plate', 'license_plate'),
        Index('idx_vehicle_make_model', 'make', 'model'),
        Index('idx_vehicle_year', 'year'),
        Index('idx_vehicle_policy', 'policy_id'),
        Index('idx_vehicle_owner', 'owner_id'),
        Index('idx_vehicle_status', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<Vehicle(id={self.id}, vin={self.vin}, make={self.make}, model={self.model})>"
    
    @property
    def full_name(self) -> str:
        """Return vehicle's full name"""
        return f"{self.year} {self.make} {self.model}"
    
    @property
    def age(self) -> int:
        """Calculate vehicle age"""
        from datetime import date
        return date.today().year - self.year
