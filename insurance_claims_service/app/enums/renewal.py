"""Renewal-related enums"""

import enum


class RenewalType(str, enum.Enum):
    """Type of policy renewal"""
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class RenewalStatus(str, enum.Enum):
    """Status of policy renewal"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CustomerAction(str, enum.Enum):
    """Customer action on renewal"""
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REQUESTED_MODIFICATION = "requested_modification"
    NO_RESPONSE = "no_response"
