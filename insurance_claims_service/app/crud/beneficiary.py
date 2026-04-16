"""CRUD operations for Beneficiary"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.beneficiary import Beneficiary


class CRUDBeneficiary(CRUDBase[Beneficiary]):
    """
    CRUD operations for Beneficiary model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_primary() method

    pass


# Create global instance
beneficiary = CRUDBeneficiary(Beneficiary)
