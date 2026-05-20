"""Input validation utilities."""
import re
from typing import Optional


def validate_phone(phone: str) -> bool:
    """Validate Indian phone number."""
    # Accept: +919999999999, 919999999999, 9999999999
    phone = phone.strip()
    if phone.startswith("+91"):
        phone = phone[3:]
    elif phone.startswith("91"):
        phone = phone[2:]

    return len(phone) == 10 and phone.isdigit()


def validate_email(email: str) -> bool:
    """Validate email address."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_pdf_filename(filename: str) -> bool:
    """Validate PDF file."""
    return filename.lower().endswith(".pdf")


def normalize_phone(phone: str) -> str:
    """Normalize phone to +91XXXXXXXXXX format."""
    phone = phone.strip()
    if phone.startswith("+91"):
        return phone
    elif phone.startswith("91"):
        return f"+{phone}"
    else:
        return f"+91{phone}"


def hash_phone(phone: str, salt: str) -> str:
    """Hash phone number with salt."""
    import hashlib

    full_string = f"{phone}{salt}"
    return hashlib.sha256(full_string.encode()).hexdigest()
