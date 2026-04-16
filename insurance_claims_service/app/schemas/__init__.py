"""Schemas package - Pydantic models for API validation and serialization"""

# Base schemas
from app.schemas.base import (
    BaseSchema,
    TimestampSchema,
    ResponseSchema,
    PaginationParams,
    PaginatedResponse,
    SuccessResponse,
    ErrorResponse,
)

# Authentication schemas
from app.schemas.auth import (
    Token,
    TokenData,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

# Entity schemas
from app.schemas.address import (
    AddressBase,
    AddressCreate,
    AddressUpdate,
    AddressResponse,
    AddressInDB,
)

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInDB,
)

from app.schemas.customer import (
    CustomerBase,
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerInDB,
)

from app.schemas.policy import (
    PolicyBase,
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyInDB,
)

from app.schemas.claim import (
    ClaimBase,
    ClaimCreate,
    ClaimUpdate,
    ClaimResponse,
    ClaimInDB,
)

from app.schemas.agent import (
    AgentBase,
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentInDB,
)

from app.schemas.payment import (
    PaymentBase,
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
    PaymentInDB,
)

from app.schemas.quote import (
    QuoteBase,
    QuoteCreate,
    QuoteUpdate,
    QuoteResponse,
    QuoteInDB,
)

from app.schemas.premium import (
    PremiumBase,
    PremiumCreate,
    PremiumUpdate,
    PremiumResponse,
    PremiumInDB,
)

from app.schemas.coverage import (
    CoverageBase,
    CoverageCreate,
    CoverageUpdate,
    CoverageResponse,
    CoverageInDB,
)

from app.schemas.beneficiary import (
    BeneficiaryBase,
    BeneficiaryCreate,
    BeneficiaryUpdate,
    BeneficiaryResponse,
    BeneficiaryInDB,
)

from app.schemas.policy_renewal import (
    PolicyRenewalBase,
    PolicyRenewalCreate,
    PolicyRenewalUpdate,
    PolicyRenewalResponse,
    PolicyRenewalInDB,
)

from app.schemas.endorsement import (
    EndorsementBase,
    EndorsementCreate,
    EndorsementUpdate,
    EndorsementResponse,
    EndorsementInDB,
)

from app.schemas.commission import (
    CommissionBase,
    CommissionCreate,
    CommissionUpdate,
    CommissionResponse,
    CommissionInDB,
)

from app.schemas.insurer import (
    InsurerBase,
    InsurerCreate,
    InsurerUpdate,
    InsurerResponse,
    InsurerInDB,
)

from app.schemas.underwriter import (
    UnderwriterBase,
    UnderwriterCreate,
    UnderwriterUpdate,
    UnderwriterResponse,
    UnderwriterInDB,
)

from app.schemas.incident import (
    IncidentBase,
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IncidentInDB,
)

from app.schemas.risk_assessment import (
    RiskAssessmentBase,
    RiskAssessmentCreate,
    RiskAssessmentUpdate,
    RiskAssessmentResponse,
    RiskAssessmentInDB,
)

from app.schemas.document import (
    DocumentBase,
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentInDB,
)

from app.schemas.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleInDB,
)

from app.schemas.property import (
    PropertyBase,
    PropertyCreate,
    PropertyUpdate,
    PropertyResponse,
    PropertyInDB,
)

from app.schemas.medical_record import (
    MedicalRecordBase,
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
    MedicalRecordInDB,
)


__all__ = [
    # Base
    "BaseSchema",
    "TimestampSchema",
    "ResponseSchema",
    "PaginationParams",
    "PaginatedResponse",
    "SuccessResponse",
    "ErrorResponse",
    # Auth
    "Token",
    "TokenData",
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    # Address
    "AddressBase",
    "AddressCreate",
    "AddressUpdate",
    "AddressResponse",
    "AddressInDB",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInDB",
    # Customer
    "CustomerBase",
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "CustomerInDB",
    # Policy
    "PolicyBase",
    "PolicyCreate",
    "PolicyUpdate",
    "PolicyResponse",
    "PolicyInDB",
    # Claim
    "ClaimBase",
    "ClaimCreate",
    "ClaimUpdate",
    "ClaimResponse",
    "ClaimInDB",
    # Agent
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "AgentInDB",
    # Payment
    "PaymentBase",
    "PaymentCreate",
    "PaymentUpdate",
    "PaymentResponse",
    "PaymentInDB",
    # Quote
    "QuoteBase",
    "QuoteCreate",
    "QuoteUpdate",
    "QuoteResponse",
    "QuoteInDB",
    # Premium
    "PremiumBase",
    "PremiumCreate",
    "PremiumUpdate",
    "PremiumResponse",
    "PremiumInDB",
    # Coverage
    "CoverageBase",
    "CoverageCreate",
    "CoverageUpdate",
    "CoverageResponse",
    "CoverageInDB",
    # Beneficiary
    "BeneficiaryBase",
    "BeneficiaryCreate",
    "BeneficiaryUpdate",
    "BeneficiaryResponse",
    "BeneficiaryInDB",
    # PolicyRenewal
    "PolicyRenewalBase",
    "PolicyRenewalCreate",
    "PolicyRenewalUpdate",
    "PolicyRenewalResponse",
    "PolicyRenewalInDB",
    # Endorsement
    "EndorsementBase",
    "EndorsementCreate",
    "EndorsementUpdate",
    "EndorsementResponse",
    "EndorsementInDB",
    # Commission
    "CommissionBase",
    "CommissionCreate",
    "CommissionUpdate",
    "CommissionResponse",
    "CommissionInDB",
    # Insurer
    "InsurerBase",
    "InsurerCreate",
    "InsurerUpdate",
    "InsurerResponse",
    "InsurerInDB",
    # Underwriter
    "UnderwriterBase",
    "UnderwriterCreate",
    "UnderwriterUpdate",
    "UnderwriterResponse",
    "UnderwriterInDB",
    # Incident
    "IncidentBase",
    "IncidentCreate",
    "IncidentUpdate",
    "IncidentResponse",
    "IncidentInDB",
    # RiskAssessment
    "RiskAssessmentBase",
    "RiskAssessmentCreate",
    "RiskAssessmentUpdate",
    "RiskAssessmentResponse",
    "RiskAssessmentInDB",
    # Document
    "DocumentBase",
    "DocumentCreate",
    "DocumentUpdate",
    "DocumentResponse",
    "DocumentInDB",
    # Vehicle
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",
    "VehicleInDB",
    # Property
    "PropertyBase",
    "PropertyCreate",
    "PropertyUpdate",
    "PropertyResponse",
    "PropertyInDB",
    # MedicalRecord
    "MedicalRecordBase",
    "MedicalRecordCreate",
    "MedicalRecordUpdate",
    "MedicalRecordResponse",
    "MedicalRecordInDB",
]
