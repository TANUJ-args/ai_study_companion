"""Shared API dependencies and in-memory data stores."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_token, hash_password
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

FAKE_USERS_DB = {
    "user1": {
        "username": "user1",
        "full_name": "John Doe",
        "email": "user1@example.com",
        "hashed_password": hash_password("password123"),
        "disabled": False,
    },
    "user2": {
        "username": "user2",
        "full_name": "Jane Smith",
        "email": "user2@example.com",
        "hashed_password": hash_password("securepass456"),
        "disabled": False,
    },
}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Validate JWT token and return authenticated user payload."""

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_token(token)
    if token_data is None:
        raise credential_exception

    user = FAKE_USERS_DB.get(token_data.username)
    if user is None:
        raise credential_exception

    return token_data
