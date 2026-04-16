"""CRUD operations for User"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User]):
    """
    CRUD operations for User model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_email() method

    # TODO: Implement get_by_username() method

    # TODO: Implement authenticate() method

    pass


# Create global instance
user = CRUDUser(User)
