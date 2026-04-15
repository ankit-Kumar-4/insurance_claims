"""Endorsement-related enums"""

import enum


class EndorsementType(str, enum.Enum):
    """Type of policy endorsement"""
    ADD_COVERAGE = "add_coverage"
    REMOVE_COVERAGE = "remove_coverage"
    INCREASE_LIMIT = "increase_limit"
    DECREASE_LIMIT = "decrease_limit"
    CHANGE_BENEFICIARY = "change_beneficiary"
    CHANGE_ADDRESS = "change_address"
    CHANGE_VEHICLE = "change_vehicle"
    ADD_DRIVER = "add_driver"
    REMOVE_DRIVER = "remove_driver"
    ADD_PROPERTY = "add_property"
    REMOVE_PROPERTY = "remove_property"
    CHANGE_DEDUCTIBLE = "change_deductible"
    OTHER = "other"


class EndorsementStatus(str, enum.Enum):
    """Status of endorsement"""
    REQUESTED = "requested"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    CANCELLED = "cancelled"


class RequestedBy(str, enum.Enum):
    """Who requested the endorsement"""
    POLICYHOLDER = "policyholder"
    AGENT = "agent"
    INSURER = "insurer"
    SYSTEM = "system"
