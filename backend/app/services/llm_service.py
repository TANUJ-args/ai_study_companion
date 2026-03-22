"""Groq-backed LLM service helpers."""

import json
import re
from typing import Any, Dict, Optional

from groq import Groq

from app.core.config import GROQ_API_KEY, GROQ_MODEL_NAME

SYSTEM_PROMPT = (
    "You are an AI Study Companion that generates quiz questions and explains "
    "answers simply."
)


def _get_client() -> Groq:
    """Create a Groq client and fail clearly when config is missing."""

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured")
    return Groq(api_key=GROQ_API_KEY)


def safe_parse_json(raw_text: str) -> Optional[Dict[str, Any]]:
    """Safely parse a JSON object from model output text."""

    if not raw_text:
        return None

    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    candidate = cleaned[start : end + 1]
    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None


def ask_llm(prompt: str) -> str:
    """Send a plain chat prompt to the model and return text output."""

    client = _get_client()
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        model=GROQ_MODEL_NAME,
        temperature=0.3,
    )
    return (response.choices[0].message.content or "").strip()


def _validate_quiz_question_payload(question_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate one generated MCQ object and return normalized values."""

    question = question_data.get("question")
    options = question_data.get("options")
    correct_idx = question_data.get("correct_option_index")
    explanation = question_data.get("explanation")

    if not isinstance(question, str) or not question.strip():
        raise RuntimeError("LLM response missing valid 'question'")
    if not isinstance(explanation, str) or not explanation.strip():
        raise RuntimeError("LLM response missing valid 'explanation'")
    if (
        not isinstance(options, list)
        or len(options) != 4
        or not all(isinstance(opt, str) and opt.strip() for opt in options)
    ):
        raise RuntimeError("LLM response must contain exactly 4 non-empty options")
    if not isinstance(correct_idx, int) or correct_idx < 0 or correct_idx > 3:
        raise RuntimeError("LLM response has invalid 'correct_option_index'")

    return {
        "question": question.strip(),
        "options": [opt.strip() for opt in options],
        "correct_option_index": correct_idx,
        "explanation": explanation.strip(),
    }


def generate_quiz_questions(
    topic: str, difficulty: str = "medium", count: int = 2
) -> Dict[str, Any]:
    """Generate a strict JSON batch of MCQs for a topic."""

    if count <= 0:
        raise RuntimeError("count must be greater than 0")

    client = _get_client()
    prompt = (
        f"Generate exactly {count} multiple-choice questions as strict JSON only.\n"
        "Do not include markdown, prose, or code fences.\n"
        "Schema:\n"
        '{"questions":[{"question":"string","options":["a","b","c","d"],"correct_option_index":0,"explanation":"string"}]}\n'
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        "Rules:\n"
        f"- return exactly {count} questions\n"
        "- options must contain exactly 4 concise options\n"
        "- correct_option_index must be an integer 0..3\n"
        "- explanation must be 1-2 simple sentences for beginners\n"
        "- exactly one correct answer\n"
        "- return JSON object only"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model=GROQ_MODEL_NAME,
            temperature=0.2,
            max_tokens=950,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API error while generating questions: {exc}") from exc

    raw = (response.choices[0].message.content or "").strip()
    parsed = safe_parse_json(raw)
    if not parsed:
        raise RuntimeError("Failed to parse JSON from LLM response")

    questions = parsed.get("questions")
    if not isinstance(questions, list) or len(questions) != count:
        raise RuntimeError(f"LLM response must contain exactly {count} questions")

    cleaned_questions = []
    for item in questions:
        if not isinstance(item, dict):
            raise RuntimeError("Each question must be a JSON object")
        cleaned_questions.append(_validate_quiz_question_payload(item))

    return {"questions": cleaned_questions}


def generate_quiz_question(topic: str, difficulty: str = "medium") -> Dict[str, Any]:
    """Backward-compatible helper returning one generated question."""

    result = generate_quiz_questions(topic=topic, difficulty=difficulty, count=1)
    return result["questions"][0]
