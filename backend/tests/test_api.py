"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.auth import AuthService


@pytest.mark.unit
def test_request_otp_valid_phone():
    """Test requesting OTP with valid phone."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/request-otp",
        json={
            "phone": "+919876543210",
            "language": "en",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data["data"]


@pytest.mark.unit
def test_request_otp_invalid_phone():
    """Test requesting OTP with invalid phone."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/request-otp",
        json={
            "phone": "123",
            "language": "en",
        },
    )

    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "A007"


@pytest.mark.unit
def test_verify_otp_success():
    """Test verifying OTP."""
    client = TestClient(app)

    # Request OTP first
    req_response = client.post(
        "/api/v1/auth/request-otp",
        json={
            "phone": "+919876543210test",
            "language": "en",
        },
    )

    assert req_response.status_code == 200
    otp = req_response.json()["data"].get("otp_debug")

    if otp:
        # Verify OTP
        verify_response = client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "+919876543210test",
                "otp": otp,
            },
        )

        assert verify_response.status_code == 200
        data = verify_response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.unit
def test_health_check():
    """Test health check endpoint."""
    client = TestClient(app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
