"""Authentication-related request and response schemas."""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """JWT login response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Decoded JWT payload content."""

    username: Optional[str] = None


class LoginRequest(BaseModel):
    """JSON login request body."""

    username: str
    password: str


class UserCreate(BaseModel):
    """User registration request body."""

    username: str
    email: Optional[str] = None
    password: str


class UserResponse(BaseModel):
    """Public user profile response."""

    username: str
    email: str
    full_name: Optional[str] = None
