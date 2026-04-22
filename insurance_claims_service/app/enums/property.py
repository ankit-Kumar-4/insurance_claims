"""Property-related enums"""

import enum


class PropertyType(str, enum.Enum):
    """Types of properties"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    MIXED_USE = "mixed_use"
    VACANT_LAND = "vacant_land"


class StructureType(str, enum.Enum):
    """Types of property structures"""
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    OFFICE = "office"
    WAREHOUSE = "warehouse"
    RETAIL_STORE = "retail_store"
    FACTORY = "factory"
    STORAGE_FACILITY = "storage_facility"
    FARM_BUILDING = "farm_building"
    OTHER = "other"


class ConstructionType(str, enum.Enum):
    """Types of construction materials"""
    WOOD = "wood"
    BRICK = "brick"
    CONCRETE = "concrete"
    STEEL = "steel"
    STONE = "stone"
    MIXED = "mixed"
    PREFABRICATED = "prefabricated"


class PropertyStatus(str, enum.Enum):
    """Property status"""
    ACTIVE = "active"
    SOLD = "sold"
    DEMOLISHED = "demolished"
    UNDER_CONSTRUCTION = "under_construction"
    CONDEMNED = "condemned"
    INACTIVE = "inactive"


class PropertyCondition(str, enum.Enum):
    """Property condition"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DILAPIDATED = "dilapidated"
