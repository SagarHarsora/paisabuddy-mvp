"""PDF upload and statement processing endpoints."""
from fastapi import APIRouter, UploadFile, File, Depends, Header
from sqlalchemy.ext.asyncic import AsyncSession
from datetime import datetime
import structlog

from app.database import get_db
from app.models import User, Statement, Transaction
from app.api.v1.auth import get_current_user
from app.api.schemas import UploadResponse
from app.services.parser.digital import DigitalPDFParser
from app.services.categoriser import TransactionCategorizer
from app.services.score import calculate_paisa_score
from app.services.narrative import generate_narrative
from app.utils.errors import APIError, ErrorCode
from app.utils.logging import mask_phone
from app.config import settings

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_statement(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    """Upload bank statement PDF and process it."""
    logger.info("upload_start", user_id=str(current_user.id), filename=file.filename)

    try:
        # Validate file
        if not file.filename.lower().endswith(".pdf"):
            logger.warning("invalid_file_type", filename=file.filename)
            raise APIError(
                code=ErrorCode.FILE_NOT_PDF,
                message="That file isn't a PDF. Bank statements are usually downloaded as PDFs from your bank's app or net banking.",
                user_facing=True,
            )

        # Check file size (max 10MB)
        file_size = await file.read()
        file_size_mb = len(file_size) / (1024 * 1024)

        if file_size_mb > 10:
            logger.warning("file_too_large", size_mb=file_size_mb)
            raise APIError(
                code=ErrorCode.FILE_TOO_LARGE,
                message="File is too large. Maximum size is 10MB.",
                user_facing=True,
            )

        # Reset file pointer
        await file.seek(0)

        # Create statement record
        statement = Statement(
            user_id=current_user.id,
            bank="unknown",
            statement_type="digital",
            months_covered=1,
            parse_status="processing",
        )
        db.add(statement)
        await db.flush()

        logger.info("statement_created", statement_id=str(statement.id))

        # Parse PDF
        parser = DigitalPDFParser()
        pdf_content = file_size

        # Detect bank
        bank = parser.detect_bank(pdf_content)
        statement.bank = bank
        logger.info("bank_detected", bank=bank)

        # Extract transactions
        extracted_txs = await parser.extract_transactions(pdf_content)
        logger.info("transactions_extracted", count=len(extracted_txs))

        if not extracted_txs:
            statement.parse_status = "failed"
            statement.parse_error = "No transactions found in PDF"
            await db.flush()
            raise APIError(
                code=ErrorCode.NO_TRANSACTIONS_FOUND,
                message="No transactions found in this PDF. Check that it's a valid bank statement.",
                user_facing=True,
            )

        # Convert to dicts for categorization
        txs_dict = [
            {
                "date": tx.date,
                "amount": float(tx.amount),
                "description": tx.description,
                "is_debit": tx.is_debit,
                "category": tx.category,
                "confidence": float(tx.confidence),
            }
            for tx in extracted_txs
        ]

        # Categorize transactions
        categorizer = TransactionCategorizer()
        for tx in txs_dict:
            tx["category"] = categorizer.categorize(tx["description"])
            tx["is_salary"] = categorizer.is_salary(tx["description"])
            tx["is_emi"] = categorizer.is_emi(tx["description"])

        logger.info("transactions_categorized", count=len(txs_dict))

        # Save transactions to database
        for tx in txs_dict:
            transaction = Transaction(
                statement_id=statement.id,
                user_id=current_user.id,
                date=tx["date"],
                amount=tx["amount"],
                description=tx["description"],
                category=tx["category"],
                is_debit=tx["is_debit"],
                is_salary=tx.get("is_salary", False),
                is_emi=tx.get("is_emi", False),
                confidence=tx.get("confidence", 1.0),
            )
            db.add(transaction)

        statement.transaction_count = len(txs_dict)
        statement.parse_status = "done"
        statement.accuracy_score = 0.95  # TODO: Calculate actual accuracy

        await db.commit()

        logger.info(
            "upload_complete",
            statement_id=str(statement.id),
            transactions=len(txs_dict),
            bank=bank,
        )

        return UploadResponse(
            statement_id=str(statement.id),
            bank=bank,
            status="done",
            message=f"Successfully processed {len(txs_dict)} transactions from your {bank.upper()} statement.",
        )

    except APIError:
        if 'statement' in locals():
            statement.parse_status = "failed"
            await db.commit()
        raise
    except Exception as e:
        logger.exception("upload_failed", error=type(e).__name__)
        if 'statement' in locals():
            statement.parse_status = "failed"
            statement.parse_error = str(e)[:500]
            await db.commit()
        raise APIError(
            code=ErrorCode.PARSER_CRASHED,
            message="Something went wrong processing your PDF. Our team has been notified.",
            user_facing=True,
            status_code=500,
        )
