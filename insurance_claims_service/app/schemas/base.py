"""Base Pydantic schemas with common functionality"""

from datetime import datetime
from typing import Optional, TypeVar, Generic, List
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar('T')


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=False,
        str_strip_whitespace=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields"""
    created_date: datetime = Field(..., description="Creation timestamp")
    last_modified_date: datetime = Field(..., description="Last modification timestamp")


class ResponseSchema(TimestampSchema):
    """Base response schema with ID and timestamps"""
    id: int = Field(..., description="Unique identifier", gt=0)


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Page size")
    
    @property
    def skip(self) -> int:
        """Calculate skip value for database query"""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Get limit value"""
        return self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""
    items: List[T]
    total: int = Field(..., ge=0, description="Total number of items")
    skip: int = Field(..., ge=0, description="Number of items skipped")
    limit: int = Field(..., ge=1, description="Number of items per page")
    
    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
