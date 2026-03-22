"""Tests for Pydantic schema validation."""

import pytest
from pydantic import ValidationError

from app.schemas.auth import Token, TokenData, UserCreate, UserResponse
from app.schemas.chat import ChatRequest
from app.schemas.memory import BatchMemoryItem, StoreMemoryBatchRequest
from app.schemas.quiz import (
    GenerateQuestionRequest,
    GenerateQuestionResponse,
    QuizQuestionItem,
)


def test_token_schema_requires_fields():
    """Token schema requires access_token and token_type."""
    with pytest.raises(ValidationError):
        Token(access_token="xyz")  # Missing token_type

    token = Token(access_token="xyz", token_type="bearer")
    assert token.access_token == "xyz"
    assert token.token_type == "bearer"


def test_user_create_validation():
    """UserCreate schema validates username, email, password."""
    # All fields required
    with pytest.raises(ValidationError):
        UserCreate(username="user", email="user@example.com")

    user = UserCreate(
        username="newuser", email="newuser@example.com", password="mypassword"
    )
    assert user.username == "newuser"


def test_chat_request_schema():
    """ChatRequest accepts message (validation happens in route)."""
    # Schema accepts empty string; route handler validates non-empty
    chat_empty = ChatRequest(message="")
    assert chat_empty.message == ""

    chat = ChatRequest(message="Hello AI")
    assert chat.message == "Hello AI"


def test_batch_memory_item_validates_mistake_type():
    """BatchMemoryItem validates mistake_type enum."""
    with pytest.raises(ValidationError):
        BatchMemoryItem(
            topic="Algebra", mistake_type="InvalidType", difficulty="Medium", score=70
        )

    item = BatchMemoryItem(
        topic="Algebra", mistake_type="Conceptual", difficulty="Medium", score=70
    )
    assert item.mistake_type == "Conceptual"


def test_batch_memory_item_validates_score_range():
    """BatchMemoryItem validates score is 0-100."""
    with pytest.raises(ValidationError):
        BatchMemoryItem(
            topic="Algebra", mistake_type="Conceptual", difficulty="Medium", score=150
        )

    with pytest.raises(ValidationError):
        BatchMemoryItem(
            topic="Algebra", mistake_type="Conceptual", difficulty="Medium", score=-10
        )


def test_store_memory_batch_request_requires_exactly_two_attempts():
    """StoreMemoryBatchRequest validates exactly 2 attempts."""
    with pytest.raises(ValidationError):
        StoreMemoryBatchRequest(
            user_id="user1",
            attempts=[
                BatchMemoryItem(
                    topic="Algebra",
                    mistake_type="Conceptual",
                    difficulty="Medium",
                    score=70,
                )
            ],
        )

    batch = StoreMemoryBatchRequest(
        user_id="user1",
        attempts=[
            BatchMemoryItem(
                topic="Algebra",
                mistake_type="Conceptual",
                difficulty="Medium",
                score=70,
            ),
            BatchMemoryItem(
                topic="Geometry",
                mistake_type="Calculation",
                difficulty="Hard",
                score=60,
            ),
        ],
    )
    assert len(batch.attempts) == 2


def test_generate_question_request_validates_difficulty():
    """GenerateQuestionRequest validates difficulty enum."""
    with pytest.raises(ValidationError):
        GenerateQuestionRequest(
            topic="Algebra", difficulty="impossible", question_count=2
        )

    req = GenerateQuestionRequest(
        topic="Algebra", difficulty="medium", question_count=2
    )
    assert req.difficulty == "medium"


def test_generate_question_request_enforces_count_equals_two():
    """GenerateQuestionRequest enforces question_count == 2."""
    with pytest.raises(ValidationError):
        GenerateQuestionRequest(topic="Algebra", difficulty="medium", question_count=5)

    req = GenerateQuestionRequest(
        topic="Algebra", difficulty="medium", question_count=2
    )
    assert req.question_count == 2


def test_quiz_question_item_validation():
    """QuizQuestionItem validates structure and correct_option_index."""
    # Valid item
    item = QuizQuestionItem(
        question="What is 2+2?",
        options=["1", "4", "3", "5"],
        correct_option_index=1,
        explanation="2+2 equals 4",
    )
    assert item.correct_option_index == 1

    # Invalid: wrong option count
    with pytest.raises(ValidationError):
        QuizQuestionItem(
            question="What is 2+2?",
            options=["1", "4"],
            correct_option_index=1,
            explanation="2+2 equals 4",
        )

    # Invalid: out of range index
    with pytest.raises(ValidationError):
        QuizQuestionItem(
            question="What is 2+2?",
            options=["1", "4", "3", "5"],
            correct_option_index=5,
            explanation="2+2 equals 4",
        )
