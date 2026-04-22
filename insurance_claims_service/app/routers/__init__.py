"""
Routers package
"""

from app.routers.auth import router as auth_router
from app.routers.policy import router as policy_router
from app.routers.claim import router as claim_router
from app.routers.customer import router as customer_router
from app.routers.agent import router as agent_router
from app.routers.insurer import router as insurer_router
from app.routers.premium import router as premium_router
from app.routers.coverage import router as coverage_router
from app.routers.beneficiary import router as beneficiary_router
from app.routers.underwriter import router as underwriter_router
from app.routers.risk_assessment import router as risk_assessment_router
from app.routers.payment import router as payment_router
from app.routers.document import router as document_router
from app.routers.incident import router as incident_router
from app.routers.vehicle import router as vehicle_router
from app.routers.property import router as property_router
from app.routers.medical_record import router as medical_record_router
from app.routers.quote import router as quote_router
from app.routers.policy_renewal import router as policy_renewal_router
from app.routers.commission import router as commission_router
from app.routers.endorsement import router as endorsement_router

__all__ = [
    "auth_router",
    "policy_router",
    "claim_router",
    "customer_router",
    "agent_router",
    "insurer_router",
    "premium_router",
    "coverage_router",
    "beneficiary_router",
    "underwriter_router",
    "risk_assessment_router",
    "payment_router",
    "document_router",
    "incident_router",
    "vehicle_router",
    "property_router",
    "medical_record_router",
    "quote_router",
    "policy_renewal_router",
    "commission_router",
    "endorsement_router",
]
