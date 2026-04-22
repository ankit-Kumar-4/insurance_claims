"""
FastAPI dependencies for authentication and authorization
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.security import decode_token
from app.crud import user as user_crud
from app.models.user import User
from app.enums.user import UserRole, UserStatus

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token
    
    Args:
        token: JWT access token from Authorization header
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    # Check token type
    if payload.get("type") != "access":
        raise credentials_exception
    
    # Get user ID from token
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    user = await user_crud.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (enforces active status)
    
    Args:
        current_user: Current user from get_current_user dependency
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is not active
    """
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


class RoleChecker:
    """
    Dependency class for role-based access control
    """
    
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles
    
    async def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        Check if user has required role
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            Current user if role is allowed
            
        Raises:
            HTTPException: If user doesn't have required role
        """
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user


# Pre-defined role checkers for common access patterns
require_super_admin = RoleChecker([UserRole.SUPER_ADMIN])
require_admin = RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN])
require_agent = RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.AGENT])
require_underwriter = RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.UNDERWRITER])
require_customer = RoleChecker([UserRole.CUSTOMER])
require_auditor = RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.AUDITOR])
require_support = RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER_SERVICE])


def has_permission(user: User, required_roles: list[UserRole]) -> bool:
    """
    Check if user has any of the required roles
    
    Args:
        user: User object
        required_roles: List of allowed roles
        
    Returns:
        True if user has permission, False otherwise
    """
    return user.role in required_roles


def is_admin_or_owner(user: User, resource_user_id: int) -> bool:
    """
    Check if user is admin or owns the resource
    
    Args:
        user: Current user
        resource_user_id: User ID of resource owner
        
    Returns:
        True if user has access, False otherwise
    """
    if user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        return True
    return user.id == resource_user_id


def can_access_customer_data(user: User, customer_user_id: int) -> bool:
    """
    Check if user can access customer data
    - Admins can access all
    - Agents can access their assigned customers
    - Customers can access their own data
    
    Args:
        user: Current user
        customer_user_id: Customer's user ID
        
    Returns:
        True if user has access, False otherwise
    """
    if user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        return True
    if user.role == UserRole.CUSTOMER and user.id == customer_user_id:
        return True
    # TODO: Add agent-customer assignment check
    return False


def can_manage_policies(user: User) -> bool:
    """
    Check if user can manage policies
    
    Args:
        user: Current user
        
    Returns:
        True if user can manage policies
    """
    return user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.AGENT, UserRole.UNDERWRITER]


def can_approve_claims(user: User) -> bool:
    """
    Check if user can approve claims
    
    Args:
        user: Current user
        
    Returns:
        True if user can approve claims
    """
    return user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.UNDERWRITER]


def can_process_payments(user: User) -> bool:
    """
    Check if user can process payments
    
    Args:
        user: Current user
        
    Returns:
        True if user can process payments
    """
    return user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]
