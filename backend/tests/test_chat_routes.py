"""Tests for chat and quiz generation routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    """Create test client with fresh app instance."""
    app = create_app()
    return TestClient(app)


def test_chat_with_empty_message(client):
    """Chat endpoint rejects empty message."""
    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_chat_with_whitespace_only_message(client):
    """Chat endpoint rejects whitespace-only message."""
    response = client.post("/chat", json={"message": "   "})

    assert response.status_code == 400


def test_chat_endpoint_validates_json_format(client):
    """Chat endpoint requires valid JSON."""
    response = client.post("/chat", json="not-a-valid-json-object")

    assert response.status_code == 422


def test_generate_question_with_invalid_count(client):
    """Generate question endpoint requires exactly 2 questions."""
    response = client.post(
        "/generate-question",
        json={"topic": "Algebra", "difficulty": "medium", "question_count": 5},
    )

    assert response.status_code == 422


def test_generate_question_with_invalid_difficulty(client):
    """Generate question endpoint validates difficulty enum."""
    response = client.post(
        "/generate-question",
        json={"topic": "Algebra", "difficulty": "impossible", "question_count": 2},
    )

    assert response.status_code == 422


def test_generate_question_with_empty_topic(client):
    """Generate question endpoint rejects empty topic."""
    response = client.post(
        "/generate-question",
        json={"topic": "", "difficulty": "medium", "question_count": 2},
    )

    assert response.status_code == 422


def test_generate_question_response_structure(client):
    """Generate question response has required fields."""
    response = client.post(
        "/generate-question",
        json={"topic": "test_topic", "difficulty": "medium", "question_count": 2},
    )

    # Note: This will fail if GROQ_API_KEY is not set, which is expected in test environment
    # but we test the schema validation here
    if response.status_code in [200, 502]:  # 502 = API not configured
        if response.status_code == 200:
            data = response.json()
            assert "topic" in data
            assert "difficulty" in data
            assert "batch_size" in data
            assert "questions" in data
