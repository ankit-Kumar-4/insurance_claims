"""CRUD operations for MedicalRecord"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.medical_record import MedicalRecord


class CRUDMedicalRecord(CRUDBase[MedicalRecord]):
    """
    CRUD operations for MedicalRecord model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    # TODO: Implement get_by_policy() method

    # TODO: Implement get_by_customer() method

    pass


# Create global instance
medical_record = CRUDMedicalRecord(MedicalRecord)
