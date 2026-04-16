"""CRUD operations for Property"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.property import Property


class CRUDProperty(CRUDBase[Property]):
    """
    CRUD operations for Property model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_by_address() method

    pass


# Create global instance
property = CRUDProperty(Property)
