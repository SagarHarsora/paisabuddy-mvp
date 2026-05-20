"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog
from datetime import datetime

from app.database import get_db
from app.models import User
from app.api.schemas import RequestOTPRequest, VerifyOTPRequest, AuthResponse
from app.services.auth import AuthService
from app.utils.errors import APIError, ErrorCode
from app.utils.validators import validate_phone, normalize_phone
from app.utils.logging import mask_phone
from app.config import settings

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/request-otp")
async def request_otp(req: RequestOTPRequest, db: AsyncSession = Depends(get_db)):
    """Request OTP for phone number."""
    logger.info("request_otp", phone=mask_phone(req.phone), language=req.language)

    # Validate phone
    if not validate_phone(req.phone):
        logger.warning("invalid_phone_format", phone=mask_phone(req.phone))
        raise APIError(
            code=ErrorCode.A007,
            message="Invalid phone number format. Use +919876543210 or 9876543210.",
            user_facing=True,
            status_code=400,
        )

    try:
        # Generate OTP
        otp = AuthService.generate_otp(req.phone)

        # TODO: Send OTP via MSG91 API
        # For now, return OTP in response (dev only)
        logger.info("otp_request_success", phone=mask_phone(req.phone))

        return {
            "success": True,
            "data": {
                "message": "OTP sent to your phone number",
                "phone": mask_phone(req.phone),
                "otp_debug": otp if req.phone.endswith("test") else None,  # Dev only
            },
        }

    except APIError:
        raise
    except Exception as e:
        logger.exception("otp_request_failed", error=type(e).__name__)
        raise APIError(
            code=ErrorCode.E500,
            message="Failed to send OTP. Please try again.",
            user_facing=True,
            status_code=500,
        )


@router.post("/verify-otp", response_model=AuthResponse)
async def verify_otp(req: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify OTP and return JWT token."""
    logger.info("verify_otp", phone=mask_phone(req.phone))

    # Validate phone
    if not validate_phone(req.phone):
        raise APIError(
            code=ErrorCode.A001,
            message="Invalid phone number.",
            user_facing=True,
        )

    try:
        # Verify OTP
        AuthService.verify_otp(req.phone, req.otp)

        # Get or create user
        phone = normalize_phone(req.phone)
        phone_hash, salt = AuthService.hash_phone_with_salt(phone)

        # Check if user exists
        result = await db.execute(select(User).where(User.phone_hash == phone_hash))
        user = result.scalars().first()

        if not user:
            # Create new user
            user = User(phone_hash=phone_hash, phone_salt=salt, language="en")
            db.add(user)
            await db.flush()
            logger.info("user_created", user_id=str(user.id))
        else:
            logger.info("user_exists", user_id=str(user.id))

        # Update last login
        user.last_login_at = __import__("datetime").datetime.utcnow()
        await db.flush()

        # Generate JWT
        token = AuthService.generate_jwt(str(user.id))

        logger.info("verify_otp_success", user_id=str(user.id))

        return AuthResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRY_DAYS * 86400,
        )

    except APIError:
        raise
    except Exception as e:
        logger.exception("verify_otp_failed", error=type(e).__name__)
        raise APIError(
            code=ErrorCode.E500,
            message="Authentication failed. Please try again.",
            user_facing=True,
            status_code=500,
        )


# Dependency for protected routes
async def get_current_user(
    token: str = None, db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT."""
    if not token:
        raise APIError(
            code=ErrorCode.JWT_INVALID,
            message="Missing authentication token.",
            user_facing=True,
            status_code=401,
        )

    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]

    user_id = AuthService.verify_jwt(token)

    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise APIError(
            code=ErrorCode.A004,
            message="User not found.",
            user_facing=True,
            status_code=404,
        )

    return user
