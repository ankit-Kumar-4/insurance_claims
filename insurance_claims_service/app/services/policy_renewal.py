"""
Policy Renewal Service
Handles automatic policy renewal processing
"""

from decimal import Decimal
from datetime import datetime, date, timedelta
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.policy import Policy
from app.models.policy_renewal import PolicyRenewal
from app.enums.renewal import RenewalStatus


class PolicyRenewalService:
    """Service for handling policy renewals"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def check_renewal_eligibility(self, policy: Policy) -> Dict[str, Any]:
        """Check if policy is eligible for renewal"""
        is_eligible = True
        reasons = []
        
        if policy.status != "ACTIVE":
            is_eligible = False
            reasons.append("Policy is not active")
        
        if not policy.end_date:
            is_eligible = False
            reasons.append("Policy has no end date")
        
        # Check if renewal is within window (30-90 days before expiry)
        days_until_expiry = (policy.end_date - date.today()).days
        if days_until_expiry > 90:
            is_eligible = False
            reasons.append(f"Too early to renew ({days_until_expiry} days until expiry)")
        elif days_until_expiry < 0:
            is_eligible = False
            reasons.append("Policy has already expired")
        
        return {
            "is_eligible": is_eligible,
            "reasons": reasons,
            "days_until_expiry": days_until_expiry,
            "policy_id": policy.id,
        }
    
    async def calculate_renewal_premium(
        self,
        policy: Policy,
        rate_adjustment: Decimal = Decimal("1.05")  # 5% increase
    ) -> Dict[str, Any]:
        """Calculate renewal premium with rate adjustment"""
        
        current_premium = policy.premium_amount or Decimal("0")
        new_premium = (current_premium * rate_adjustment).quantize(Decimal('0.01'))
        
        return {
            "current_premium": current_premium.quantize(Decimal('0.01')),
            "new_premium": new_premium,
            "rate_adjustment": float(rate_adjustment),
            "increase_amount": (new_premium - current_premium).quantize(Decimal('0.01')),
            "increase_percentage": float((rate_adjustment - Decimal("1")) * Decimal("100")),
        }
    
    async def get_expiring_policies(self, days: int = 30) -> List[Policy]:
        """Get policies expiring within specified days"""
        cutoff_date = date.today() + timedelta(days=days)
        
        stmt = select(Policy).where(
            Policy.end_date <= cutoff_date,
            Policy.end_date >= date.today(),
            Policy.status == "ACTIVE",
            Policy.deleted_at.is_(None)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
