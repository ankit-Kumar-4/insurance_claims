"""
Commission Calculation Service
Handles commission calculations for agents and sales teams
"""

from decimal import Decimal
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.policy import Policy
from app.models.agent import Agent
from app.models.commission import Commission
from app.enums.policy import PolicyType
from app.enums.commission import CommissionType, CommissionPaymentStatus


class CommissionCalculatorService:
    """Service for calculating agent commissions"""
    
    # Base commission rates by policy type (percentage of premium)
    BASE_COMMISSION_RATES = {
        PolicyType.AUTO: Decimal("0.10"),  # 10%
        PolicyType.HEALTH: Decimal("0.12"),  # 12%
        PolicyType.LIFE: Decimal("0.15"),  # 15%
        PolicyType.HOME: Decimal("0.10"),  # 10%
        PolicyType.TRAVEL: Decimal("0.08"),  # 8%
        PolicyType.BUSINESS: Decimal("0.12"),  # 12%
    }
    
    # Tiered commission structure based on sales volume
    TIER_MULTIPLIERS = {
        "BRONZE": Decimal("1.0"),    # 0-50 policies
        "SILVER": Decimal("1.1"),    # 51-100 policies
        "GOLD": Decimal("1.2"),      # 101-200 policies
        "PLATINUM": Decimal("1.3"),  # 201+ policies
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def calculate_policy_commission(
        self,
        policy: Policy,
        agent: Agent,
        premium_amount: Decimal,
        is_new_business: bool = True,
        is_renewal: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate commission for a single policy
        
        Args:
            policy: Policy instance
            agent: Agent instance
            premium_amount: Premium amount for the policy
            is_new_business: Whether this is new business (vs renewal)
            is_renewal: Whether this is a renewal
            
        Returns:
            Dict with commission details
        """
        # Get base commission rate
        base_rate = self.BASE_COMMISSION_RATES.get(
            policy.policy_type,
            Decimal("0.10")
        )
        
        # Apply new business vs renewal factor
        if is_new_business:
            business_type_multiplier = Decimal("1.0")  # Full commission
        elif is_renewal:
            business_type_multiplier = Decimal("0.5")  # 50% for renewals
        else:
            business_type_multiplier = Decimal("0.75")  # 75% for other
        
        # Calculate agent's tier based on performance
        tier = await self._calculate_agent_tier(agent.id)
        tier_multiplier = self.TIER_MULTIPLIERS.get(tier, Decimal("1.0"))
        
        # Calculate base commission
        base_commission = premium_amount * base_rate
        
        # Apply multipliers
        final_commission = (
            base_commission *
            business_type_multiplier *
            tier_multiplier
        )
        
        final_commission = final_commission.quantize(Decimal('0.01'))
        
        return {
            "commission_amount": final_commission,
            "base_commission": base_commission.quantize(Decimal('0.01')),
            "base_rate": float(base_rate),
            "tier": tier,
            "tier_multiplier": float(tier_multiplier),
            "business_type_multiplier": float(business_type_multiplier),
            "premium_amount": premium_amount,
            "policy_type": policy.policy_type.value,
        }
    
    async def calculate_split_commission(
        self,
        policy: Policy,
        agents: List[Agent],
        split_percentages: List[Decimal],
        premium_amount: Decimal
    ) -> List[Dict[str, Any]]:
        """
        Calculate split commission for multiple agents
        
        Args:
            policy: Policy instance
            agents: List of Agent instances
            split_percentages: List of split percentages (must sum to 100)
            premium_amount: Premium amount
            
        Returns:
            List of commission details for each agent
        """
        if len(agents) != len(split_percentages):
            raise ValueError("Number of agents must match number of split percentages")
        
        if sum(split_percentages) != Decimal("100"):
            raise ValueError("Split percentages must sum to 100")
        
        commissions = []
        
        for agent, split_pct in zip(agents, split_percentages):
            # Calculate commission for this agent
            agent_premium = premium_amount * (split_pct / Decimal("100"))
            
            commission_data = await self.calculate_policy_commission(
                policy=policy,
                agent=agent,
                premium_amount=agent_premium,
                is_new_business=True
            )
            
            commission_data["split_percentage"] = float(split_pct)
            commission_data["agent_id"] = agent.id
            commission_data["agent_name"] = f"{agent.first_name} {agent.last_name}"
            
            commissions.append(commission_data)
        
        return commissions
    
    async def calculate_renewal_commission(
        self,
        policy: Policy,
        agent: Agent,
        renewal_premium: Decimal
    ) -> Dict[str, Any]:
        """
        Calculate commission for policy renewal
        
        Args:
            policy: Policy instance
            agent: Agent instance
            renewal_premium: Premium amount for renewal
            
        Returns:
            Dict with commission details
        """
        return await self.calculate_policy_commission(
            policy=policy,
            agent=agent,
            premium_amount=renewal_premium,
            is_new_business=False,
            is_renewal=True
        )
    
    async def calculate_override_commission(
        self,
        manager_agent: Agent,
        team_policies: List[Policy],
        override_rate: Decimal = Decimal("0.02")  # 2% override
    ) -> Dict[str, Any]:
        """
        Calculate override commission for sales managers
        
        Args:
            manager_agent: Manager agent instance
            team_policies: List of policies sold by team
            override_rate: Override commission rate
            
        Returns:
            Dict with override commission details
        """
        total_premium = Decimal("0")
        policy_count = len(team_policies)
        
        for policy in team_policies:
            if policy.premium_amount:
                total_premium += policy.premium_amount
        
        override_commission = total_premium * override_rate
        override_commission = override_commission.quantize(Decimal('0.01'))
        
        return {
            "override_commission": override_commission,
            "total_team_premium": total_premium.quantize(Decimal('0.01')),
            "policy_count": policy_count,
            "override_rate": float(override_rate),
            "manager_id": manager_agent.id,
            "manager_name": f"{manager_agent.first_name} {manager_agent.last_name}",
        }
    
    async def calculate_bonus_commission(
        self,
        agent: Agent,
        period_start: date,
        period_end: date
    ) -> Dict[str, Any]:
        """
        Calculate bonus commission based on performance targets
        
        Args:
            agent: Agent instance
            period_start: Start date of period
            period_end: End date of period
            
        Returns:
            Dict with bonus details
        """
        # Get agent's policies in period
        stmt = select(Policy).where(
            Policy.agent_id == agent.id,
            Policy.start_date >= period_start,
            Policy.start_date <= period_end,
            Policy.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        policies = result.scalars().all()
        
        policy_count = len(policies)
        total_premium = sum(p.premium_amount or Decimal("0") for p in policies)
        
        # Bonus tiers
        bonus_amount = Decimal("0")
        
        if policy_count >= 50:
            bonus_amount = Decimal("5000")  # $5000 bonus
        elif policy_count >= 30:
            bonus_amount = Decimal("3000")  # $3000 bonus
        elif policy_count >= 20:
            bonus_amount = Decimal("1500")  # $1500 bonus
        elif policy_count >= 10:
            bonus_amount = Decimal("500")   # $500 bonus
        
        # Additional premium-based bonus (0.5% of total premium if > $100k)
        if total_premium > Decimal("100000"):
            premium_bonus = total_premium * Decimal("0.005")
            bonus_amount += premium_bonus
        
        return {
            "bonus_amount": bonus_amount.quantize(Decimal('0.01')),
            "policy_count": policy_count,
            "total_premium": total_premium.quantize(Decimal('0.01')),
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "agent_id": agent.id,
        }
    
    async def calculate_monthly_commission_summary(
        self,
        agent: Agent,
        month: int,
        year: int
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive commission summary for a month
        
        Args:
            agent: Agent instance
            month: Month number (1-12)
            year: Year
            
        Returns:
            Dict with monthly commission summary
        """
        # Get month start and end
        from calendar import monthrange
        _, last_day = monthrange(year, month)
        period_start = date(year, month, 1)
        period_end = date(year, month, last_day)
        
        # Get all commissions for the period
        stmt = select(Commission).where(
            Commission.agent_id == agent.id,
            Commission.earned_date >= period_start,
            Commission.earned_date <= period_end,
            Commission.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        commissions = result.scalars().all()
        
        # Calculate totals by type
        new_business_total = Decimal("0")
        renewal_total = Decimal("0")
        override_total = Decimal("0")
        bonus_total = Decimal("0")
        
        for comm in commissions:
            if comm.commission_type == CommissionType.NEW_BUSINESS:
                new_business_total += comm.amount
            elif comm.commission_type == CommissionType.RENEWAL:
                renewal_total += comm.amount
            elif comm.commission_type == CommissionType.OVERRIDE:
                override_total += comm.amount
            elif comm.commission_type == CommissionType.BONUS:
                bonus_total += comm.amount
        
        total_earned = new_business_total + renewal_total + override_total + bonus_total
        
        # Get payment status breakdown
        paid = sum(c.amount for c in commissions if c.payment_status == CommissionPaymentStatus.PAID)
        pending = sum(c.amount for c in commissions if c.payment_status == CommissionPaymentStatus.PENDING)
        
        return {
            "agent_id": agent.id,
            "agent_name": f"{agent.first_name} {agent.last_name}",
            "period": f"{year}-{month:02d}",
            "total_earned": total_earned.quantize(Decimal('0.01')),
            "new_business": new_business_total.quantize(Decimal('0.01')),
            "renewals": renewal_total.quantize(Decimal('0.01')),
            "overrides": override_total.quantize(Decimal('0.01')),
            "bonuses": bonus_total.quantize(Decimal('0.01')),
            "paid": paid.quantize(Decimal('0.01')),
            "pending": pending.quantize(Decimal('0.01')),
            "commission_count": len(commissions),
        }
    
    async def _calculate_agent_tier(self, agent_id: int) -> str:
        """
        Calculate agent's performance tier based on policy count
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Tier name (BRONZE, SILVER, GOLD, PLATINUM)
        """
        # Get policy count for last 12 months
        one_year_ago = datetime.now() - timedelta(days=365)
        
        stmt = select(func.count(Policy.id)).where(
            Policy.agent_id == agent_id,
            Policy.start_date >= one_year_ago,
            Policy.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        policy_count = result.scalar()
        
        if policy_count >= 201:
            return "PLATINUM"
        elif policy_count >= 101:
            return "GOLD"
        elif policy_count >= 51:
            return "SILVER"
        else:
            return "BRONZE"


from datetime import timedelta
