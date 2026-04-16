"""CRUD operations for Customer"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.customer import Customer


class CRUDCustomer(CRUDBase[Customer]):
    """
    CRUD operations for Customer model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_email() method

    # TODO: Implement get_active_policies() method

    pass


# Create global instance
customer = CRUDCustomer(Customer)
