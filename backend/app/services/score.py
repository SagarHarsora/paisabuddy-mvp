"""Paisa Score calculation service."""
from decimal import Decimal
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger(__name__)


class PaisaScoreCalculator:
    """Calculate Paisa Score based on transactions."""

    @staticmethod
    def calculate(transactions: List[Dict[str, Any]]) -> int:
        """Calculate Paisa Score (0-100)."""
        if not transactions:
            return 0

        try:
            # Calculate metrics
            total_income = Decimal(0)
            total_debit = Decimal(0)
            emi_amount = Decimal(0)
            salary_amount = Decimal(0)
            category_breakdown: Dict[str, Decimal] = {}

            for tx in transactions:
                amount = Decimal(str(tx.get("amount", 0)))
                is_debit = tx.get("is_debit", False)
                is_salary = tx.get("is_salary", False)
                is_emi = tx.get("is_emi", False)
                category = tx.get("category", "other")

                if is_salary:
                    salary_amount += amount
                    total_income += amount
                elif is_debit:
                    total_debit += amount
                    if is_emi:
                        emi_amount += amount
                    # Track category spend
                    category_breakdown[category] = category_breakdown.get(category, Decimal(0)) + amount

            # Calculate savings rate
            if total_income > 0:
                savings = total_income - total_debit
                savings_rate = (savings / total_income) * 100
            else:
                savings_rate = 0

            # Calculate score components
            score = 0

            # 1. Savings rate (0-30 points)
            # 0% = 0 points, 50%+ = 30 points
            savings_points = min(30, max(0, int((savings_rate / 50) * 30)))
            score += savings_points

            # 2. Spend consistency (0-20 points)
            # Lower variance = higher score
            if len(category_breakdown) > 0:
                avg_spend = sum(category_breakdown.values()) / len(category_breakdown)
                if avg_spend > 0:
                    variance = sum(
                        ((v - avg_spend) ** 2 for v in category_breakdown.values())
                    ) / len(category_breakdown)
                    consistency = 20 / (1 + float(variance / (avg_spend ** 2)))
                    score += min(20, int(consistency))

            # 3. EMI management (0-20 points)
            # Lower EMI ratio = higher score
            if total_debit > 0:
                emi_ratio = float(emi_amount / total_debit)
                emi_points = max(0, 20 - int(emi_ratio * 20))
                score += emi_points

            # 4. Category control (0-20 points)
            # More diverse spending = higher score (balanced)
            num_categories = len(category_breakdown)
            category_points = min(20, num_categories * 2)
            score += category_points

            # 5. Salary presence (0-10 points)
            # Regular salary = 10 points
            if salary_amount > 0:
                score += 10

            # Ensure score is between 0-100
            score = min(100, max(0, score))

            logger.info(
                "score_calculated",
                score=score,
                savings_rate=float(savings_rate),
                categories=len(category_breakdown),
            )

            return score

        except Exception as e:
            logger.error("score_calculation_failed", error=str(e))
            return 50  # Default neutral score on error


def calculate_paisa_score(transactions: List[Dict[str, Any]]) -> int:
    """Calculate Paisa Score for transactions."""
    calculator = PaisaScoreCalculator()
    return calculator.calculate(transactions)
