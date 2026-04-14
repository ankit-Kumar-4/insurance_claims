"""
Base model for all database models.
Provides common fields and functionality for all entities.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all SQLAlchemy models"""
    
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base):
    """
    Abstract base model with common fields for all entities.
    
    All models should inherit from this class to get:
    - id: Primary key
    - created_date: Timestamp when record was created
    - last_modified_date: Timestamp when record was last updated
    - deleted_at: Soft delete timestamp (NULL if not deleted)
    """
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_modified_date = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)  # For soft deletes
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
