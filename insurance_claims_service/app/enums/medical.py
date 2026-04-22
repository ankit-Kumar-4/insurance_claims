"""Medical record-related enums"""

import enum


class MedicalRecordType(str, enum.Enum):
    """Types of medical records"""
    CHECKUP = "checkup"
    DIAGNOSIS = "diagnosis"
    TREATMENT = "treatment"
    PRESCRIPTION = "prescription"
    LAB_RESULT = "lab_result"
    IMAGING = "imaging"
    SURGERY = "surgery"
    HOSPITALIZATION = "hospitalization"
    EMERGENCY = "emergency"
    VACCINATION = "vaccination"
    THERAPY = "therapy"


class SmokingStatus(str, enum.Enum):
    """Smoking status"""
    NON_SMOKER = "non_smoker"
    FORMER_SMOKER = "former_smoker"
    OCCASIONAL_SMOKER = "occasional_smoker"
    REGULAR_SMOKER = "regular_smoker"
    HEAVY_SMOKER = "heavy_smoker"


class AlcoholConsumption(str, enum.Enum):
    """Alcohol consumption level"""
    NONE = "none"
    OCCASIONAL = "occasional"
    MODERATE = "moderate"
    HEAVY = "heavy"


# Alias for backwards compatibility
RecordType = MedicalRecordType
