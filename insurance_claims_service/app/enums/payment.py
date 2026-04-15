"""Payment-related enums"""

import enum


class PaymentType(str, enum.Enum):
    """Type of payment transaction"""
    PREMIUM = "premium"
    CLAIM_SETTLEMENT = "claim_settlement"
    REFUND = "refund"
    COMMISSION = "commission"
    PENALTY = "penalty"
    LATE_FEE = "late_fee"


class PaymentMethod(str, enum.Enum):
    """Method of payment"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    ACH = "ach"
    CHECK = "check"
    CASH = "cash"
    DIGITAL_WALLET = "digital_wallet"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    WIRE_TRANSFER = "wire_transfer"


class PaymentStatus(str, enum.Enum):
    """Status of payment transaction"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    OVERDUE = "overdue"
    WAIVED = "waived"
