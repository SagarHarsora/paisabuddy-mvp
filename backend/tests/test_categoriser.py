"""Tests for transaction categorizer."""
import pytest

from app.services.categoriser import TransactionCategorizer


@pytest.mark.unit
def test_categorize_food():
    """Test food category detection."""
    categorizer = TransactionCategorizer()

    categories = [
        "FOOD DELIVERY - SWIGGY",
        "RESTAURANT - PIZZA HUT",
        "CAFE - STARBUCKS",
    ]

    for desc in categories:
        category = categorizer.categorize(desc)
        assert category == "food", f"Failed for {desc}"


@pytest.mark.unit
def test_categorize_transport():
    """Test transport category detection."""
    categorizer = TransactionCategorizer()

    categories = [
        "FUEL PUMP - SHELL",
        "UBER - RIDE",
        "PETROL BUNK",
    ]

    for desc in categories:
        category = categorizer.categorize(desc)
        assert category == "transport", f"Failed for {desc}"


@pytest.mark.unit
def test_categorize_shopping():
    """Test shopping category detection."""
    categorizer = TransactionCategorizer()

    categories = [
        "AMAZON - ONLINE SHOPPING",
        "FLIPKART",
        "MYNTRA - FASHION",
    ]

    for desc in categories:
        category = categorizer.categorize(desc)
        assert category == "shopping", f"Failed for {desc}"


@pytest.mark.unit
def test_is_salary():
    """Test salary detection."""
    categorizer = TransactionCategorizer()

    assert categorizer.is_salary("SALARY CREDIT - COMPANY") is True
    assert categorizer.is_salary("PAYROLL DEPOSIT") is True
    assert categorizer.is_salary("FOOD - SWIGGY") is False


@pytest.mark.unit
def test_is_emi():
    """Test EMI detection."""
    categorizer = TransactionCategorizer()

    assert categorizer.is_emi("EMI - HOME LOAN") is True
    assert categorizer.is_emi("LOAN PAYMENT") is True
    assert categorizer.is_emi("FOOD - SWIGGY") is False
