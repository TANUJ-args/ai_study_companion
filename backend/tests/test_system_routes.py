"""Tests for system and info routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    """Create test client with fresh app instance."""
    app = create_app()
    return TestClient(app)


def test_root_endpoint_returns_info(client):
    """Root endpoint returns API info and endpoints list."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert "test_credentials" in data


def test_root_endpoint_includes_all_routes(client):
    """Root endpoint documents all major routes."""
    response = client.get("/")

    data = response.json()
    endpoints = data["endpoints"]

    # Check major routes are documented
    assert any("signup" in str(v).lower() for v in endpoints.values())
    assert any("login" in str(v).lower() for v in endpoints.values())
    assert any("chat" in str(v).lower() for v in endpoints.values())
    assert any("generate-question" in str(v).lower() for v in endpoints.values())
    assert any("memory" in str(v).lower() for v in endpoints.values())


def test_root_endpoint_includes_test_credentials(client):
    """Root endpoint provides test credentials."""
    response = client.get("/")

    data = response.json()
    creds = data["test_credentials"]
    assert "username" in creds
    assert "password" in creds
