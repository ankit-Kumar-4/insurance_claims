"""CRUD operations for Insurer"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.insurer import Insurer


class CRUDInsurer(CRUDBase[Insurer]):
    """
    CRUD operations for Insurer model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_license_number() method

    # TODO: Implement get_active() method

    pass


# Create global instance
insurer = CRUDInsurer(Insurer)
