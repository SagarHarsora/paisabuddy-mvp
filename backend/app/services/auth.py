"""Authentication service."""
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
import jwt
import structlog

from app.config import settings
from app.utils.validators import hash_phone, normalize_phone
from app.utils.errors import APIError, ErrorCode

logger = structlog.get_logger(__name__)


class AuthService:
    """Handle authentication - OTP and JWT."""

    # In-memory OTP storage (replace with Redis in production)
    _otp_store: dict = {}
    _failed_attempts: dict = {}

    @classmethod
    def generate_otp(cls, phone: str) -> str:
        """Generate and store OTP for phone number."""
        phone = normalize_phone(phone)

        # Check rate limiting
        attempts_key = f"otp_failed:{phone}"
        failed_attempts = cls._failed_attempts.get(attempts_key, 0)

        if failed_attempts >= 5:
            logger.warning("otp_rate_limit", phone=phone)
            raise APIError(
                code=ErrorCode.OTP_RATE_LIMIT,
                message="Too many OTP requests. Try again in 10 minutes.",
                user_facing=True,
                status_code=429,
            )

        # Generate OTP
        otp = f"{secrets.randbelow(1000000):06d}"
        expiry = datetime.utcnow() + timedelta(minutes=10)

        # Store OTP
        cls._otp_store[phone] = {
            "otp": otp,
            "expiry": expiry,
            "attempts": 0,
        }

        logger.info("otp_generated", phone=phone)
        return otp

    @classmethod
    def verify_otp(cls, phone: str, otp: str) -> bool:
        """Verify OTP for phone number."""
        phone = normalize_phone(phone)

        if phone not in cls._otp_store:
            logger.warning("otp_not_found", phone=phone)
            raise APIError(
                code=ErrorCode.OTP_INVALID,
                message="Invalid OTP. Request a new one.",
                user_facing=True,
            )

        otp_data = cls._otp_store[phone]

        # Check expiry
        if datetime.utcnow() > otp_data["expiry"]:
            del cls._otp_store[phone]
            logger.warning("otp_expired", phone=phone)
            raise APIError(
                code=ErrorCode.OTP_EXPIRED,
                message="OTP has expired. Request a new one.",
                user_facing=True,
            )

        # Check attempts
        if otp_data["attempts"] >= 3:
            del cls._otp_store[phone]
            logger.warning("otp_max_attempts", phone=phone)
            raise APIError(
                code=ErrorCode.OTP_INVALID,
                message="Too many failed attempts. Request a new OTP.",
                user_facing=True,
            )

        # Verify OTP
        if otp_data["otp"] != otp:
            otp_data["attempts"] += 1
            logger.warning("otp_mismatch", phone=phone, attempt=otp_data["attempts"])
            raise APIError(
                code=ErrorCode.OTP_INVALID,
                message="Invalid OTP. Please try again.",
                user_facing=True,
            )

        # Clear OTP
        del cls._otp_store[phone]
        logger.info("otp_verified", phone=phone)
        return True

    @staticmethod
    def generate_jwt(user_id: str) -> str:
        """Generate JWT token for user."""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=settings.JWT_EXPIRY_DAYS),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        logger.info("jwt_generated", user_id=user_id)
        return token

    @staticmethod
    def verify_jwt(token: str) -> Optional[str]:
        """Verify JWT token and return user_id."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            user_id = payload.get("user_id")
            return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("jwt_expired")
            raise APIError(
                code=ErrorCode.JWT_EXPIRED,
                message="Token has expired. Please login again.",
                user_facing=True,
            )
        except jwt.InvalidTokenError:
            logger.warning("jwt_invalid")
            raise APIError(
                code=ErrorCode.JWT_INVALID,
                message="Invalid token. Please login again.",
                user_facing=True,
            )

    @staticmethod
    def hash_phone_with_salt(phone: str) -> tuple[str, str]:
        """Hash phone with random salt."""
        phone = normalize_phone(phone)
        salt = secrets.token_hex(16)
        phone_hash = hash_phone(phone, salt)
        return phone_hash, salt
