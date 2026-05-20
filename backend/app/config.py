"""Application configuration and settings."""
import os
import logging
from typing import Optional
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/paisabuddy_dev",
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # AWS S3
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME", "paisabuddy-statements-dev")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    PDF_DELETION_DELAY_SECONDS: int = int(
        os.getenv("PDF_DELETION_DELAY_SECONDS", "60")
    )

    # JWT / Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRY_DAYS: int = int(os.getenv("JWT_EXPIRY_DAYS", "30"))

    # Messaging
    MSG91_AUTH_KEY: str = os.getenv("MSG91_AUTH_KEY", "")
    MSG91_TEMPLATE_ID_OTP: str = os.getenv("MSG91_TEMPLATE_ID_OTP", "")
    MSG91_WHATSAPP_AUTH_KEY: str = os.getenv("MSG91_WHATSAPP_AUTH_KEY", "")

    # Payments
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "")

    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG" if DEBUG else "INFO")

    # Parser
    PARSER_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("PARSER_CONFIDENCE_THRESHOLD", "0.75")
    )
    OCR_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.85")
    )

    class Config:
        env_file = ".env"


settings = Settings()


def init_sentry() -> None:
    """Initialize Sentry for error tracking and monitoring."""
    if not settings.SENTRY_DSN:
        print("⚠️  Sentry not configured. Set SENTRY_DSN to enable monitoring.")
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 1.0,
        profiles_sample_rate=0.1 if settings.ENVIRONMENT == "production" else 0.0,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            RedisIntegration(),
        ],
        attach_stacktrace=True,
        send_default_pii=False,
    )
    print("✓ Sentry initialized")


# Initialize Sentry on module load
init_sentry()
