"""Hindsight memory storage and analytics utilities."""

from collections import Counter
from datetime import datetime
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
        timestamp: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.topic = topic
        self.mistake_type = mistake_type
        self.difficulty = difficulty
        self.score = score
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict:
        """Convert memory to a serializable record."""

        return {
            "user_id": self.user_id,
            "topic": self.topic,
            "mistake_type": self.mistake_type,
            "difficulty": self.difficulty,
            "score": self.score,
            "timestamp": self.timestamp.isoformat(),
        }


def _build_client() -> Optional[Hindsight]:
    """Initialize Hindsight client if API key is configured."""

    if not HINDSIGHT_API_KEY:
        return None
    try:
        return Hindsight(base_url=HINDSIGHT_BASE_URL, api_key=HINDSIGHT_API_KEY)
    except Exception:
        return None


hs_client = _build_client()


def get_memories(user_id: str) -> List[Dict]:
    """Retrieve all memories for a user from Hindsight."""

    if not hs_client:
        return []

    try:
        query = {"user_id": user_id}
        memories = hs_client.search(collection=HINDSIGHT_COLLECTION_NAME, query=query)
        return memories if memories else []
    except Exception:
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


def store_memory(quiz_data: Dict) -> bool:
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
        )

        hs_client.add(
            collection=HINDSIGHT_COLLECTION_NAME,
            records=[memory.to_dict()],
        )
        return True
    except Exception:
        return False
