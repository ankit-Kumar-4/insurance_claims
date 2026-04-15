"""Customer-related enums"""

import enum


class CustomerType(str, enum.Enum):
    """Type of customer"""
    INDIVIDUAL = "individual"
    CORPORATE = "corporate"
    FAMILY = "family"
    SMALL_BUSINESS = "small_business"


class RiskProfile(str, enum.Enum):
    """Customer risk assessment level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class CustomerStatus(str, enum.Enum):
    """Customer account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BLACKLISTED = "blacklisted"
    PENDING_VERIFICATION = "pending_verification"


class IdentificationType(str, enum.Enum):
    """Types of identification documents"""
    SSN = "ssn"
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"
    NATIONAL_ID = "national_id"
    TAX_ID = "tax_id"
    AADHAR = "aadhar"
    PAN = "pan"
