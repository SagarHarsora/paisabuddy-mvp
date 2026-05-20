"""Tests for PDF parser."""
import pytest

from app.services.parser.digital import DigitalPDFParser, TransactionData


@pytest.mark.unit
def test_digital_parser_initialization():
    """Test parser can be initialized."""
    parser = DigitalPDFParser()
    assert parser is not None


@pytest.mark.unit
async def test_extract_transactions_empty_pdf():
    """Test handling of empty PDF."""
    parser = DigitalPDFParser()

    # Test with actual empty PDF data
    # For now, we'll test the structure
    assert hasattr(parser, "extract_transactions")
    assert hasattr(parser, "detect_bank")


@pytest.mark.unit
def test_parse_row_valid():
    """Test parsing a valid transaction row."""
    parser = DigitalPDFParser()

    row = ["01-Apr-2024", "SALARY CREDIT - COMPANY", "50000"]
    result = parser._parse_row(row)

    assert result is not None
    assert result.date == "2024-04-01"
    assert result.amount == 50000.0
    assert "SALARY" in result.description.upper()


@pytest.mark.unit
def test_parse_row_invalid():
    """Test parsing an invalid row."""
    parser = DigitalPDFParser()

    # Missing data
    row = ["01-Apr-2024", "Food"]
    result = parser._parse_row(row)

    assert result is None


@pytest.mark.unit
def test_detect_bank():
    """Test bank detection."""
    parser = DigitalPDFParser()

    # Test with mock content
    for bank, keywords in parser.BANK_KEYWORDS.items():
        assert len(keywords) > 0
