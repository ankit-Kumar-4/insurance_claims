"""Document schemas for API validation and serialization"""

from typing import Optional
from pydantic import Field

from app.schemas.base import BaseSchema, ResponseSchema
from app.enums.document import DocumentType


class DocumentBase(BaseSchema):
    """Base document schema"""
    document_type: DocumentType
    file_name: str = Field(..., min_length=1, max_length=255)
    file_path: str = Field(..., min_length=1, max_length=500)
    file_size: int = Field(..., gt=0)
    mime_type: str = Field(..., max_length=100)
    entity_type: Optional[str] = Field(None, max_length=50)
    entity_id: Optional[int] = Field(None, gt=0)


class DocumentCreate(DocumentBase):
    """Schema for creating a document"""
    pass


class DocumentUpdate(BaseSchema):
    """Schema for updating a document"""
    document_type: Optional[DocumentType] = None
    file_name: Optional[str] = Field(None, min_length=1, max_length=255)


class DocumentResponse(DocumentBase, ResponseSchema):
    """Schema for document response"""
    pass


class DocumentInDB(DocumentResponse):
    """Schema for document in database"""
    pass
