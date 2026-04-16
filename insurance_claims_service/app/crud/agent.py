"""CRUD operations for Agent"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.agent import Agent


class CRUDAgent(CRUDBase[Agent]):
    """
    CRUD operations for Agent model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_agent_code() method

    # TODO: Implement get_active() method

    # TODO: Implement get_top_performers() method

    pass


# Create global instance
agent = CRUDAgent(Agent)
