"""Report narrative generation service."""
from decimal import Decimal
from typing import List, Dict, Any
import structlog

logger = structlog.get_logger(__name__)


class NarrativeGenerator:
    """Generate narrative insights for reports."""

    @staticmethod
    def generate(
        transactions: List[Dict[str, Any]],
        score: int,
        month: str,
    ) -> str:
        """Generate a narrative summary of the month's finances."""
        try:
            # Calculate metrics
            total_income = Decimal(0)
            total_expense = Decimal(0)
            category_totals: Dict[str, Decimal] = {}
            max_expense_category = None
            max_expense_amount = Decimal(0)

            for tx in transactions:
                amount = Decimal(str(tx.get("amount", 0)))
                is_salary = tx.get("is_salary", False)
                is_debit = tx.get("is_debit", False)
                category = tx.get("category", "other")

                if is_salary:
                    total_income += amount
                elif is_debit:
                    total_expense += amount
                    category_totals[category] = category_totals.get(category, Decimal(0)) + amount

                    if amount > max_expense_amount:
                        max_expense_amount = amount
                        max_expense_category = category

            # Generate narrative
            narrative_parts = []

            # Opening statement
            if score >= 80:
                narrative_parts.append(f"Excellent financial control this month! Your Paisa Score of {score} shows you're managing your money well.")
            elif score >= 60:
                narrative_parts.append(f"Good job managing your finances. Your Paisa Score of {score} is healthy, but there's room to optimize.")
            elif score >= 40:
                narrative_parts.append(f"Your Paisa Score of {score} suggests you should look at your spending patterns more carefully.")
            else:
                narrative_parts.append(f"Your Paisa Score of {score} indicates significant opportunities to improve your financial health.")

            # Savings rate
            if total_income > 0:
                savings = total_income - total_expense
                savings_rate = (savings / total_income) * 100
                narrative_parts.append(f"You saved {savings_rate:.1f}% of your income this month.")
            else:
                narrative_parts.append("No income detected this month.")

            # Top expense
            if max_expense_category:
                narrative_parts.append(
                    f"Your highest spending was on {max_expense_category} (₹{max_expense_amount:,})."
                )

            # Specific insights
            if category_totals.get("food", Decimal(0)) > total_expense * Decimal(0.2):
                narrative_parts.append("Food and dining is taking more than 20% of your expenses. Consider meal planning to reduce costs.")

            if category_totals.get("entertainment", Decimal(0)) > Decimal(2000):
                narrative_parts.append("Entertainment subscriptions are adding up. Review which services you actually use.")

            if category_totals.get("shopping", Decimal(0)) > total_expense * Decimal(0.15):
                narrative_parts.append("Shopping expenses are significant. Look for opportunities to reduce discretionary spending.")

            # Closing
            narrative_parts.append("Keep tracking your finances for better control next month.")

            narrative = " ".join(narrative_parts)
            logger.info("narrative_generated", score=score, length=len(narrative))
            return narrative

        except Exception as e:
            logger.error("narrative_generation_failed", error=str(e))
            return "Your financial data is being processed. Check back soon for insights."


def generate_narrative(
    transactions: List[Dict[str, Any]],
    score: int,
    month: str = "this month",
) -> str:
    """Generate narrative for a report."""
    generator = NarrativeGenerator()
    return generator.generate(transactions, score, month)
