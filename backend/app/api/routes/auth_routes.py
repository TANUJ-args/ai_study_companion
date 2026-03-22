"""Authentication and protected user routes."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import FAKE_USERS_DB, get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import Token, TokenData, UserCreate

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return a JWT token."""

    user = FAKE_USERS_DB.get(form_data.username)

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreate):
    """Register a new user in the in-memory store."""

    if (
        not user_data.username
        or len(user_data.username) < 3
        or len(user_data.username) > 20
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-20 characters long",
        )

    if user_data.username.lower() in [u.lower() for u in FAKE_USERS_DB.keys()]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if not user_data.email or "@" not in user_data.email or "." not in user_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        )

    if any(
        u["email"].lower() == user_data.email.lower() for u in FAKE_USERS_DB.values()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if not user_data.password or len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long",
        )

    hashed_password = hash_password(user_data.password)
    FAKE_USERS_DB[user_data.username] = {
        "username": user_data.username,
        "full_name": user_data.username.title(),
        "email": user_data.email,
        "hashed_password": hashed_password,
        "disabled": False,
    }

    return {
        "message": "User registered successfully",
        "username": user_data.username,
        "email": user_data.email,
        "status": "active",
    }


@router.get("/protected")
async def protected_route(current_user: TokenData = Depends(get_current_user)):
    """Sample protected route requiring a valid JWT token."""

    user = FAKE_USERS_DB.get(current_user.username)
    return {
        "message": f"Hello, {user['full_name']}!",
        "username": current_user.username,
        "email": user["email"],
    }


@router.get("/user/profile")
async def get_user_profile(current_user: TokenData = Depends(get_current_user)):
    """Return profile information for the currently authenticated user."""

    user = FAKE_USERS_DB.get(current_user.username)
    return {
        "username": user["username"],
        "full_name": user["full_name"],
        "email": user["email"],
        "disabled": user["disabled"],
    }
