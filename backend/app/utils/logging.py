"""Logging utilities with structured logging and PII masking."""
import hashlib
import structlog
from typing import Any


def mask_phone(phone: str) -> str:
    """Mask phone to +91xxxxxxx890."""
    if not phone or len(phone) < 4:
        return "***"
    return f"+91{'x' * 7}{phone[-3:]}"


def mask_email(email: str) -> str:
    """Mask email to user***@domain.com."""
    if not email or "@" not in email:
        return "***"
    user, domain = email.split("@")
    return f"{user[:3]}***@{domain}"


def sanitize_log_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Remove or mask PII from log entries."""
    MASKED_FIELDS = {
        "phone": mask_phone,
        "email": mask_email,
        "password": lambda x: "***",
        "otp": lambda x: "***",
        "account_number": lambda x: f"XXXX{x[-4:] if x else ''}",
        "transaction_description": lambda x: "***",
    }

    for field, mask_fn in MASKED_FIELDS.items():
        if field in entry and entry[field]:
            try:
                entry[field] = mask_fn(str(entry[field]))
            except Exception:
                entry[field] = "***"

    return entry


def setup_structlog() -> None:
    """Configure structured logging."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a logger instance."""
    return structlog.get_logger(name)
