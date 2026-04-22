"""Commission-related enums"""

import enum


class CommissionType(str, enum.Enum):
    """Type of commission"""
    NEW_BUSINESS = "new_business"
    RENEWAL = "renewal"
    REFERRAL = "referral"
    CROSS_SELL = "cross_sell"
    UP_SELL = "up_sell"
    OVERRIDE = "override"


class CommissionPaymentStatus(str, enum.Enum):
    """Status of commission payment"""
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    WITHHELD = "withheld"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


# Alias for backwards compatibility
CommissionStatus = CommissionPaymentStatus
