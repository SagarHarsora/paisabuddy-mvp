"""API schemas for request/response validation."""
from typing import Any, Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal


# Error responses
class ErrorDetail(BaseModel):
    """Error response detail."""

    code: str
    message: str
    user_facing: bool = True


class APIResponse(BaseModel):
    """Standard API response wrapper."""

    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None


# Health check
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    environment: str


# Auth schemas
class RequestOTPRequest(BaseModel):
    """Request OTP schema."""

    phone: str = Field(..., description="Phone number in format +91XXXXXXXXXX or 91XXXXXXXXXX or XXXXXXXXXX")
    language: str = Field(default="en", pattern="^(en|hi)$")


class VerifyOTPRequest(BaseModel):
    """Verify OTP schema."""

    phone: str
    otp: str = Field(..., min_length=4, max_length=6)


class AuthResponse(BaseModel):
    """Authentication response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Upload schemas
class UploadResponse(BaseModel):
    """Upload response."""

    statement_id: str
    bank: str
    status: str  # 'pending', 'processing', 'done', 'failed'
    message: str


# Transaction schema
class TransactionResponse(BaseModel):
    """Transaction data in report."""

    date: str
    description: str
    amount: float
    category: str
    is_debit: bool


# Report schemas
class CategoryBreakdown(BaseModel):
    """Category spending breakdown."""

    category: str
    amount: float
    percentage: float
    transaction_count: int


class ReportResponse(BaseModel):
    """Monthly report response."""

    statement_id: str
    bank: str
    month: str  # YYYY-MM
    paisa_score: int
    total_income: float
    total_expense: float
    savings_rate: float
    narrative: str
    categories: List[CategoryBreakdown]
    transactions: List[TransactionResponse]
    generated_at: str


# List reports
class ReportListItem(BaseModel):
    """Report list item."""

    statement_id: str
    bank: str
    month: str
    paisa_score: int
    generated_at: str


class ReportsListResponse(BaseModel):
    """List of reports response."""

    reports: List[ReportListItem]
    total: int
