"""Tests for health check endpoint."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.unit
def test_health_check():
    """Test health check endpoint."""
    client = TestClient(app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data


@pytest.mark.unit
def test_root_endpoint():
    """Test root endpoint."""
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "PaisaBuddy" in data["name"]
