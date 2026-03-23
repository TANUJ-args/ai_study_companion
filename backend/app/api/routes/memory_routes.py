"""Memory storage and learning insight routes."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.memory import StoreMemoryBatchRequest, StoreMemoryRequest
from app.services.memory_service import (
    calculate_insights,
    filter_weak_topics,
    get_memories,
    recommend_topics,
    store_memory,
)

router = APIRouter()


@router.post("/store-memory-batch", response_model=dict)
async def store_memory_batch(payload: StoreMemoryBatchRequest):
    """Store exactly two quiz attempts in memory."""

    stored_count = 0
    for attempt in payload.attempts:
        success = await store_memory(
            {
                "user_id": payload.user_id.strip(),
                "topic": attempt.topic,
                "mistake_type": attempt.mistake_type,
                "difficulty": attempt.difficulty,
                "score": attempt.score,
                "question_id": attempt.question_id,
                "subtopic": attempt.subtopic,
                "confidence": attempt.confidence,
                "time_spent_seconds": attempt.time_spent_seconds,
                "source": attempt.source,
                "session_id": attempt.session_id,
                "user_answer": attempt.user_answer,
                "correct_answer": attempt.correct_answer,
            }
        )
        if success:
            stored_count += 1

    if stored_count != 2:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stored {stored_count}/2 attempts in memory",
        )

    return {
        "message": "Memory updated for 2 attempts",
        "stored_count": stored_count,
        "status": "success",
    }


@router.post("/store-memory")
async def store_quiz_memory(quiz_data: StoreMemoryRequest):
    """Store one quiz attempt for later insight generation."""

    success = await store_memory(quiz_data.model_dump())

    if success:
        return {"message": "Quiz memory stored successfully", "status": "success"}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to store memory",
    )


@router.get("/weak-topics/{user_id}")
async def get_weak_topics(user_id: str):
    """Return unique topics where the user has weak quiz performance."""

    if not user_id or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id cannot be empty",
        )

    memories = await get_memories(user_id)
    if not memories:
        return {
            "user_id": user_id,
            "weak_topics": [],
            "message": "No quiz records found for this user",
        }

    weak_topics = filter_weak_topics(memories)
    return {"user_id": user_id, "weak_topics": weak_topics, "count": len(weak_topics)}


@router.get("/mistakes/{user_id}")
async def get_past_mistakes(user_id: str):
    """Return detailed list of past mistakes for a user."""

    if not user_id or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id cannot be empty",
        )

    memories = await get_memories(user_id)
    if not memories:
        return {
            "user_id": user_id,
            "mistakes": [],
            "message": "No quiz records found for this user",
        }

    mistakes = []
    for memory in memories:
        if memory.get("score", 0) < 100:
            mistakes.append(
                {
                    "topic": memory.get("topic"),
                    "mistake_type": memory.get("mistake_type"),
                    "score": memory.get("score"),
                    "difficulty": memory.get("difficulty"),
                    "timestamp": memory.get("timestamp"),
                }
            )

    return {"user_id": user_id, "mistakes": mistakes, "total_mistakes": len(mistakes)}


@router.get("/insights/{user_id}")
async def get_learning_insights(user_id: str):
    """Return aggregate learning insights computed from memory history."""

    if not user_id or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id cannot be empty",
        )

    memories = await get_memories(user_id)
    if not memories:
        return {
            "user_id": user_id,
            "insights": {
                "weak_topics": [],
                "strong_topics": [],
                "most_common_mistake_type": None,
            },
            "message": "No quiz records found for this user",
        }

    insights = calculate_insights(memories)
    return {"user_id": user_id, "insights": insights, "total_records": len(memories)}


@router.get("/recommendations/{user_id}")
async def get_topic_recommendations(user_id: str):
    """Return prioritized next topics and actions based on learning memory."""

    if not user_id or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id cannot be empty",
        )

    memories = await get_memories(user_id)
    if not memories:
        return {
            "user_id": user_id,
            "recommendations": [],
            "message": "No quiz records found for this user",
        }

    recommendations = recommend_topics(memories)
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "total_records": len(memories),
    }
