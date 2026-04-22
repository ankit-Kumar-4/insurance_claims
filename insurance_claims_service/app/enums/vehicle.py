"""Vehicle-related enums"""

import enum


class BodyType(str, enum.Enum):
    """Vehicle body types"""
    SEDAN = "sedan"
    SUV = "suv"
    TRUCK = "truck"
    COUPE = "coupe"
    CONVERTIBLE = "convertible"
    HATCHBACK = "hatchback"
    WAGON = "wagon"
    VAN = "van"
    MINIVAN = "minivan"
    PICKUP = "pickup"
    SPORTS_CAR = "sports_car"
    MOTORCYCLE = "motorcycle"
    OTHER = "other"


class FuelType(str, enum.Enum):
    """Vehicle fuel types"""
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    PLUGIN_HYBRID = "plugin_hybrid"
    CNG = "cng"
    LPG = "lpg"
    HYDROGEN = "hydrogen"


class VehicleUsageType(str, enum.Enum):
    """How the vehicle is used"""
    PERSONAL = "personal"
    COMMERCIAL = "commercial"
    RIDE_SHARING = "ride_sharing"
    DELIVERY = "delivery"
    BUSINESS = "business"
    RENTAL = "rental"


class VehicleStatus(str, enum.Enum):
    """Vehicle status"""
    ACTIVE = "active"
    SOLD = "sold"
    TOTALED = "totaled"
    STOLEN = "stolen"
    SALVAGED = "salvaged"
    INACTIVE = "inactive"


class VehicleCondition(str, enum.Enum):
    """Vehicle condition"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    SALVAGE = "salvage"


# Alias for backwards compatibility
VehicleType = BodyType
