"""CRUD operations for Quote"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.quote import Quote


class CRUDQuote(CRUDBase[Quote]):
    """
    CRUD operations for Quote model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_quote_number() method

    # TODO: Implement get_active() method

    # TODO: Implement get_expired() method

    pass


# Create global instance
quote = CRUDQuote(Quote)
