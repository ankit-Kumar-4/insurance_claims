"""CRUD operations for all entities"""

# Import all CRUD instances
from app.crud.address import address
from app.crud.user import user
from app.crud.customer import customer
from app.crud.policy import policy
from app.crud.claim import claim
from app.crud.agent import agent
from app.crud.payment import payment
from app.crud.quote import quote
from app.crud.premium import premium
from app.crud.coverage import coverage
from app.crud.beneficiary import beneficiary
from app.crud.policy_renewal import policy_renewal
from app.crud.endorsement import endorsement
from app.crud.commission import commission
from app.crud.insurer import insurer
from app.crud.underwriter import underwriter
from app.crud.incident import incident
from app.crud.risk_assessment import risk_assessment
from app.crud.document import document
from app.crud.vehicle import vehicle
from app.crud.property import property as property_crud  # 'property' is a Python keyword
from app.crud.medical_record import medical_record

__all__ = [
    "address",
    "user",
    "customer",
    "policy",
    "claim",
    "agent",
    "payment",
    "quote",
    "premium",
    "coverage",
    "beneficiary",
    "policy_renewal",
    "endorsement",
    "commission",
    "insurer",
    "underwriter",
    "incident",
    "risk_assessment",
    "document",
    "vehicle",
    "property_crud",
    "medical_record",
]
