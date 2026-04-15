"""User model for authentication and authorization"""

from sqlalchemy import Column, String, Boolean, DateTime, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel
from app.enums.user import UserRole, UserStatus


class User(BaseModel):
    """
    User model for authentication and authorization
    Supports multiple roles: admin, agent, customer, underwriter, etc.
    """
    
    __tablename__ = "users"
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile fields
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    
    # Role and status
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.CUSTOMER, index=True)
    status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.PENDING_ACTIVATION, index=True)
    
    # Security fields
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Password reset
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    # Email verification
    email_verification_token = Column(String(255), nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    
    # Login tracking
    last_login = Column(DateTime, nullable=True)
    last_login_ip = Column(String(50), nullable=True)
    failed_login_attempts = Column(String(10), default="0", nullable=False)
    locked_until = Column(DateTime, nullable=True)
    
    # API key for integrations
    api_key = Column(String(255), unique=True, nullable=True, index=True)
    api_key_expires = Column(DateTime, nullable=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role_status', 'role', 'status'),
        Index('idx_user_active', 'is_active'),
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def full_name(self) -> str:
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is locked"""
        if self.locked_until:
            return self.locked_until > datetime.utcnow()
        return False
    
    def has_role(self, role: UserRole) -> bool:
        """Check if user has specific role"""
        return self.role == role
    
    def is_admin(self) -> bool:
        """Check if user has admin privileges"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]
