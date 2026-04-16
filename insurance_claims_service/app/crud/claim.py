"""CRUD operations for Claim"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.claim import Claim


class CRUDClaim(CRUDBase[Claim]):
    """
    CRUD operations for Claim model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_claim_number() method

    # TODO: Implement get_by_status() method

    # TODO: Implement get_pending() method

    pass


# Create global instance
claim = CRUDClaim(Claim)
