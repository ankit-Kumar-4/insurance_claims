"""Incident-related enums"""

import enum


class IncidentType(str, enum.Enum):
    """Types of incidents"""
    ACCIDENT = "accident"
    THEFT = "theft"
    FIRE = "fire"
    FLOOD = "flood"
    MEDICAL_EMERGENCY = "medical_emergency"
    DEATH = "death"
    NATURAL_DISASTER = "natural_disaster"
    VANDALISM = "vandalism"
    COLLISION = "collision"
    BREAK_IN = "break_in"
    PROPERTY_DAMAGE = "property_damage"
    PERSONAL_INJURY = "personal_injury"
    EQUIPMENT_FAILURE = "equipment_failure"
    OTHER = "other"


class IncidentSeverity(str, enum.Enum):
    """Severity level of an incident"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CATASTROPHIC = "catastrophic"
    TOTAL_LOSS = "total_loss"
