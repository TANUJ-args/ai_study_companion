from datetime import datetime

from app.services.memory_service import (
    QuizMemory,
    calculate_insights,
    filter_strong_topics,
    filter_weak_topics,
)


def test_quiz_memory_to_dict_serializes_fields():
    ts = datetime(2026, 1, 1, 10, 30, 0)
    memory = QuizMemory(
        user_id="u1",
        topic="Algebra",
        mistake_type="Conceptual",
        difficulty="Medium",
        score=45,
        timestamp=ts,
    )

    payload = memory.to_dict()

    assert payload["user_id"] == "u1"
    assert payload["topic"] == "Algebra"
    assert payload["mistake_type"] == "Conceptual"
    assert payload["difficulty"] == "Medium"
    assert payload["score"] == 45
    assert payload["timestamp"] == ts.isoformat()


def test_filter_weak_topics_returns_unique_topics_below_50():
    memories = [
        {"topic": "Algebra", "score": 45},
        {"topic": "Algebra", "score": 20},
        {"topic": "Geometry", "score": 49},
        {"topic": "Physics", "score": 70},
    ]

    weak = filter_weak_topics(memories)

    assert set(weak) == {"Algebra", "Geometry"}


def test_filter_strong_topics_returns_unique_topics_above_70():
    memories = [
        {"topic": "Algebra", "score": 71},
        {"topic": "Algebra", "score": 95},
        {"topic": "Geometry", "score": 70},
        {"topic": "Physics", "score": 85},
    ]

    strong = filter_strong_topics(memories)

    assert set(strong) == {"Algebra", "Physics"}


def test_calculate_insights_returns_expected_summary():
    memories = [
        {"topic": "Algebra", "score": 45, "mistake_type": "Conceptual"},
        {"topic": "Physics", "score": 80, "mistake_type": "Calculation"},
        {"topic": "Algebra", "score": 30, "mistake_type": "Conceptual"},
    ]

    insights = calculate_insights(memories)

    assert set(insights["weak_topics"]) == {"Algebra"}
    assert set(insights["strong_topics"]) == {"Physics"}
    assert insights["most_common_mistake_type"] == "Conceptual"


def test_calculate_insights_empty_input_defaults():
    insights = calculate_insights([])

    assert insights == {
        "weak_topics": [],
        "strong_topics": [],
        "most_common_mistake_type": None,
    }
