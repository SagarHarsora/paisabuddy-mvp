"""Digital PDF parser for HDFC, SBI, Union Bank statements."""
from typing import List, Optional
import pdfplumber
import structlog
from datetime import datetime

from app.services.parser.base import BaseParser, TransactionData
from app.utils.errors import APIError, ErrorCode
from app.config import settings

logger = structlog.get_logger(__name__)


class DigitalPDFParser(BaseParser):
    """Parser for digital bank statements (PDF tables)."""

    BANK_KEYWORDS = {
        "hdfc": ["HDFC Bank", "HDFC", "hdfc"],
        "sbi": ["State Bank of India", "SBI", "sbi"],
        "union_bank": ["Union Bank", "UNION BANK", "union"],
        "icici": ["ICICI", "icici"],
        "axis": ["Axis Bank", "AXIS", "axis"],
    }

    async def extract_transactions(self, pdf_content: bytes) -> List[TransactionData]:
        """Extract transactions from digital PDF."""
        logger.info("extract_start", size_kb=len(pdf_content) // 1024)

        transactions: List[TransactionData] = []

        try:
            with pdfplumber.open(pdf_content) as pdf:
                if not pdf.pages:
                    logger.warning("empty_pdf")
                    raise APIError(
                        code=ErrorCode.NO_TRANSACTIONS_FOUND,
                        message="Your PDF has no pages. Please upload a valid bank statement.",
                        user_facing=True,
                    )

                # Process each page
                for page_num, page in enumerate(pdf.pages, 1):
                    logger.debug("processing_page", page=page_num, total=len(pdf.pages))

                    # Extract tables from page
                    tables = page.extract_tables()
                    if not tables:
                        logger.debug("no_tables_on_page", page=page_num)
                        continue

                    # Parse each table
                    for table in tables:
                        if not table or len(table) < 2:
                            continue

                        # Skip header row
                        for row in table[1:]:
                            tx = self._parse_row(row)
                            if tx:
                                transactions.append(tx)

            if not transactions:
                logger.warning("no_transactions_extracted")
                raise APIError(
                    code=ErrorCode.NO_TRANSACTIONS_FOUND,
                    message="No transactions found in this PDF. This might not be a bank statement.",
                    user_facing=True,
                )

            logger.info("extract_success", count=len(transactions))
            return transactions

        except pdfplumber.PDFException as e:
            logger.error("pdf_exception", error=str(e))
            raise APIError(
                code=ErrorCode.FILE_CORRUPTED,
                message="Your PDF seems damaged. Try downloading it again from your bank's app.",
                user_facing=True,
            )
        except APIError:
            raise
        except Exception as e:
            logger.exception("unexpected_error", error=type(e).__name__)
            raise APIError(
                code=ErrorCode.PARSER_CRASHED,
                message="Something went wrong while reading your PDF. Our team has been notified.",
                user_facing=True,
                status_code=500,
            )

    def _parse_row(self, row: List[str]) -> Optional[TransactionData]:
        """Parse a single transaction row."""
        try:
            if not row or len(row) < 3:
                return None

            # Clean and extract data
            date_str = str(row[0]).strip() if row[0] else None
            description = str(row[1]).strip() if row[1] else None
            amount_str = str(row[2]).strip() if row[2] else None

            if not all([date_str, description, amount_str]):
                return None

            # Parse date
            try:
                # Try common formats: DD-Mon-YYYY, DD-MM-YYYY, DD/MM/YYYY
                for fmt in ["%d-%b-%Y", "%d-%m-%Y", "%d/%m/%Y"]:
                    try:
                        date_obj = datetime.strptime(date_str, fmt)
                        date_formatted = date_obj.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
                else:
                    # If no format matches, skip this row
                    return None
            except Exception:
                return None

            # Parse amount
            try:
                # Remove currency symbols and commas
                clean_amount = (
                    amount_str.replace("₹", "")
                    .replace("Rs.", "")
                    .replace(",", "")
                    .strip()
                )
                amount = float(clean_amount)
            except ValueError:
                return None

            # Determine if debit or credit
            # Usually: debit shows as positive, credit as separate column or shows as credit
            is_debit = amount > 0

            return TransactionData(
                date=date_formatted,
                amount=abs(amount),
                description=description,
                is_debit=is_debit,
                category="other",  # Will be categorized separately
                confidence=1.0,
            )

        except Exception as e:
            logger.debug("row_parse_failed", error=str(e))
            return None

    def detect_bank(self, pdf_content: bytes) -> str:
        """Detect bank from PDF content."""
        try:
            with pdfplumber.open(pdf_content) as pdf:
                if not pdf.pages:
                    return "unknown"

                # Check first page
                text = pdf.pages[0].extract_text() or ""

                # Check for bank keywords
                for bank, keywords in self.BANK_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword in text:
                            logger.info("bank_detected", bank=bank)
                            return bank

                logger.warning("bank_not_detected")
                return "unknown"

        except Exception as e:
            logger.error("bank_detection_failed", error=str(e))
            return "unknown"
