import pytest

from app.services.llm_service import _validate_quiz_question_payload, safe_parse_json


def test_safe_parse_json_parses_plain_json():
    raw = '{"questions": [{"question": "Q"}]}'
    parsed = safe_parse_json(raw)

    assert parsed is not None
    assert "questions" in parsed


def test_safe_parse_json_parses_fenced_json():
    raw = "```json\n{\"questions\": []}\n```"
    parsed = safe_parse_json(raw)

    assert parsed == {"questions": []}


def test_safe_parse_json_parses_embedded_json_block():
    raw = "text before {\"questions\": []} text after"
    parsed = safe_parse_json(raw)

    assert parsed == {"questions": []}


def test_validate_quiz_question_payload_accepts_valid_data():
    item = {
        "question": "  What is 2 + 2?  ",
        "options": [" 1 ", " 4 ", " 3 ", " 5 "],
        "correct_option_index": 1,
        "explanation": " 2 + 2 equals 4. ",
    }

    cleaned = _validate_quiz_question_payload(item)

    assert cleaned["question"] == "What is 2 + 2?"
    assert cleaned["options"] == ["1", "4", "3", "5"]
    assert cleaned["correct_option_index"] == 1
    assert cleaned["explanation"] == "2 + 2 equals 4."


def test_validate_quiz_question_payload_rejects_invalid_options():
    item = {
        "question": "What is 2 + 2?",
        "options": ["1", "4"],
        "correct_option_index": 1,
        "explanation": "2 + 2 equals 4.",
    }

    with pytest.raises(RuntimeError, match="exactly 4"):
        _validate_quiz_question_payload(item)
