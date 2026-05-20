"""Database models."""
import uuid
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Date, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_hash = Column(String(64), unique=True, nullable=False, index=True)
    phone_salt = Column(String(32), nullable=False)
    language = Column(String(10), default="en")  # 'en' or 'hi'
    whatsapp_opted_in = Column(Boolean, default=False)
    subscription_tier = Column(String(20), default="free")  # 'free', 'basic', 'pro'
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    last_upload_at = Column(DateTime, nullable=True)

    # Relationships
    statements = relationship("Statement", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class Statement(Base):
    """Bank statement model."""

    __tablename__ = "statements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    bank = Column(String(20), nullable=False)  # 'hdfc', 'sbi', 'union_bank', etc.
    statement_type = Column(String(20), nullable=False)  # 'digital', 'scanned'
    months_covered = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, index=True)
    pdf_deleted_at = Column(DateTime, nullable=True)
    parse_status = Column(String(20), default="pending")  # 'pending', 'processing', 'done', 'failed'
    parse_error = Column(String(500), nullable=True)
    transaction_count = Column(Integer, default=0)
    accuracy_score = Column(Numeric(3, 2), nullable=True)  # 0.00-1.00

    # Relationships
    user = relationship("User", back_populates="statements")
    transactions = relationship("Transaction", back_populates="statement")

    __table_args__ = (
        Index("ix_user_uploaded", user_id, uploaded_at),
    )


class Transaction(Base):
    """Transaction model."""

    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    statement_id = Column(UUID(as_uuid=True), ForeignKey("statements.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(500), nullable=False)
    category = Column(String(30), nullable=False, index=True)  # 'food', 'transport', 'emi', 'salary', 'bill', 'entertainment', 'shopping', 'other'
    is_debit = Column(Boolean, nullable=False)
    is_emi = Column(Boolean, default=False)
    is_salary = Column(Boolean, default=False)
    confidence = Column(Numeric(3, 2), nullable=True)  # 0.00-1.00 (OCR confidence)
    corrected_by_user = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    statement = relationship("Statement", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

    __table_args__ = (
        Index("ix_user_date", user_id, date),
        Index("ix_user_category", user_id, category),
    )


class Report(Base):
    """Monthly report model."""

    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    statement_id = Column(UUID(as_uuid=True), ForeignKey("statements.id"), nullable=False)
    month = Column(Date, nullable=False)  # First day of month
    paisa_score = Column(Integer, nullable=False)  # 0-100
    total_income = Column(Numeric(12, 2), nullable=False)
    total_expense = Column(Numeric(12, 2), nullable=False)
    savings_rate = Column(Numeric(5, 2), nullable=False)  # 0-100 (percentage)
    narrative = Column(String(2000), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_user_month", user_id, month),
    )
