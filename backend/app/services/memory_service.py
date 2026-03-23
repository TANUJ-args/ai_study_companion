"""Hindsight memory storage and analytics utilities."""

from collections import Counter
import asyncio
from datetime import datetime
import inspect
import logging
import re
from typing import Dict, List, Optional

from hindsight_client import Hindsight

from app.core.config import (
    HINDSIGHT_API_KEY,
    HINDSIGHT_BASE_URL,
    HINDSIGHT_COLLECTION_NAME,
)


class QuizMemory:
    """Represents one quiz attempt to be stored in memory."""

    def __init__(
        self,
        user_id: str,
        topic: str,
        mistake_type: str,
        difficulty: str,
        score: int,
        question_id: Optional[str] = None,
        subtopic: Optional[str] = None,
        confidence: Optional[int] = None,
        time_spent_seconds: Optional[int] = None,
        source: Optional[str] = None,
        session_id: Optional[str] = None,
        user_answer: Optional[str] = None,
        correct_answer: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.topic = topic
        self.mistake_type = mistake_type
        self.difficulty = difficulty
        self.score = score
        self.question_id = question_id
        self.subtopic = subtopic
        self.confidence = confidence
        self.time_spent_seconds = time_spent_seconds
        self.source = source
        self.session_id = session_id
        self.user_answer = user_answer
        self.correct_answer = correct_answer
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict:
        """Convert memory to a serializable record."""

        payload = {
            "user_id": self.user_id,
            "topic": self.topic,
            "mistake_type": self.mistake_type,
            "difficulty": self.difficulty,
            "score": self.score,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.question_id:
            payload["question_id"] = self.question_id
        if self.subtopic:
            payload["subtopic"] = self.subtopic
        if self.confidence is not None:
            payload["confidence"] = self.confidence
        if self.time_spent_seconds is not None:
            payload["time_spent_seconds"] = self.time_spent_seconds
        if self.source:
            payload["source"] = self.source
        if self.session_id:
            payload["session_id"] = self.session_id
        if self.user_answer:
            payload["user_answer"] = self.user_answer
        if self.correct_answer:
            payload["correct_answer"] = self.correct_answer
        return payload


def _build_client() -> Optional[Hindsight]:
    """Initialize Hindsight client if API key is configured."""

    if not HINDSIGHT_API_KEY:
        return None
    try:
        return Hindsight(base_url=HINDSIGHT_BASE_URL, api_key=HINDSIGHT_API_KEY)
    except Exception:
        return None


hs_client = _build_client()
logger = logging.getLogger(__name__)


def _build_tags(memory: QuizMemory) -> List[str]:
    """Build structured tags for reliable filtering with new Hindsight SDK."""

    tags = [
        f"user_id:{memory.user_id}",
        f"topic:{memory.topic}",
        f"mistake_type:{memory.mistake_type}",
        f"difficulty:{memory.difficulty}",
        f"score:{memory.score}",
    ]
    if memory.question_id:
        tags.append(f"question_id:{memory.question_id}")
    if memory.subtopic:
        tags.append(f"subtopic:{memory.subtopic}")
    if memory.confidence is not None:
        tags.append(f"confidence:{memory.confidence}")
    if memory.time_spent_seconds is not None:
        tags.append(f"time_spent_seconds:{memory.time_spent_seconds}")
    if memory.source:
        tags.append(f"source:{memory.source}")
    if memory.session_id:
        tags.append(f"session_id:{memory.session_id}")
    return tags


def _extract_tag(tags: List[str], key: str) -> Optional[str]:
    """Extract one key:value tag value from a tag list."""

    prefix = f"{key}:"
    for tag in tags:
        if tag.startswith(prefix):
            return tag[len(prefix) :]
    return None


def _parse_score_from_text(text: str) -> int:
    """Best-effort score parsing from generated memory text."""

    if not text:
        return 0

    match = re.search(r"score\s+of\s+(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    match = re.search(r"scoring\s+(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    return 0


def _build_structured_content(memory: QuizMemory) -> str:
    """Build deterministic key-value content for robust recall parsing."""

    pairs = [
        ("user_id", memory.user_id),
        ("topic", memory.topic),
        ("mistake_type", memory.mistake_type),
        ("difficulty", memory.difficulty),
        ("score", str(memory.score)),
        ("timestamp", memory.timestamp.isoformat()),
    ]

    if memory.question_id:
        pairs.append(("question_id", memory.question_id))
    if memory.subtopic:
        pairs.append(("subtopic", memory.subtopic))
    if memory.confidence is not None:
        pairs.append(("confidence", str(memory.confidence)))
    if memory.time_spent_seconds is not None:
        pairs.append(("time_spent_seconds", str(memory.time_spent_seconds)))
    if memory.source:
        pairs.append(("source", memory.source))
    if memory.session_id:
        pairs.append(("session_id", memory.session_id))

    clean_pairs = [
        (key, str(value).replace(";", ",").strip())
        for key, value in pairs
        if value is not None
    ]
    body = "; ".join(f"{key}={value}" for key, value in clean_pairs)
    return f"QUIZ_MEMORY; {body};"


def _parse_memory_from_text(text: str, expected_user_id: str) -> Optional[Dict]:
    """Parse one memory record from recall text using key-value or legacy format."""

    if not text:
        return None

    key_values = dict(re.findall(r"([a-z_]+)=([^;]+)", text))
    if key_values:
        user_id = (key_values.get("user_id") or "").strip()
        if user_id and user_id != expected_user_id:
            return None

        score_raw = (key_values.get("score") or "").strip()
        score = int(score_raw) if score_raw.isdigit() else _parse_score_from_text(text)

        confidence_raw = (key_values.get("confidence") or "").strip()
        time_spent_raw = (key_values.get("time_spent_seconds") or "").strip()

        return {
            "user_id": user_id or expected_user_id,
            "topic": (key_values.get("topic") or "").strip(),
            "mistake_type": (key_values.get("mistake_type") or "").strip(),
            "difficulty": (key_values.get("difficulty") or "").strip(),
            "score": score,
            "question_id": (key_values.get("question_id") or "").strip() or None,
            "subtopic": (key_values.get("subtopic") or "").strip() or None,
            "confidence": int(confidence_raw) if confidence_raw.isdigit() else None,
            "time_spent_seconds": (
                int(time_spent_raw) if time_spent_raw.isdigit() else None
            ),
            "source": (key_values.get("source") or "").strip() or None,
            "session_id": (key_values.get("session_id") or "").strip() or None,
            "timestamp": (key_values.get("timestamp") or "").strip() or None,
        }

    # Legacy fallback for older natural-language records.
    topic_match = re.search(
        r"quiz on\s+(.+?)(?:\s+with\s+a\s+score|\s+on\s+a\s+[a-zA-Z]+\s+difficulty|,|\.)",
        text,
        re.IGNORECASE,
    )
    diff_match = re.search(r"on a\s+([a-zA-Z]+)\s+difficulty", text, re.IGNORECASE)
    mistake_match = re.search(r"making a\s+([a-zA-Z]+)\s+mistake", text, re.IGNORECASE)

    user_match = re.search(r"User ID:\s*([A-Za-z0-9_\-]+)", text)
    # Reject legacy records that do not explicitly include a user marker.
    if not user_match:
        return None

    parsed_user_id = user_match.group(1).strip()
    if parsed_user_id != expected_user_id:
        return None

    score = _parse_score_from_text(text)
    if score == 0 and not topic_match:
        return None

    return {
        "user_id": parsed_user_id,
        "topic": topic_match.group(1).strip() if topic_match else "",
        "mistake_type": mistake_match.group(1).capitalize() if mistake_match else "",
        "difficulty": diff_match.group(1).capitalize() if diff_match else "",
        "score": score,
        "question_id": None,
        "subtopic": None,
        "confidence": None,
        "time_spent_seconds": None,
        "source": None,
        "session_id": None,
        "timestamp": None,
    }


def _parse_timestamp(value: Optional[str]) -> datetime:
    """Parse timestamp values safely for recency-aware analytics."""

    if not value:
        return datetime.min
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return datetime.min


async def _call_client(method, **kwargs):
    """Call client method safely from async routes.

    Some SDK sync methods internally run an event loop and fail when called from
    FastAPI async context. Running those in a worker thread avoids nested-loop
    errors.
    """

    if inspect.iscoroutinefunction(method):
        return await method(**kwargs)
    return await asyncio.to_thread(method, **kwargs)


async def get_memories(user_id: str) -> List[Dict]:
    """Retrieve all memories for a user from Hindsight."""

    if not hs_client:
        return []

    try:
        if hasattr(hs_client, "search"):
            query = {"user_id": user_id}
            memories = await _call_client(
                hs_client.search,
                collection=HINDSIGHT_COLLECTION_NAME,
                query=query,
            )
            return memories if memories else []

        if hasattr(hs_client, "arecall"):
            recall_response = await _call_client(
                hs_client.arecall,
                bank_id=HINDSIGHT_COLLECTION_NAME,
                query=f"user_id={user_id}",
                budget="high",
            )

            results = getattr(recall_response, "results", []) or []
            parsed_memories: List[Dict] = []
            for result in results:
                text = getattr(result, "text", None)
                if text is None and isinstance(result, dict):
                    text = result.get("text")

                parsed = _parse_memory_from_text(text or "", user_id)
                if parsed:
                    parsed_memories.append(parsed)

            if parsed_memories:
                return parsed_memories

        memory_api = getattr(hs_client, "_memory_api", None)
        if memory_api and hasattr(memory_api, "list_memories"):
            response = await _call_client(
                memory_api.list_memories,
                bank_id=HINDSIGHT_COLLECTION_NAME,
                limit=500,
                offset=0,
            )
            items = getattr(response, "items", []) or []
            user_tag = f"user_id:{user_id}"

            converted: List[Dict] = []
            for item in items:
                tags = item.get("tags", []) or []
                if user_tag not in tags:
                    continue

                score_tag = _extract_tag(tags, "score")
                score = int(score_tag) if score_tag and score_tag.isdigit() else 0
                if score == 0:
                    score = _parse_score_from_text(item.get("text", ""))

                converted.append(
                    {
                        "user_id": user_id,
                        "topic": _extract_tag(tags, "topic") or "",
                        "mistake_type": _extract_tag(tags, "mistake_type") or "",
                        "difficulty": _extract_tag(tags, "difficulty") or "",
                        "score": score,
                        "question_id": _extract_tag(tags, "question_id"),
                        "subtopic": _extract_tag(tags, "subtopic"),
                        "confidence": (
                            int(_extract_tag(tags, "confidence"))
                            if (_extract_tag(tags, "confidence") or "").isdigit()
                            else None
                        ),
                        "time_spent_seconds": (
                            int(_extract_tag(tags, "time_spent_seconds"))
                            if (
                                _extract_tag(tags, "time_spent_seconds") or ""
                            ).isdigit()
                            else None
                        ),
                        "source": _extract_tag(tags, "source"),
                        "session_id": _extract_tag(tags, "session_id"),
                        "timestamp": item.get("date"),
                    }
                )

            if converted:
                return converted

        if hasattr(hs_client, "list_memories"):
            response = await _call_client(
                hs_client.list_memories,
                bank_id=HINDSIGHT_COLLECTION_NAME,
                limit=500,
                offset=0,
            )
            items = getattr(response, "items", []) or []
            user_tag = f"user_id:{user_id}"

            converted: List[Dict] = []
            for item in items:
                tags = item.get("tags", []) or []
                if user_tag not in tags:
                    continue

                score_tag = _extract_tag(tags, "score")
                score = int(score_tag) if score_tag and score_tag.isdigit() else 0
                if score == 0:
                    score = _parse_score_from_text(item.get("text", ""))

                converted.append(
                    {
                        "user_id": user_id,
                        "topic": _extract_tag(tags, "topic") or "",
                        "mistake_type": _extract_tag(tags, "mistake_type") or "",
                        "difficulty": _extract_tag(tags, "difficulty") or "",
                        "score": score,
                        "question_id": _extract_tag(tags, "question_id"),
                        "subtopic": _extract_tag(tags, "subtopic"),
                        "confidence": (
                            int(_extract_tag(tags, "confidence"))
                            if (_extract_tag(tags, "confidence") or "").isdigit()
                            else None
                        ),
                        "time_spent_seconds": (
                            int(_extract_tag(tags, "time_spent_seconds"))
                            if (
                                _extract_tag(tags, "time_spent_seconds") or ""
                            ).isdigit()
                            else None
                        ),
                        "source": _extract_tag(tags, "source"),
                        "session_id": _extract_tag(tags, "session_id"),
                        "timestamp": item.get("date"),
                    }
                )

            return converted

        return []
    except Exception as exc:
        logger.exception("Failed to read memories from Hindsight: %s", exc)
        return []


def filter_weak_topics(memories: List[Dict]) -> List[str]:
    """Return unique topics where score is below 50."""

    weak_topics = set()
    for memory in memories:
        score = memory.get("score", 0)
        topic = memory.get("topic", "")
        if score < 50 and topic:
            weak_topics.add(topic)
    return list(weak_topics)


def filter_strong_topics(memories: List[Dict]) -> List[str]:
    """Return unique topics where score is above 70."""

    strong_topics = set()
    for memory in memories:
        score = memory.get("score", 0)
        topic = memory.get("topic", "")
        if score > 70 and topic:
            strong_topics.add(topic)
    return list(strong_topics)


def calculate_insights(memories: List[Dict]) -> Dict:
    """Compute weak topics, strong topics, and most common mistake type."""

    insights = {
        "weak_topics": [],
        "strong_topics": [],
        "most_common_mistake_type": None,
    }

    if not memories:
        return insights

    insights["weak_topics"] = filter_weak_topics(memories)
    insights["strong_topics"] = filter_strong_topics(memories)

    mistake_types = [
        memory.get("mistake_type", "Unknown")
        for memory in memories
        if memory.get("mistake_type")
    ]
    if mistake_types:
        counter = Counter(mistake_types)
        most_common = counter.most_common(1)
        insights["most_common_mistake_type"] = (
            most_common[0][0] if most_common else None
        )

    return insights


def calculate_topic_mastery(
    memories: List[Dict], alpha: float = 0.35
) -> Dict[str, Dict]:
    """Compute recency-weighted mastery and trend per topic."""

    topics: Dict[str, List[Dict]] = {}
    for memory in memories:
        topic = (memory.get("topic") or "").strip()
        if not topic:
            continue
        topics.setdefault(topic, []).append(memory)

    mastery_by_topic: Dict[str, Dict] = {}
    for topic, attempts in topics.items():
        ordered_attempts = sorted(
            attempts,
            key=lambda item: _parse_timestamp(item.get("timestamp")),
        )
        scores = [
            max(0, min(100, int(item.get("score", 0)))) for item in ordered_attempts
        ]
        normalized = [score / 100.0 for score in scores]
        if not normalized:
            continue

        mastery = normalized[0]
        for score in normalized[1:]:
            mastery = alpha * score + (1 - alpha) * mastery

        recent_window = normalized[-3:]
        trend = recent_window[-1] - recent_window[0] if len(recent_window) > 1 else 0.0

        mastery_by_topic[topic] = {
            "topic": topic,
            "attempt_count": len(normalized),
            "latest_score": scores[-1],
            "mastery": round(mastery, 3),
            "trend": round(trend, 3),
            "recommended_difficulty": (
                "Easy" if mastery < 0.5 else "Medium" if mastery < 0.75 else "Hard"
            ),
        }

    return mastery_by_topic


def recommend_topics(memories: List[Dict], limit: int = 3) -> List[Dict]:
    """Prioritize next topics using mastery, trend, and mistake history."""

    topic_mastery = calculate_topic_mastery(memories)
    if not topic_mastery:
        return []

    topic_mistakes: Counter = Counter()
    for memory in memories:
        topic = memory.get("topic")
        if not topic:
            continue
        if int(memory.get("score", 0)) < 100:
            topic_mistakes[topic] += 1

    ranked: List[Dict] = []
    for topic, stats in topic_mastery.items():
        weakness = 1 - stats["mastery"]
        instability_penalty = max(0.0, -stats["trend"])
        mistake_pressure = min(1.0, topic_mistakes.get(topic, 0) / 5)
        priority_score = round(
            0.55 * weakness + 0.25 * instability_penalty + 0.2 * mistake_pressure, 3
        )

        if stats["mastery"] < 0.5:
            reason = "Low mastery"
            next_action = "Revisit core concept, then do 2 easy checks"
        elif stats["trend"] < -0.15:
            reason = "Recent decline"
            next_action = "Do a focused refresh with one medium and one hard question"
        else:
            reason = "Keep momentum"
            next_action = "Practice one mixed question to reinforce retention"

        ranked.append(
            {
                **stats,
                "mistake_count": topic_mistakes.get(topic, 0),
                "priority_score": priority_score,
                "reason": reason,
                "next_action": next_action,
            }
        )

    ranked.sort(key=lambda item: item["priority_score"], reverse=True)
    return ranked[: max(1, limit)]


async def store_memory(quiz_data: Dict) -> bool:
    """Store one quiz attempt in Hindsight memory."""

    if not hs_client:
        return False

    try:
        memory = QuizMemory(
            user_id=quiz_data.get("user_id"),
            topic=quiz_data.get("topic"),
            mistake_type=quiz_data.get("mistake_type"),
            difficulty=quiz_data.get("difficulty"),
            score=quiz_data.get("score"),
            question_id=quiz_data.get("question_id"),
            subtopic=quiz_data.get("subtopic"),
            confidence=quiz_data.get("confidence"),
            time_spent_seconds=quiz_data.get("time_spent_seconds"),
            source=quiz_data.get("source"),
            session_id=quiz_data.get("session_id"),
            user_answer=quiz_data.get("user_answer"),
            correct_answer=quiz_data.get("correct_answer"),
        )

        if hasattr(hs_client, "add"):
            await _call_client(
                hs_client.add,
                collection=HINDSIGHT_COLLECTION_NAME,
                records=[memory.to_dict()],
            )
            return True

        if hasattr(hs_client, "retain"):
            if hasattr(hs_client, "acreate_bank"):
                try:
                    await _call_client(
                        hs_client.acreate_bank,
                        bank_id=HINDSIGHT_COLLECTION_NAME,
                        name=HINDSIGHT_COLLECTION_NAME,
                    )
                except Exception:
                    # Bank may already exist; continue with retain.
                    pass
            elif hasattr(hs_client, "create_bank"):
                try:
                    await _call_client(
                        hs_client.create_bank,
                        bank_id=HINDSIGHT_COLLECTION_NAME,
                        name=HINDSIGHT_COLLECTION_NAME,
                    )
                except Exception:
                    # Bank may already exist; continue with retain.
                    pass

            if hasattr(hs_client, "aretain"):
                await _call_client(
                    hs_client.aretain,
                    bank_id=HINDSIGHT_COLLECTION_NAME,
                    content=_build_structured_content(memory),
                    timestamp=memory.timestamp,
                    tags=_build_tags(memory),
                )
            else:
                await _call_client(
                    hs_client.retain,
                    bank_id=HINDSIGHT_COLLECTION_NAME,
                    content=_build_structured_content(memory),
                    timestamp=memory.timestamp,
                    tags=_build_tags(memory),
                )
            return True

        return False
    except Exception as exc:
        logger.exception("Failed to store memory in Hindsight: %s", exc)
        return False
