"""CRUD operations for User"""

from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.security import verify_password, get_password_hash
from app.enums.user import UserStatus


class CRUDUser(CRUDBase[User]):
    """
    CRUD operations for User model
    
    Inherits all base CRUD operations and can be extended with
    entity-specific methods.
    """
    
    # ==================== CUSTOM METHODS ====================

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Get user by email address
        
        Args:
            db: Database session
            email: User's email address
            
        Returns:
            User object or None if not found
        """
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            db: Database session
            username: User's username
            
        Returns:
            User object or None if not found
        """
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_api_key(self, db: AsyncSession, api_key: str) -> Optional[User]:
        """
        Get user by API key
        
        Args:
            db: Database session
            api_key: User's API key
            
        Returns:
            User object or None if not found
        """
        result = await db.execute(
            select(User).where(User.api_key == api_key)
        )
        return result.scalar_one_or_none()

    async def authenticate(
        self, 
        db: AsyncSession, 
        email: str, 
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            email: User's email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def create_user(
        self,
        db: AsyncSession,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **kwargs
    ) -> User:
        """
        Create a new user with hashed password
        
        Args:
            db: Database session
            email: User's email
            password: Plain text password
            first_name: User's first name
            last_name: User's last name
            **kwargs: Additional user fields
            
        Returns:
            Created user object
        """
        hashed_password = get_password_hash(password)
        user_data = {
            "email": email,
            "password_hash": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            **kwargs
        }
        return await self.create(db, obj_in=user_data)

    async def update_password(
        self,
        db: AsyncSession,
        user: User,
        new_password: str
    ) -> User:
        """
        Update user's password
        
        Args:
            db: Database session
            user: User object
            new_password: New plain text password
            
        Returns:
            Updated user object
        """
        hashed_password = get_password_hash(new_password)
        return await self.update(
            db,
            db_obj=user,
            obj_in={"password_hash": hashed_password}
        )

    async def update_last_login(
        self,
        db: AsyncSession,
        user: User,
        ip_address: Optional[str] = None
    ) -> User:
        """
        Update user's last login timestamp
        
        Args:
            db: Database session
            user: User object
            ip_address: Optional IP address of login
            
        Returns:
            Updated user object
        """
        update_data = {"last_login": datetime.utcnow()}
        if ip_address:
            update_data["last_login_ip"] = ip_address
        return await self.update(db, db_obj=user, obj_in=update_data)

    async def verify_email(self, db: AsyncSession, user: User) -> User:
        """
        Mark user's email as verified
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            Updated user object
        """
        return await self.update(
            db,
            db_obj=user,
            obj_in={
                "is_verified": True,
                "email_verified_at": datetime.utcnow(),
                "email_verification_token": None,
                "status": UserStatus.ACTIVE
            }
        )

    async def set_password_reset_token(
        self,
        db: AsyncSession,
        user: User,
        token: str,
        expires: datetime
    ) -> User:
        """
        Set password reset token for user
        
        Args:
            db: Database session
            user: User object
            token: Password reset token
            expires: Token expiration time
            
        Returns:
            Updated user object
        """
        return await self.update(
            db,
            db_obj=user,
            obj_in={
                "password_reset_token": token,
                "password_reset_expires": expires
            }
        )

    async def is_active(self, user: User) -> bool:
        """
        Check if user is active
        
        Args:
            user: User object
            
        Returns:
            True if user is active, False otherwise
        """
        return user.status == UserStatus.ACTIVE and user.is_active


# Create global instance
user = CRUDUser(User)
