"""Property model for property insurance"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, Boolean, Index, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.property import PropertyType, StructureType, ConstructionType, PropertyStatus


class Property(BaseModel):
    """
    Property model - represents properties covered by property/home insurance
    """
    
    __tablename__ = "properties"
    
    # Property identification
    property_type = Column(SQLEnum(PropertyType), nullable=False, index=True)
    structure_type = Column(SQLEnum(StructureType), nullable=False, index=True)
    
    # Address
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False, index=True)
    
    # Property details
    year_built = Column(Integer, nullable=True)
    construction_type = Column(SQLEnum(ConstructionType), nullable=True)
    square_footage = Column(Integer, nullable=True)
    lot_size = Column(Numeric(15, 2), nullable=True)  # in square feet or acres
    
    # Rooms
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Numeric(3, 1), nullable=True)  # e.g., 2.5 bathrooms
    stories = Column(Integer, nullable=True)
    
    # Value
    purchase_price = Column(Numeric(15, 2), nullable=True)
    current_market_value = Column(Numeric(15, 2), nullable=False)
    estimated_rebuild_cost = Column(Numeric(15, 2), nullable=True)
    
    # Features
    has_garage = Column(Boolean, default=False, nullable=False)
    has_basement = Column(Boolean, default=False, nullable=False)
    has_pool = Column(Boolean, default=False, nullable=False)
    has_security_system = Column(Boolean, default=False, nullable=False)
    has_fire_alarm = Column(Boolean, default=False, nullable=False)
    
    # Additional details
    description = Column(Text, nullable=True)
    
    # Status
    status = Column(SQLEnum(PropertyStatus), nullable=False, default=PropertyStatus.ACTIVE, index=True)
    
    # Related entities
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    
    # Relationships
    address = relationship("Address", foreign_keys=[address_id])
    policy = relationship("Policy", back_populates="properties")
    owner = relationship("Customer", foreign_keys=[owner_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_property_type', 'property_type'),
        Index('idx_property_structure', 'structure_type'),
        Index('idx_property_address', 'address_id'),
        Index('idx_property_policy', 'policy_id'),
        Index('idx_property_owner', 'owner_id'),
        Index('idx_property_status', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<Property(id={self.id}, type={self.property_type}, structure={self.structure_type})>"
    
    @property
    def age(self) -> int:
        """Calculate property age"""
        if self.year_built:
            from datetime import date
            return date.today().year - self.year_built
        return None
