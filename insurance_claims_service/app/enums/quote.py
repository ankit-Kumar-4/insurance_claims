"""Quote-related enums"""

import enum


class QuoteStatus(str, enum.Enum):
    """Status of insurance quote"""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CONVERTED_TO_POLICY = "converted_to_policy"
    UNDER_REVIEW = "under_review"
