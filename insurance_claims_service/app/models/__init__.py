"""Models package - exports all SQLAlchemy models"""

from app.models.base import Base, BaseModel
from app.models.address import Address
from app.models.user import User
from app.models.customer import Customer
from app.models.agent import Agent
from app.models.insurer import Insurer
from app.models.underwriter import Underwriter
from app.models.policy import Policy
from app.models.coverage import Coverage
from app.models.premium import Premium
from app.models.beneficiary import Beneficiary
from app.models.claim import Claim
from app.models.incident import Incident
from app.models.risk_assessment import RiskAssessment
from app.models.payment import Payment
from app.models.document import Document
from app.models.vehicle import Vehicle
from app.models.property import Property
from app.models.medical_record import MedicalRecord
from app.models.quote import Quote
from app.models.policy_renewal import PolicyRenewal
from app.models.commission import Commission
from app.models.endorsement import Endorsement

__all__ = [
    # Base
    "Base",
    "BaseModel",
    # Supporting & Authentication
    "Address",
    "User",
    # People & Organizations
    "Customer",
    "Agent",
    "Insurer",
    "Underwriter",
    # Policy-Related
    "Policy",
    "Coverage",
    "Premium",
    "Beneficiary",
    # Claims-Related
    "Claim",
    "Incident",
    "RiskAssessment",
    # Transactions & Files
    "Payment",
    "Document",
    # Assets & Health
    "Vehicle",
    "Property",
    "MedicalRecord",
    # Workflow
    "Quote",
    "PolicyRenewal",
    "Commission",
    "Endorsement",
]
