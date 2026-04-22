"""
Claim Processing Service
Handles claim validation, workflow, and settlement
"""

from decimal import Decimal
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.claim import Claim
from app.models.policy import Policy
from app.enums.claim import ClaimStatus


class ClaimProcessorService:
    """Service for processing insurance claims"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def validate_claim(self, claim: Claim, policy: Policy) -> Dict[str, Any]:
        """
        Validate claim against policy coverage and terms
        
        Returns validation result with any issues found
        """
        issues = []
        is_valid = True
        
        # Check policy is active
        if policy.status != "ACTIVE":
            issues.append("Policy is not active")
            is_valid = False
        
        # Check incident date is within policy period
        if claim.incident_date < policy.start_date:
            issues.append("Incident occurred before policy start date")
            is_valid = False
        
        if policy.end_date and claim.incident_date > policy.end_date:
            issues.append("Incident occurred after policy end date")
            is_valid = False
        
        # Check claim amount against coverage
        if claim.claim_amount > policy.coverage_amount:
            issues.append(f"Claim amount exceeds policy coverage limit")
            is_valid = False
        
        return {
            "is_valid": is_valid,
            "issues": issues,
            "policy_id": policy.id,
            "claim_id": claim.id,
        }
    
    async def calculate_settlement(
        self,
        claim: Claim,
        policy: Policy,
        approved_amount: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """Calculate claim settlement amount after deductible"""
        
        # Use approved amount or full claim amount
        settlement_base = approved_amount or claim.claim_amount
        
        # Apply deductible
        deductible = policy.deductible or Decimal("0")
        settlement_amount = max(Decimal("0"), settlement_base - deductible)
        
        # Check coverage limit
        coverage_limit = policy.coverage_amount
        if settlement_amount > coverage_limit:
            settlement_amount = coverage_limit
        
        return {
            "settlement_amount": settlement_amount.quantize(Decimal('0.01')),
            "claim_amount": claim.claim_amount.quantize(Decimal('0.01')),
            "deductible_applied": deductible.quantize(Decimal('0.01')),
            "coverage_limit": coverage_limit.quantize(Decimal('0.01')),
        }
    
    async def process_approval(self, claim: Claim, approved_by: int) -> Dict[str, Any]:
        """Process claim approval"""
        return {
            "claim_id": claim.id,
            "status": ClaimStatus.APPROVED,
            "approved_by": approved_by,
            "approved_at": datetime.now(),
        }
    
    async def process_rejection(
        self,
        claim: Claim,
        rejected_by: int,
        reason: str
    ) -> Dict[str, Any]:
        """Process claim rejection"""
        return {
            "claim_id": claim.id,
            "status": ClaimStatus.REJECTED,
            "rejected_by": rejected_by,
            "rejection_reason": reason,
            "rejected_at": datetime.now(),
        }
