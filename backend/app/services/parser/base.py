"""Base parser abstract class."""
from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class TransactionData(BaseModel):
    """Extracted transaction data."""

    date: str  # YYYY-MM-DD
    amount: float
    description: str
    is_debit: bool
    category: str  # Will be set by categorizer
    confidence: float = 1.0  # 0.00-1.00


class BaseParser(ABC):
    """Abstract base class for all PDF parsers."""

    @abstractmethod
    async def extract_transactions(self, pdf_content: bytes) -> List[TransactionData]:
        """Extract transactions from PDF."""
        pass

    @abstractmethod
    def detect_bank(self, pdf_content: bytes) -> str:
        """Detect bank from PDF."""
        pass
