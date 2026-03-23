from datetime import datetime

from app.services.memory_service import (
    _build_structured_content,
    _parse_memory_from_text,
    QuizMemory,
    calculate_insights,
    calculate_topic_mastery,
    filter_strong_topics,
    filter_weak_topics,
    recommend_topics,
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


def test_calculate_topic_mastery_uses_recency_weighting():
    memories = [
        {"topic": "Algebra", "score": 30, "timestamp": "2026-01-01T10:00:00"},
        {"topic": "Algebra", "score": 50, "timestamp": "2026-01-02T10:00:00"},
        {"topic": "Algebra", "score": 80, "timestamp": "2026-01-03T10:00:00"},
    ]

    mastery = calculate_topic_mastery(memories, alpha=0.5)

    assert "Algebra" in mastery
    assert mastery["Algebra"]["attempt_count"] == 3
    assert mastery["Algebra"]["latest_score"] == 80
    assert 0.5 < mastery["Algebra"]["mastery"] <= 1.0


def test_recommend_topics_prioritizes_weaker_topic():
    memories = [
        {"topic": "Algebra", "score": 35, "timestamp": "2026-01-01T10:00:00"},
        {"topic": "Algebra", "score": 40, "timestamp": "2026-01-02T10:00:00"},
        {"topic": "Geometry", "score": 80, "timestamp": "2026-01-01T10:00:00"},
        {"topic": "Geometry", "score": 85, "timestamp": "2026-01-02T10:00:00"},
    ]

    recommendations = recommend_topics(memories, limit=2)

    assert len(recommendations) == 2
    assert recommendations[0]["topic"] == "Algebra"
    assert recommendations[0]["priority_score"] >= recommendations[1]["priority_score"]


def test_build_structured_content_contains_core_keys():
    memory = QuizMemory(
        user_id="u1",
        topic="Algebra",
        mistake_type="Conceptual",
        difficulty="Medium",
        score=42,
        source="quiz",
        session_id="s1",
    )

    content = _build_structured_content(memory)

    assert "QUIZ_MEMORY" in content
    assert "user_id=u1" in content
    assert "topic=Algebra" in content
    assert "mistake_type=Conceptual" in content
    assert "difficulty=Medium" in content
    assert "score=42" in content


def test_parse_memory_from_text_reads_structured_record():
    text = (
        "QUIZ_MEMORY; user_id=u1; topic=Algebra; mistake_type=Conceptual; "
        "difficulty=Medium; score=42; timestamp=2026-01-01T10:00:00; "
        "source=quiz;"
    )

    parsed = _parse_memory_from_text(text, "u1")

    assert parsed is not None
    assert parsed["user_id"] == "u1"
    assert parsed["topic"] == "Algebra"
    assert parsed["mistake_type"] == "Conceptual"
    assert parsed["difficulty"] == "Medium"
    assert parsed["score"] == 42
    assert parsed["source"] == "quiz"


def test_parse_memory_from_text_rejects_legacy_without_user_marker():
    text = (
        "User completed a quiz on Algebra with a score of 35, "
        "making a conceptual mistake on a medium difficulty question."
    )

    parsed = _parse_memory_from_text(text, "u1")

    assert parsed is None
