"""
Enums package for Insurance Claims API.
Contains all enum definitions used across the application.
"""

from app.enums.policy import PolicyType, PolicyStatus, PremiumFrequency
from app.enums.claim import ClaimType, ClaimStatus
from app.enums.customer import CustomerType, RiskProfile, CustomerStatus, IdentificationType
from app.enums.payment import PaymentType, PaymentMethod, PaymentStatus
from app.enums.document import DocumentType, DocumentVerificationStatus
from app.enums.incident import IncidentType, IncidentSeverity
from app.enums.vehicle import BodyType, FuelType, VehicleUsageType, VehicleStatus
from app.enums.property import PropertyType, StructureType, ConstructionType, PropertyStatus
from app.enums.medical import MedicalRecordType, SmokingStatus, AlcoholConsumption
from app.enums.quote import QuoteStatus
from app.enums.renewal import RenewalType, RenewalStatus, CustomerAction
from app.enums.commission import CommissionType, CommissionPaymentStatus
from app.enums.endorsement import EndorsementType, EndorsementStatus, RequestedBy
from app.enums.user import UserRole, UserStatus
from app.enums.common import Gender, Status

__all__ = [
    # Policy
    "PolicyType",
    "PolicyStatus",
    "PremiumFrequency",
    # Claim
    "ClaimType",
    "ClaimStatus",
    # Customer
    "CustomerType",
    "RiskProfile",
    "CustomerStatus",
    "IdentificationType",
    # Payment
    "PaymentType",
    "PaymentMethod",
    "PaymentStatus",
    # Document
    "DocumentType",
    "DocumentVerificationStatus",
    # Incident
    "IncidentType",
    "IncidentSeverity",
    # Vehicle
    "BodyType",
    "FuelType",
    "VehicleUsageType",
    "VehicleStatus",
    # Property
    "PropertyType",
    "StructureType",
    "ConstructionType",
    "PropertyStatus",
    # Medical
    "MedicalRecordType",
    "SmokingStatus",
    "AlcoholConsumption",
    # Quote
    "QuoteStatus",
    # Renewal
    "RenewalType",
    "RenewalStatus",
    "CustomerAction",
    # Commission
    "CommissionType",
    "CommissionPaymentStatus",
    # Endorsement
    "EndorsementType",
    "EndorsementStatus",
    "RequestedBy",
    # User
    "UserRole",
    "UserStatus",
    # Common
    "Gender",
    "Status",
]
