"""CRUD operations for Commission"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.commission import Commission


class CRUDCommission(CRUDBase[Commission]):
    """
    CRUD operations for Commission model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_agent() method

    # TODO: Implement get_pending() method

    # TODO: Implement get_unpaid() method

    pass


# Create global instance
commission = CRUDCommission(Commission)
