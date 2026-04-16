"""CRUD operations for Coverage"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.coverage import Coverage


class CRUDCoverage(CRUDBase[Coverage]):
    """
    CRUD operations for Coverage model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_mandatory() method

    pass


# Create global instance
coverage = CRUDCoverage(Coverage)
