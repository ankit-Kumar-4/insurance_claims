"""Address model for storing location information"""

from sqlalchemy import Column, String, Float, Index
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Address(BaseModel):
    """
    Address model - supporting entity used by multiple entities
    Stores physical address information for customers, agents, properties, etc.
    """
    
    __tablename__ = "addresses"
    
    # Address fields
    street_line1 = Column(String(255), nullable=False)
    street_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    postal_code = Column(String(20), nullable=False, index=True)
    country = Column(String(100), nullable=False, default="USA", index=True)
    
    # Geographic coordinates for mapping
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Additional details
    address_type = Column(String(50), nullable=True)  # residential, commercial, mailing, etc.
    is_primary = Column(String(10), nullable=True, default="true")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_address_city_state', 'city', 'state'),
        Index('idx_address_postal_code', 'postal_code'),
        Index('idx_address_coordinates', 'latitude', 'longitude'),
    )
    
    def __repr__(self) -> str:
        return f"<Address(id={self.id}, city={self.city}, state={self.state})>"
    
    @property
    def full_address(self) -> str:
        """Return formatted full address"""
        parts = [self.street_line1]
        if self.street_line2:
            parts.append(self.street_line2)
        parts.append(f"{self.city}, {self.state} {self.postal_code}")
        parts.append(self.country)
        return ", ".join(parts)
