"""
Risk Scoring Service
Handles risk assessment and scoring for underwriting
"""

from decimal import Decimal
from datetime import datetime, date
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.customer import Customer
from app.models.vehicle import Vehicle
from app.models.property import Property
from app.models.claim import Claim
from app.enums.policy import PolicyType
from app.enums.vehicle import VehicleCondition
from app.enums.property import PropertyCondition


class RiskScorerService:
    """Service for calculating risk scores"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def calculate_auto_risk_score(
        self,
        customer: Customer,
        vehicle: Vehicle,
        driver_age: int,
        years_licensed: int,
        annual_mileage: int,
        has_violations: bool = False,
        violation_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate auto insurance risk score (0-100, higher = riskier)
        
        Returns risk score and underwriting recommendation
        """
        risk_score = 0
        
        # Age factor (0-25 points)
        if driver_age < 21:
            risk_score += 25
        elif driver_age < 25:
            risk_score += 18
        elif driver_age < 30:
            risk_score += 10
        elif driver_age > 70:
            risk_score += 12
        else:
            risk_score += 5
        
        # Experience factor (0-15 points)
        if years_licensed < 2:
            risk_score += 15
        elif years_licensed < 5:
            risk_score += 10
        else:
            risk_score += max(0, 10 - years_licensed)
        
        # Mileage factor (0-15 points)
        if annual_mileage > 20000:
            risk_score += 15
        elif annual_mileage > 15000:
            risk_score += 10
        else:
            risk_score += 5
        
        # Vehicle factors (0-20 points)
        vehicle_age = datetime.now().year - vehicle.year
        if vehicle_age > 15:
            risk_score += 12
        elif vehicle_age > 10:
            risk_score += 8
        else:
            risk_score += 3
        
        if vehicle.condition in [VehicleCondition.POOR, VehicleCondition.SALVAGE]:
            risk_score += 8
        
        # Violations (0-25 points)
        if has_violations:
            risk_score += min(25, violation_count * 8)
        
        # Claims history (async)
        claims_count = await self._get_customer_claims_count(customer.id)
        risk_score += min(15, claims_count * 5)
        
        # Determine recommendation
        if risk_score <= 30:
            recommendation = "APPROVED"
            rate_adjustment = "STANDARD"
        elif risk_score <= 50:
            recommendation = "APPROVED"
            rate_adjustment = "INCREASED"
        elif risk_score <= 70:
            recommendation = "CONDITIONAL"
            rate_adjustment = "HIGH"
        else:
            recommendation = "DECLINED"
            rate_adjustment = "N/A"
        
        return {
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "recommendation": recommendation,
            "rate_adjustment": rate_adjustment,
            "factors": {
                "driver_age": driver_age,
                "years_licensed": years_licensed,
                "annual_mileage": annual_mileage,
                "vehicle_age": vehicle_age,
                "violations": violation_count,
                "claims_history": claims_count,
            }
        }
    
    async def calculate_health_risk_score(
        self,
        customer: Customer,
        is_smoker: bool,
        has_pre_existing: bool,
        bmi: Optional[float] = None,
        occupation_risk: str = "LOW"
    ) -> Dict[str, Any]:
        """Calculate health insurance risk score"""
        risk_score = 0
        age = (date.today() - customer.date_of_birth).days // 365
        
        # Age factor (0-25 points)
        if age > 60:
            risk_score += 25
        elif age > 50:
            risk_score += 18
        elif age > 40:
            risk_score += 12
        else:
            risk_score += 5
        
        # Smoking (0-25 points)
        if is_smoker:
            risk_score += 25
        
        # Pre-existing conditions (0-20 points)
        if has_pre_existing:
            risk_score += 20
        
        # BMI factor (0-15 points)
        if bmi:
            if bmi > 35:
                risk_score += 15
            elif bmi > 30:
                risk_score += 10
            elif bmi < 18.5:
                risk_score += 8
        
        # Occupation (0-15 points)
        occupation_scores = {"LOW": 5, "MEDIUM": 10, "HIGH": 15}
        risk_score += occupation_scores.get(occupation_risk, 5)
        
        # Determine recommendation
        if risk_score <= 35:
            recommendation = "APPROVED"
        elif risk_score <= 60:
            recommendation = "CONDITIONAL"
        else:
            recommendation = "DECLINED"
        
        return {
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "recommendation": recommendation,
            "factors": {
                "age": age,
                "is_smoker": is_smoker,
                "has_pre_existing": has_pre_existing,
                "bmi": bmi,
                "occupation_risk": occupation_risk,
            }
        }
    
    async def calculate_property_risk_score(
        self,
        property_obj: Property,
        has_security: bool,
        has_fire_prevention: bool,
        flood_zone: bool = False,
        earthquake_zone: bool = False
    ) -> Dict[str, Any]:
        """Calculate property insurance risk score"""
        risk_score = 0
        
        # Property age (0-20 points)
        property_age = datetime.now().year - property_obj.year_built
        if property_age > 50:
            risk_score += 20
        elif property_age > 25:
            risk_score += 12
        else:
            risk_score += 5
        
        # Condition (0-20 points)
        if property_obj.condition == PropertyCondition.POOR:
            risk_score += 15
        elif property_obj.condition == PropertyCondition.DILAPIDATED:
            risk_score += 20
        else:
            risk_score += 5
        
        # Safety features (reduce risk)
        if has_security:
            risk_score -= 10
        if has_fire_prevention:
            risk_score -= 8
        
        # Natural disaster zones (0-30 points)
        if flood_zone:
            risk_score += 15
        if earthquake_zone:
            risk_score += 15
        
        # Claims history
        # TODO: Add property claims history lookup
        
        risk_score = max(0, risk_score)  # Ensure non-negative
        
        if risk_score <= 30:
            recommendation = "APPROVED"
        elif risk_score <= 50:
            recommendation = "CONDITIONAL"
        else:
            recommendation = "DECLINED"
        
        return {
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "recommendation": recommendation,
            "factors": {
                "property_age": property_age,
                "condition": property_obj.condition,
                "has_security": has_security,
                "has_fire_prevention": has_fire_prevention,
                "flood_zone": flood_zone,
                "earthquake_zone": earthquake_zone,
            }
        }
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Convert risk score to risk level"""
        if risk_score <= 25:
            return "LOW"
        elif risk_score <= 50:
            return "MEDIUM"
        elif risk_score <= 75:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    async def _get_customer_claims_count(self, customer_id: int) -> int:
        """Get number of claims for a customer in last 3 years"""
        three_years_ago = datetime.now() - timedelta(days=1095)
        
        stmt = select(func.count(Claim.id)).where(
            Claim.customer_id == customer_id,
            Claim.incident_date >= three_years_ago,
            Claim.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0


from datetime import timedelta
