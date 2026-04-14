"""
SQLAlchemy models package.

Import all models here to ensure they are registered with SQLAlchemy
and available for Alembic migrations.
"""

from app.models.base import Base, BaseModel

# Import all models here as they are created in Phase 2
# Example:
# from app.models.policy import Policy
# from app.models.claim import Claim
# from app.models.customer import Customer
# etc.

__all__ = [
    "Base",
    "BaseModel",
]
