"""Error codes and exception handling."""
from enum import Enum
from typing import Any, Optional


class ErrorCode(str, Enum):
    """Standardized error codes for all API responses."""

    # Auth errors (A001–A099)
    OTP_INVALID = "A001"
    OTP_EXPIRED = "A002"
    OTP_RATE_LIMIT = "A003"
    PHONE_NOT_REGISTERED = "A004"
    JWT_INVALID = "A005"
    JWT_EXPIRED = "A006"
    PHONE_ALREADY_EXISTS = "A007"

    # Upload errors (U001–U099)
    FILE_NOT_PDF = "U001"
    FILE_CORRUPTED = "U002"
    FILE_TOO_LARGE = "U003"
    FILE_ENCRYPTION_FAILED = "U004"
    UPLOAD_RATE_LIMIT = "U005"

    # Parser errors (P001–P099)
    BANK_NOT_DETECTED = "P001"
    PARSER_CRASHED = "P002"
    OCR_LOW_CONFIDENCE = "P003"
    NO_TRANSACTIONS_FOUND = "P004"

    # Database errors (D001–D099)
    DB_CONNECTION_FAILED = "D001"
    DB_TRANSACTION_FAILED = "D002"

    # External service errors (E001–E099)
    S3_UPLOAD_FAILED = "E001"
    MSG91_API_ERROR = "E002"
    RAZORPAY_API_ERROR = "E003"

    # Unknown/server errors
    INTERNAL_ERROR = "E500"


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        user_facing: bool = True,
        status_code: int = 400,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        self.code = code
        self.message = message
        self.user_facing = user_facing
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
