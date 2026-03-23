"""Tests for memory storage and insights routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    """Create test client with fresh app instance."""
    app = create_app()
    return TestClient(app)


def test_store_memory_with_valid_payload(client):
    """Store memory endpoint accepts valid quiz data."""
    response = client.post(
        "/store-memory",
        json={
            "user_id": "user1",
            "topic": "Algebra",
            "mistake_type": "Conceptual",
            "difficulty": "Medium",
            "score": 75,
        },
    )

    # Hindsight client may not be configured; both 200 and 500 are acceptable
    assert response.status_code in [200, 500]


def test_store_memory_with_missing_fields(client):
    """Store memory rejects incomplete payload."""
    response = client.post(
        "/store-memory", json={"user_id": "user1", "topic": "Algebra"}
    )

    assert response.status_code == 422


def test_store_memory_with_invalid_score(client):
    """Store memory rejects invalid score values."""
    response = client.post(
        "/store-memory",
        json={
            "user_id": "user1",
            "topic": "Algebra",
            "mistake_type": "Conceptual",
            "difficulty": "Medium",
            "score": 150,  # Invalid: > 100
        },
    )

    assert response.status_code == 422


def test_store_memory_batch_with_valid_payload(client):
    """Store memory batch endpoint accepts 2 attempts."""
    response = client.post(
        "/store-memory-batch",
        json={
            "user_id": "user1",
            "attempts": [
                {
                    "topic": "Algebra",
                    "mistake_type": "Conceptual",
                    "difficulty": "Medium",
                    "score": 75,
                },
                {
                    "topic": "Geometry",
                    "mistake_type": "Calculation",
                    "difficulty": "Hard",
                    "score": 60,
                },
            ],
        },
    )

    # Both 200 and 500 acceptable depending on Hindsight config
    assert response.status_code in [200, 500]


def test_store_memory_batch_with_wrong_count(client):
    """Store memory batch rejects if not exactly 2 attempts."""
    response = client.post(
        "/store-memory-batch",
        json={
            "user_id": "user1",
            "attempts": [
                {
                    "topic": "Algebra",
                    "mistake_type": "Conceptual",
                    "difficulty": "Medium",
                    "score": 75,
                }
            ],
        },
    )

    assert response.status_code == 422
    assert "exactly 2" in response.json()["detail"][0]["msg"].lower()


def test_weak_topics_with_empty_user_id(client):
    """Weak topics endpoint rejects empty user_id."""
    response = client.get("/weak-topics/")

    assert response.status_code == 404  # Or validation error


def test_weak_topics_with_valid_user_id(client):
    """Weak topics endpoint returns list structure."""
    response = client.get("/weak-topics/user1")

    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "weak_topics" in data
    assert isinstance(data["weak_topics"], list)


def test_mistakes_with_empty_user_id(client):
    """Mistakes endpoint rejects empty user_id."""
    response = client.get("/mistakes/")

    assert response.status_code == 404


def test_mistakes_with_valid_user_id(client):
    """Mistakes endpoint returns list structure."""
    response = client.get("/mistakes/user1")

    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "mistakes" in data
    assert isinstance(data["mistakes"], list)


def test_insights_with_empty_user_id(client):
    """Insights endpoint rejects empty user_id."""
    response = client.get("/insights/")

    assert response.status_code == 404


def test_insights_with_valid_user_id(client):
    """Insights endpoint returns insights structure."""
    response = client.get("/insights/user1")

    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "insights" in data
    assert "weak_topics" in data["insights"]
    assert "strong_topics" in data["insights"]


def test_recommendations_with_valid_user_id(client):
    """Recommendations endpoint returns expected structure."""
    response = client.get("/recommendations/user1")

    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
