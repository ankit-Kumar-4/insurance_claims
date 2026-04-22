"""Policy-related enums"""

import enum


class PolicyType(str, enum.Enum):
    """Types of insurance policies"""
    AUTO = "auto"
    HEALTH = "health"
    LIFE = "life"
    PROPERTY = "property"
    HOME = "home"
    RENTERS = "renters"
    TRAVEL = "travel"
    BUSINESS = "business"
    LIABILITY = "liability"
    DISABILITY = "disability"
    DENTAL = "dental"
    VISION = "vision"
    PET = "pet"


class PolicyStatus(str, enum.Enum):
    """Status of an insurance policy"""
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    LAPSED = "lapsed"
    SUSPENDED = "suspended"
    UNDER_REVIEW = "under_review"


class PremiumFrequency(str, enum.Enum):
    """Frequency of premium payments"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semi_annually"
    ANNUALLY = "annually"
    ONE_TIME = "one_time"


class CoverageType(str, enum.Enum):
    """Types of insurance coverage"""
    LIABILITY = "liability"
    COLLISION = "collision"
    COMPREHENSIVE = "comprehensive"
    PERSONAL_INJURY = "personal_injury"
    PROPERTY_DAMAGE = "property_damage"
    MEDICAL_PAYMENTS = "medical_payments"
    UNINSURED_MOTORIST = "uninsured_motorist"
    UNDERINSURED_MOTORIST = "underinsured_motorist"
