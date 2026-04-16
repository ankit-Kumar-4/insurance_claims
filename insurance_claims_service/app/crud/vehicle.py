"""CRUD operations for Vehicle"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.vehicle import Vehicle


class CRUDVehicle(CRUDBase[Vehicle]):
    """
    CRUD operations for Vehicle model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_by_vin() method

    pass


# Create global instance
vehicle = CRUDVehicle(Vehicle)
