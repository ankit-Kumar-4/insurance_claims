"""CRUD operations for Underwriter"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.underwriter import Underwriter


class CRUDUnderwriter(CRUDBase[Underwriter]):
    """
    CRUD operations for Underwriter model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_license_number() method

    # TODO: Implement get_active() method

    pass


# Create global instance
underwriter = CRUDUnderwriter(Underwriter)
