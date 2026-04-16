"""CRUD operations for Premium"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.premium import Premium


class CRUDPremium(CRUDBase[Premium]):
    """
    CRUD operations for Premium model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_overdue() method

    # TODO: Implement get_upcoming() method

    pass


# Create global instance
premium = CRUDPremium(Premium)
