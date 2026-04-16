"""Document model for file management"""

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Index, Enum as SQLEnum, Text, BigInteger
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.enums.document import DocumentType, DocumentVerificationStatus


class Document(BaseModel):
    """
    Document model - manages all files and documents in the system
    """
    
    __tablename__ = "documents"
    
    # Document identification
    document_name = Column(String(255), nullable=False)
    document_type = Column(SQLEnum(DocumentType), nullable=False, index=True)
    
    # File details
    file_path = Column(String(500), nullable=False)  # S3 path or local path
    file_size = Column(BigInteger, nullable=True)  # in bytes
    mime_type = Column(String(100), nullable=True)
    file_extension = Column(String(10), nullable=True)
    
    # Related entities
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True, index=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Upload information
    upload_date = Column(DateTime, nullable=False, index=True)
    
    # Verification
    verification_status = Column(
        SQLEnum(DocumentVerificationStatus), 
        nullable=False, 
        default=DocumentVerificationStatus.PENDING,
        index=True
    )
    verified_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_date = Column(Date, nullable=True)
    
    # Description
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # S3 metadata
    s3_bucket = Column(String(255), nullable=True)
    s3_key = Column(String(500), nullable=True)
    s3_version_id = Column(String(255), nullable=True)
    
    # Relationships
    policy = relationship("Policy", foreign_keys=[policy_id])
    claim = relationship("Claim", back_populates="documents", foreign_keys=[claim_id])
    customer = relationship("Customer", foreign_keys=[customer_id])
    uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])
    verified_by = relationship("User", foreign_keys=[verified_by_id])
    
    # Indexes for high-volume table
    __table_args__ = (
        Index('idx_document_type', 'document_type'),
        Index('idx_document_policy', 'policy_id'),
        Index('idx_document_claim', 'claim_id'),
        Index('idx_document_customer', 'customer_id'),
        Index('idx_document_uploaded_by', 'uploaded_by_id'),
        Index('idx_document_verification', 'verification_status'),
        Index('idx_document_upload_date', 'upload_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, name={self.document_name}, type={self.document_type})>"
    
    @property
    def is_verified(self) -> bool:
        """Check if document has been verified"""
        return self.verification_status == DocumentVerificationStatus.VERIFIED
    
    @property
    def file_size_mb(self) -> float:
        """Return file size in megabytes"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0.0
