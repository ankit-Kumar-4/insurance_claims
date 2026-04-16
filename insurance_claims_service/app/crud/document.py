"""CRUD operations for Document"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.document import Document


class CRUDDocument(CRUDBase[Document]):
    """
    CRUD operations for Document model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_by_claim() method

    # TODO: Implement get_unverified() method

    pass


# Create global instance
document = CRUDDocument(Document)
