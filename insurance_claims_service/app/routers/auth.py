"""
Authentication router with endpoints for login, register, password management, etc.
"""

from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import user as user_crud
from app.schemas.auth import (
    Token,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.user import UserResponse
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    create_password_reset_token,
    verify_password_reset_token,
    create_email_verification_token,
    verify_email_verification_token,
    verify_password,
)
from app.dependencies import get_current_user, get_current_active_user
from app.models.user import User
from app.enums.user import UserRole, UserStatus

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Login with email and password
    
    Returns access token and refresh token
    """
    # Authenticate user
    user = await user_crud.authenticate(db, email=credentials.email, password=credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    # Check if account is locked
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked due to too many failed login attempts"
        )
    
    # Update last login
    ip_address = request.client.host if request.client else None
    await user_crud.update_last_login(db, user=user, ip_address=ip_address)
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800,  # 30 minutes
        user=UserResponse.model_validate(user)
    )


@router.post("/register", response_model=LoginResponse)
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Register a new user
    
    Returns access token and refresh token
    """
    # Check if email already exists
    existing_user = await user_crud.get_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists (if provided)
    if user_data.username:
        existing_username = await user_crud.get_by_username(db, username=user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create user
    user = await user_crud.create_user(
        db,
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        phone_number=user_data.phone,
        role=UserRole.CUSTOMER,  # Default role for registration
        status=UserStatus.PENDING_ACTIVATION
    )
    
    # Create email verification token (for future implementation)
    # verification_token = create_email_verification_token(user.email)
    # TODO: Send verification email
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800,
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token
    """
    # Decode refresh token
    payload = decode_token(token_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    user = await user_crud.get(db, id=user_id)
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Logout current user
    
    In a full implementation, this would invalidate the token
    (e.g., add to blacklist in Redis)
    """
    # TODO: Implement token blacklist in Redis
    return {"message": "Successfully logged out"}


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Change current user's password
    """
    # Verify old password
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    # Update password
    await user_crud.update_password(db, user=current_user, new_password=password_data.new_password)
    
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(
    request_data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Request password reset
    
    Sends password reset email to user
    """
    # Get user by email
    user = await user_crud.get_by_email(db, email=request_data.email)
    
    # Always return success (don't reveal if email exists)
    if not user:
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # Create password reset token
    reset_token = create_password_reset_token(user.email)
    expires = datetime.utcnow() + timedelta(hours=1)
    
    # Save token to database
    await user_crud.set_password_reset_token(
        db,
        user=user,
        token=reset_token,
        expires=expires
    )
    
    # TODO: Send password reset email with reset_token
    # Email should contain link: /reset-password?token={reset_token}
    
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Reset password using reset token
    """
    # Verify reset token
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Get user by email
    user = await user_crud.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if token matches and hasn't expired
    if (user.password_reset_token != reset_data.token or 
        not user.password_reset_expires or 
        user.password_reset_expires < datetime.utcnow()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Update password and clear reset token
    await user_crud.update_password(db, user=user, new_password=reset_data.new_password)
    await user_crud.update(
        db,
        db_obj=user,
        obj_in={
            "password_reset_token": None,
            "password_reset_expires": None
        }
    )
    
    return {"message": "Password reset successfully"}


@router.post("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Verify user's email address
    """
    # Verify token
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Get user
    user = await user_crud.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify email
    await user_crud.verify_email(db, user=user)
    
    return {"message": "Email verified successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user's profile
    """
    return UserResponse.model_validate(current_user)


@router.post("/resend-verification")
async def resend_verification_email(
    email: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Resend email verification link
    """
    user = await user_crud.get_by_email(db, email=email)
    
    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a verification link has been sent"}
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    # Create new verification token
    verification_token = create_email_verification_token(user.email)
    
    # TODO: Send verification email with verification_token
    # Email should contain link: /verify-email?token={verification_token}
    
    return {"message": "If the email exists, a verification link has been sent"}
