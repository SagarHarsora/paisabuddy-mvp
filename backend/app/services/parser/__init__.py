"""Parser package."""
from app.services.parser.base import BaseParser, TransactionData
from app.services.parser.digital import DigitalPDFParser

__all__ = ["BaseParser", "TransactionData", "DigitalPDFParser"]
