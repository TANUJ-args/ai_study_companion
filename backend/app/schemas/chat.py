"""AI chat request schemas."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Incoming chat message payload."""

    message: str
