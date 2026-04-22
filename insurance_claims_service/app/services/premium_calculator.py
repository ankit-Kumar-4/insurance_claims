"""
Premium Calculation Service
Handles premium calculations for different insurance types
"""

from decimal import Decimal
from datetime import date, datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vehicle import Vehicle
from app.models.property import Property
from app.models.customer import Customer
from app.models.policy import Policy
from app.enums.policy import PolicyType, CoverageType
from app.enums.vehicle import VehicleCondition
from app.enums.property import PropertyCondition


class PremiumCalculatorService:
    """Service for calculating insurance premiums"""
    
    # Base rates per $1000 of coverage
    BASE_RATES = {
        PolicyType.AUTO: Decimal("0.015"),  # 1.5% of vehicle value
        PolicyType.HEALTH: Decimal("0.025"),  # 2.5% of coverage
        PolicyType.LIFE: Decimal("0.008"),  # 0.8% of coverage
        PolicyType.HOME: Decimal("0.012"),  # 1.2% of property value
        PolicyType.TRAVEL: Decimal("0.050"),  # 5% of trip cost
        PolicyType.BUSINESS: Decimal("0.020"),  # 2% of business value
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def calculate_auto_premium(
        self,
        vehicle: Vehicle,
        driver_age: int,
        coverage_amount: Decimal,
        deductible: Decimal,
        coverage_type: CoverageType,
        annual_mileage: Optional[int] = None,
        has_anti_theft: bool = False,
        has_airbags: bool = False,
        claims_history_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate auto insurance premium
        
        Args:
            vehicle: Vehicle model instance
            driver_age: Age of primary driver
            coverage_amount: Total coverage amount
            deductible: Deductible amount
            coverage_type: Type of coverage (LIABILITY, COLLISION, COMPREHENSIVE)
            annual_mileage: Expected annual mileage
            has_anti_theft: Whether vehicle has anti-theft system
            has_airbags: Whether vehicle has airbags
            claims_history_count: Number of past claims
            
        Returns:
            Dict with premium breakdown
        """
        # Base premium calculation
        base_rate = self.BASE_RATES[PolicyType.AUTO]
        base_premium = coverage_amount * base_rate
        
        # Age factor (younger and older drivers pay more)
        age_factor = self._calculate_age_factor(driver_age)
        
        # Vehicle age factor
        vehicle_age = datetime.now().year - vehicle.year
        vehicle_age_factor = self._calculate_vehicle_age_factor(vehicle_age)
        
        # Vehicle condition factor
        condition_factor = self._calculate_condition_factor(vehicle.condition)
        
        # Coverage type multiplier
        coverage_multiplier = self._get_coverage_multiplier(coverage_type)
        
        # Deductible discount (higher deductible = lower premium)
        deductible_discount = self._calculate_deductible_discount(deductible)
        
        # Mileage factor (more miles = higher risk)
        mileage_factor = self._calculate_mileage_factor(annual_mileage or 12000)
        
        # Safety features discount
        safety_discount = Decimal("1.0")
        if has_anti_theft:
            safety_discount -= Decimal("0.05")  # 5% discount
        if has_airbags:
            safety_discount -= Decimal("0.03")  # 3% discount
        
        # Claims history penalty
        claims_penalty = Decimal("1.0") + (Decimal(str(claims_history_count)) * Decimal("0.10"))
        
        # Calculate final premium
        premium = (
            base_premium *
            age_factor *
            vehicle_age_factor *
            condition_factor *
            coverage_multiplier *
            deductible_discount *
            mileage_factor *
            safety_discount *
            claims_penalty
        )
        
        # Round to 2 decimal places
        premium = premium.quantize(Decimal('0.01'))
        
        return {
            "total_premium": premium,
            "annual_premium": premium,
            "monthly_premium": (premium / Decimal("12")).quantize(Decimal('0.01')),
            "breakdown": {
                "base_premium": base_premium.quantize(Decimal('0.01')),
                "age_factor": float(age_factor),
                "vehicle_age_factor": float(vehicle_age_factor),
                "condition_factor": float(condition_factor),
                "coverage_multiplier": float(coverage_multiplier),
                "deductible_discount": float(deductible_discount),
                "mileage_factor": float(mileage_factor),
                "safety_discount": float(safety_discount),
                "claims_penalty": float(claims_penalty),
            }
        }
    
    async def calculate_health_premium(
        self,
        customer: Customer,
        coverage_amount: Decimal,
        deductible: Decimal,
        is_smoker: bool = False,
        has_pre_existing: bool = False,
        dependents_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate health insurance premium
        
        Args:
            customer: Customer model instance
            coverage_amount: Total coverage amount
            deductible: Deductible amount
            is_smoker: Whether customer is a smoker
            has_pre_existing: Whether customer has pre-existing conditions
            dependents_count: Number of dependents
            
        Returns:
            Dict with premium breakdown
        """
        # Calculate age from date of birth
        age = (date.today() - customer.date_of_birth).days // 365
        
        # Base premium
        base_rate = self.BASE_RATES[PolicyType.HEALTH]
        base_premium = coverage_amount * base_rate
        
        # Age factor (older = higher premium)
        age_factor = Decimal("1.0") + (Decimal(str(age)) * Decimal("0.015"))
        
        # Smoking penalty (50% increase)
        smoking_factor = Decimal("1.5") if is_smoker else Decimal("1.0")
        
        # Pre-existing conditions penalty (30% increase)
        preexisting_factor = Decimal("1.3") if has_pre_existing else Decimal("1.0")
        
        # Deductible discount
        deductible_discount = self._calculate_deductible_discount(deductible)
        
        # Dependents factor (discount for family plans)
        dependents_discount = Decimal("1.0")
        if dependents_count > 0:
            dependents_discount = Decimal("1.0") - (Decimal(str(min(dependents_count, 3))) * Decimal("0.05"))
        
        # Calculate final premium
        premium = (
            base_premium *
            age_factor *
            smoking_factor *
            preexisting_factor *
            deductible_discount *
            dependents_discount
        )
        
        premium = premium.quantize(Decimal('0.01'))
        
        return {
            "total_premium": premium,
            "annual_premium": premium,
            "monthly_premium": (premium / Decimal("12")).quantize(Decimal('0.01')),
            "breakdown": {
                "base_premium": base_premium.quantize(Decimal('0.01')),
                "age_factor": float(age_factor),
                "smoking_factor": float(smoking_factor),
                "preexisting_factor": float(preexisting_factor),
                "deductible_discount": float(deductible_discount),
                "dependents_discount": float(dependents_discount),
            }
        }
    
    async def calculate_life_premium(
        self,
        customer: Customer,
        coverage_amount: Decimal,
        term_years: int,
        is_smoker: bool = False,
        occupation_risk_level: str = "LOW"  # LOW, MEDIUM, HIGH
    ) -> Dict[str, Any]:
        """
        Calculate life insurance premium
        
        Args:
            customer: Customer model instance
            coverage_amount: Death benefit amount
            term_years: Term length in years
            is_smoker: Whether customer is a smoker
            occupation_risk_level: Risk level of occupation
            
        Returns:
            Dict with premium breakdown
        """
        # Calculate age
        age = (date.today() - customer.date_of_birth).days // 365
        
        # Base premium per $1000 of coverage
        base_rate = self.BASE_RATES[PolicyType.LIFE]
        base_premium = (coverage_amount / Decimal("1000")) * base_rate * Decimal(str(term_years))
        
        # Age factor (exponential increase with age)
        if age < 30:
            age_factor = Decimal("0.8")
        elif age < 40:
            age_factor = Decimal("1.0")
        elif age < 50:
            age_factor = Decimal("1.3")
        elif age < 60:
            age_factor = Decimal("1.8")
        else:
            age_factor = Decimal("2.5")
        
        # Smoking penalty (100% increase)
        smoking_factor = Decimal("2.0") if is_smoker else Decimal("1.0")
        
        # Occupation risk factor
        occupation_factors = {
            "LOW": Decimal("1.0"),
            "MEDIUM": Decimal("1.2"),
            "HIGH": Decimal("1.5")
        }
        occupation_factor = occupation_factors.get(occupation_risk_level, Decimal("1.0"))
        
        # Calculate annual premium
        annual_premium = (
            base_premium *
            age_factor *
            smoking_factor *
            occupation_factor
        )
        
        annual_premium = annual_premium.quantize(Decimal('0.01'))
        
        return {
            "total_premium": annual_premium * Decimal(str(term_years)),
            "annual_premium": annual_premium,
            "monthly_premium": (annual_premium / Decimal("12")).quantize(Decimal('0.01')),
            "term_years": term_years,
            "breakdown": {
                "base_premium": base_premium.quantize(Decimal('0.01')),
                "age_factor": float(age_factor),
                "smoking_factor": float(smoking_factor),
                "occupation_factor": float(occupation_factor),
            }
        }
    
    async def calculate_property_premium(
        self,
        property_obj: Property,
        coverage_amount: Decimal,
        deductible: Decimal,
        has_security_system: bool = False,
        has_fire_prevention: bool = False,
        claims_history_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate property/home insurance premium
        
        Args:
            property_obj: Property model instance
            coverage_amount: Total coverage amount
            deductible: Deductible amount
            has_security_system: Whether property has security system
            has_fire_prevention: Whether property has fire prevention system
            claims_history_count: Number of past claims
            
        Returns:
            Dict with premium breakdown
        """
        # Base premium
        base_rate = self.BASE_RATES[PolicyType.HOME]
        base_premium = coverage_amount * base_rate
        
        # Property age factor
        property_age = datetime.now().year - property_obj.year_built
        if property_age < 10:
            age_factor = Decimal("0.9")
        elif property_age < 25:
            age_factor = Decimal("1.0")
        elif property_age < 50:
            age_factor = Decimal("1.2")
        else:
            age_factor = Decimal("1.4")
        
        # Property condition factor
        condition_factor = self._calculate_condition_factor(property_obj.condition)
        
        # Deductible discount
        deductible_discount = self._calculate_deductible_discount(deductible)
        
        # Safety features discount
        safety_discount = Decimal("1.0")
        if has_security_system:
            safety_discount -= Decimal("0.10")  # 10% discount
        if has_fire_prevention:
            safety_discount -= Decimal("0.08")  # 8% discount
        
        # Claims history penalty
        claims_penalty = Decimal("1.0") + (Decimal(str(claims_history_count)) * Decimal("0.15"))
        
        # Calculate final premium
        premium = (
            base_premium *
            age_factor *
            condition_factor *
            deductible_discount *
            safety_discount *
            claims_penalty
        )
        
        premium = premium.quantize(Decimal('0.01'))
        
        return {
            "total_premium": premium,
            "annual_premium": premium,
            "monthly_premium": (premium / Decimal("12")).quantize(Decimal('0.01')),
            "breakdown": {
                "base_premium": base_premium.quantize(Decimal('0.01')),
                "age_factor": float(age_factor),
                "condition_factor": float(condition_factor),
                "deductible_discount": float(deductible_discount),
                "safety_discount": float(safety_discount),
                "claims_penalty": float(claims_penalty),
            }
        }
    
    def _calculate_age_factor(self, age: int) -> Decimal:
        """Calculate age-based risk factor for auto insurance"""
        if age < 21:
            return Decimal("1.8")  # High risk
        elif age < 25:
            return Decimal("1.4")
        elif age < 30:
            return Decimal("1.1")
        elif age < 65:
            return Decimal("1.0")  # Base rate
        else:
            return Decimal("1.2")  # Slightly higher for seniors
    
    def _calculate_vehicle_age_factor(self, vehicle_age: int) -> Decimal:
        """Calculate vehicle age factor"""
        if vehicle_age < 3:
            return Decimal("1.0")
        elif vehicle_age < 7:
            return Decimal("1.1")
        elif vehicle_age < 12:
            return Decimal("1.2")
        else:
            return Decimal("1.3")
    
    def _calculate_condition_factor(self, condition: Optional[str]) -> Decimal:
        """Calculate condition-based factor"""
        condition_map = {
            VehicleCondition.EXCELLENT: Decimal("0.9"),
            VehicleCondition.GOOD: Decimal("1.0"),
            VehicleCondition.FAIR: Decimal("1.1"),
            VehicleCondition.POOR: Decimal("1.3"),
            VehicleCondition.SALVAGE: Decimal("1.5"),
            PropertyCondition.EXCELLENT: Decimal("0.9"),
            PropertyCondition.GOOD: Decimal("1.0"),
            PropertyCondition.FAIR: Decimal("1.1"),
            PropertyCondition.POOR: Decimal("1.3"),
            PropertyCondition.DILAPIDATED: Decimal("1.6"),
        }
        return condition_map.get(condition, Decimal("1.0"))
    
    def _get_coverage_multiplier(self, coverage_type: CoverageType) -> Decimal:
        """Get coverage type multiplier"""
        multipliers = {
            CoverageType.LIABILITY: Decimal("0.8"),
            CoverageType.COLLISION: Decimal("1.0"),
            CoverageType.COMPREHENSIVE: Decimal("1.3"),
            CoverageType.PERSONAL_INJURY: Decimal("1.1"),
            CoverageType.PROPERTY_DAMAGE: Decimal("0.9"),
        }
        return multipliers.get(coverage_type, Decimal("1.0"))
    
    def _calculate_deductible_discount(self, deductible: Decimal) -> Decimal:
        """Calculate discount based on deductible amount"""
        if deductible >= Decimal("2000"):
            return Decimal("0.85")  # 15% discount
        elif deductible >= Decimal("1000"):
            return Decimal("0.90")  # 10% discount
        elif deductible >= Decimal("500"):
            return Decimal("0.95")  # 5% discount
        else:
            return Decimal("1.0")  # No discount
    
    def _calculate_mileage_factor(self, annual_mileage: int) -> Decimal:
        """Calculate mileage-based factor"""
        if annual_mileage < 5000:
            return Decimal("0.9")
        elif annual_mileage < 10000:
            return Decimal("1.0")
        elif annual_mileage < 15000:
            return Decimal("1.1")
        elif annual_mileage < 20000:
            return Decimal("1.2")
        else:
            return Decimal("1.3")
