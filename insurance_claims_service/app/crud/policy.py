"""CRUD operations for Policy"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.policy import Policy


class CRUDPolicy(CRUDBase[Policy]):
    """
    CRUD operations for Policy model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy_number() method

    # TODO: Implement get_active() method

    # TODO: Implement get_expiring_soon() method

    pass


# Create global instance
policy = CRUDPolicy(Policy)
