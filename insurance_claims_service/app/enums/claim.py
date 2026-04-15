"""Claim-related enums"""

import enum


class ClaimType(str, enum.Enum):
    """Types of insurance claims"""
    DAMAGE = "damage"
    THEFT = "theft"
    ACCIDENT = "accident"
    MEDICAL = "medical"
    DEATH = "death"
    FIRE = "fire"
    FLOOD = "flood"
    NATURAL_DISASTER = "natural_disaster"
    LIABILITY = "liability"
    COLLISION = "collision"
    COMPREHENSIVE = "comprehensive"
    VANDALISM = "vandalism"
    PERSONAL_INJURY = "personal_injury"


class ClaimStatus(str, enum.Enum):
    """Status of a claim"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    PENDING_DOCUMENTS = "pending_documents"
    APPROVED = "approved"
    REJECTED = "rejected"
    PARTIALLY_APPROVED = "partially_approved"
    SETTLED = "settled"
    CLOSED = "closed"
    APPEALED = "appealed"
    CANCELLED = "cancelled"
