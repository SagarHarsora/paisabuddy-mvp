"""Tests for Paisa Score calculator."""
import pytest

from app.services.score import PaisaScoreCalculator


@pytest.mark.unit
def test_calculate_empty_transactions():
    """Test score calculation with no transactions."""
    calculator = PaisaScoreCalculator()
    score = calculator.calculate([])

    assert score == 0


@pytest.mark.unit
def test_calculate_good_savings():
    """Test score with good savings rate."""
    calculator = PaisaScoreCalculator()

    transactions = [
        {
            "amount": 50000,
            "is_salary": True,
            "is_debit": False,
            "is_emi": False,
            "category": "salary",
        },
        {
            "amount": 10000,
            "is_salary": False,
            "is_debit": True,
            "is_emi": False,
            "category": "food",
        },
    ]

    score = calculator.calculate(transactions)

    # Should be high (80% savings rate)
    assert score > 50


@pytest.mark.unit
def test_calculate_poor_savings():
    """Test score with poor savings rate."""
    calculator = PaisaScoreCalculator()

    transactions = [
        {
            "amount": 50000,
            "is_salary": True,
            "is_debit": False,
            "is_emi": False,
            "category": "salary",
        },
        {
            "amount": 45000,
            "is_salary": False,
            "is_debit": True,
            "is_emi": False,
            "category": "food",
        },
    ]

    score = calculator.calculate(transactions)

    # Should be low (10% savings rate)
    assert score < 50
