"""Reports endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import date
import structlog

from app.database import get_db
from app.models import User, Statement, Transaction, Report
from app.api.v1.auth import get_current_user
from app.api.schemas import ReportResponse, ReportsListResponse, ReportListItem, CategoryBreakdown, TransactionResponse
from app.services.score import calculate_paisa_score
from app.services.narrative import generate_narrative
from app.utils.errors import APIError, ErrorCode
from decimal import Decimal

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["reports"])


@router.get("/reports")
async def list_reports(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all reports for current user."""
    logger.info("list_reports_request", user_id=str(current_user.id))

    try:
        # Get all statements for user with transactions
        result = await db.execute(
            select(Statement)
            .where(Statement.user_id == current_user.id)
            .where(Statement.parse_status == "done")
            .order_by(desc(Statement.uploaded_at))
        )
        statements = result.scalars().all()

        reports = []
        for statement in statements:
            # Get transactions for this statement
            tx_result = await db.execute(
                select(Transaction).where(Transaction.statement_id == statement.id)
            )
            transactions = tx_result.scalars().all()

            if transactions:
                # Calculate score and create report item
                txs_dict = [
                    {
                        "amount": float(tx.amount),
                        "is_debit": tx.is_debit,
                        "is_salary": tx.is_salary,
                        "is_emi": tx.is_emi,
                        "category": tx.category,
                        "description": tx.description,
                    }
                    for tx in transactions
                ]

                score = calculate_paisa_score(txs_dict)
                month_str = statement.uploaded_at.strftime("%Y-%m")

                reports.append(
                    ReportListItem(
                        statement_id=str(statement.id),
                        bank=statement.bank,
                        month=month_str,
                        paisa_score=score,
                        generated_at=statement.uploaded_at.isoformat(),
                    )
                )

        logger.info("list_reports_success", count=len(reports), user_id=str(current_user.id))

        return ReportsListResponse(reports=reports, total=len(reports))

    except Exception as e:
        logger.exception("list_reports_failed", error=type(e).__name__)
        raise APIError(
            code=ErrorCode.E500,
            message="Failed to fetch reports.",
            user_facing=True,
            status_code=500,
        )


@router.get("/reports/{statement_id}", response_model=ReportResponse)
async def get_report(
    statement_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed report for a statement."""
    logger.info("get_report_request", statement_id=statement_id, user_id=str(current_user.id))

    try:
        # Get statement
        result = await db.execute(
            select(Statement)
            .where(Statement.id == statement_id)
            .where(Statement.user_id == current_user.id)
            .where(Statement.parse_status == "done")
        )
        statement = result.scalars().first()

        if not statement:
            raise APIError(
                code=ErrorCode.D001,
                message="Report not found.",
                user_facing=True,
                status_code=404,
            )

        # Get transactions
        tx_result = await db.execute(
            select(Transaction).where(Transaction.statement_id == statement.id)
        )
        transactions = tx_result.scalars().all()

        if not transactions:
            raise APIError(
                code=ErrorCode.D001,
                message="No transactions found for this report.",
                user_facing=True,
            )

        # Convert to dicts for scoring
        txs_dict = [
            {
                "amount": float(tx.amount),
                "is_debit": tx.is_debit,
                "is_salary": tx.is_salary,
                "is_emi": tx.is_emi,
                "category": tx.category,
                "description": tx.description,
            }
            for tx in transactions
        ]

        # Calculate metrics
        total_income = Decimal(0)
        total_expense = Decimal(0)
        category_totals = {}

        for tx in transactions:
            amount = Decimal(str(tx.amount))
            if tx.is_salary:
                total_income += amount
            elif tx.is_debit:
                total_expense += amount
                category_totals[tx.category] = category_totals.get(tx.category, Decimal(0)) + amount

        # Calculate score
        score = calculate_paisa_score(txs_dict)

        # Calculate savings rate
        if total_income > 0:
            savings_rate = float(((total_income - total_expense) / total_income) * 100)
        else:
            savings_rate = 0

        # Generate narrative
        narrative = generate_narrative(txs_dict, score, statement.uploaded_at.strftime("%B %Y"))

        # Build category breakdown
        categories = []
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            if total_expense > 0:
                percentage = float((amount / total_expense) * 100)
            else:
                percentage = 0

            tx_count = sum(1 for t in transactions if t.category == category and t.is_debit)
            categories.append(
                CategoryBreakdown(
                    category=category,
                    amount=float(amount),
                    percentage=percentage,
                    transaction_count=tx_count,
                )
            )

        # Build transaction list (limit to last 20 for display)
        txs_display = [
            TransactionResponse(
                date=tx.date.isoformat(),
                description=tx.description,
                amount=float(tx.amount),
                category=tx.category,
                is_debit=tx.is_debit,
            )
            for tx in sorted(transactions, key=lambda x: x.date, reverse=True)[:20]
        ]

        logger.info(
            "get_report_success",
            statement_id=statement_id,
            score=score,
            user_id=str(current_user.id),
        )

        return ReportResponse(
            statement_id=str(statement.id),
            bank=statement.bank,
            month=statement.uploaded_at.strftime("%Y-%m"),
            paisa_score=score,
            total_income=float(total_income),
            total_expense=float(total_expense),
            savings_rate=savings_rate,
            narrative=narrative,
            categories=categories,
            transactions=txs_display,
            generated_at=statement.uploaded_at.isoformat(),
        )

    except APIError:
        raise
    except Exception as e:
        logger.exception("get_report_failed", error=type(e).__name__)
        raise APIError(
            code=ErrorCode.E500,
            message="Failed to generate report.",
            user_facing=True,
            status_code=500,
        )
