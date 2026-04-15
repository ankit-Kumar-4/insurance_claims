"""Document-related enums"""

import enum


class DocumentType(str, enum.Enum):
    """Types of documents"""
    POLICY_DOCUMENT = "policy_document"
    CLAIM_FORM = "claim_form"
    MEDICAL_REPORT = "medical_report"
    POLICE_REPORT = "police_report"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    PHOTO = "photo"
    VIDEO = "video"
    ID_PROOF = "id_proof"
    ADDRESS_PROOF = "address_proof"
    INCOME_PROOF = "income_proof"
    REPAIR_ESTIMATE = "repair_estimate"
    DEATH_CERTIFICATE = "death_certificate"
    BIRTH_CERTIFICATE = "birth_certificate"
    MARRIAGE_CERTIFICATE = "marriage_certificate"
    VEHICLE_REGISTRATION = "vehicle_registration"
    PROPERTY_DEED = "property_deed"
    TAX_RETURN = "tax_return"
    BANK_STATEMENT = "bank_statement"
    OTHER = "other"


class DocumentVerificationStatus(str, enum.Enum):
    """Document verification status"""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REQUIRES_UPDATE = "requires_update"
