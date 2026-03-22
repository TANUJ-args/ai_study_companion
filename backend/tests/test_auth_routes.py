"""Tests for authentication and user routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.api.deps import FAKE_USERS_DB


@pytest.fixture
def client():
    """Create test client with fresh app instance."""
    app = create_app()
    return TestClient(app)


def test_login_with_valid_credentials(client):
    """Login endpoint returns valid JWT token."""
    response = client.post(
        "/login", data={"username": "user1", "password": "password123"}
    )

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_login_with_invalid_password(client):
    """Login with wrong password returns 401."""
    response = client.post("/login", data={"username": "user1", "password": "wrong"})

    assert response.status_code == 401
    assert "Incorrect" in response.json()["detail"]


def test_login_with_nonexistent_user(client):
    """Login with nonexistent username returns 401."""
    response = client.post(
        "/login", data={"username": "nonexistent", "password": "password"}
    )

    assert response.status_code == 401


def test_signup_creates_new_user(client):
    """Signup endpoint creates a new user."""
    response = client.post(
        "/signup",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert response.json()["username"] == "newuser"
    # Verify user was added to DB
    assert "newuser" in FAKE_USERS_DB


def test_signup_with_duplicate_username(client):
    """Signup with existing username returns 400."""
    response = client.post(
        "/signup",
        json={
            "username": "user1",
            "email": "different@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_signup_with_invalid_email(client):
    """Signup with invalid email returns 400."""
    response = client.post(
        "/signup",
        json={
            "username": "emailtest",
            "email": "invalidemail",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()


def test_signup_with_short_password(client):
    """Signup with short password returns 400."""
    response = client.post(
        "/signup",
        json={"username": "passtest", "email": "pass@example.com", "password": "short"},
    )

    assert response.status_code == 400
    assert "at least 6" in response.json()["detail"]


def test_protected_route_with_valid_token(client):
    """Protected route with valid token returns user data."""
    # First login to get token
    login_response = client.post(
        "/login", data={"username": "user1", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["username"] == "user1"
    assert "Hello" in response.json()["message"]


def test_protected_route_without_token(client):
    """Protected route without token returns 401."""
    response = client.get("/protected")

    assert response.status_code == 401


def test_protected_route_with_invalid_token(client):
    """Protected route with invalid token returns 401."""
    response = client.get(
        "/protected", headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401


def test_user_profile_endpoint(client):
    """User profile endpoint returns authenticated user info."""
    # Login
    login_response = client.post(
        "/login", data={"username": "user2", "password": "securepass456"}
    )
    token = login_response.json()["access_token"]

    # Get profile
    response = client.get("/user/profile", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    profile = response.json()
    assert profile["username"] == "user2"
    assert profile["email"] == "user2@example.com"
    assert profile["disabled"] is False


def test_user_profile_without_token(client):
    """User profile endpoint without token returns 401."""
    response = client.get("/user/profile")

    assert response.status_code == 401
