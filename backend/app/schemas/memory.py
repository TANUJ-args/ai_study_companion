"""Memory and insights schemas."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class BatchMemoryItem(BaseModel):
    """Single quiz attempt record for batch memory storage."""

    topic: str = Field(min_length=1)
    mistake_type: Literal["Conceptual", "Calculation", "Careless"]
    difficulty: Literal["Easy", "Medium", "Hard"]
    score: int = Field(ge=0, le=100)


class StoreMemoryBatchRequest(BaseModel):
    """Batch memory request with exactly two quiz attempts."""

    user_id: str = Field(min_length=1)
    attempts: list[BatchMemoryItem]

    @field_validator("attempts")
    @classmethod
    def validate_attempt_count(
        cls, value: list[BatchMemoryItem]
    ) -> list[BatchMemoryItem]:
        if len(value) != 2:
            raise ValueError("Exactly 2 attempts are required")
        return value
