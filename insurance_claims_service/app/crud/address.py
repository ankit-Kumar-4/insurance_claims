"""CRUD operations for Address"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.address import Address


class CRUDAddress(CRUDBase[Address]):
    """
    CRUD operations for Address model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    pass


# Create global instance
address = CRUDAddress(Address)
