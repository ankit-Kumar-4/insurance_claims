"""CRUD operations for Endorsement"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.endorsement import Endorsement


class CRUDEndorsement(CRUDBase[Endorsement]):
    """
    CRUD operations for Endorsement model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_pending() method

    pass


# Create global instance
endorsement = CRUDEndorsement(Endorsement)
