"""Authentication and protected user routes."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, Token, TokenData, UserCreate
from app.services.user_service import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    verify_user_password,
)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user via JSON credentials and return a JWT token."""

    user = get_user_by_username(db, credentials.username)

    if not user or not verify_user_password(user, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user in the database."""

    if (
        not user_data.username
        or len(user_data.username) < 3
        or len(user_data.username) > 20
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-20 characters long",
        )

    if get_user_by_username(db, user_data.username.lower()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if user_data.email:
        if "@" not in user_data.email or "." not in user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email address",
            )
        if get_user_by_email(db, user_data.email.lower()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    if not user_data.password or len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long",
        )

    user = create_user(
        db,
        username=user_data.username,
        password=user_data.password,
        email=user_data.email,
    )

    return {
        "message": "User registered successfully",
        "username": user.username,
        "email": user.email or "",
        "status": "active",
    }


@router.get("/protected")
async def protected_route(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sample protected route requiring a valid JWT token."""

    user = get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {
        "message": f"Hello, {user.full_name}!",
        "username": user.username,
        "email": user.email,
    }


@router.get("/user/profile")
async def get_user_profile(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return profile information for the currently authenticated user."""

    user = get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "disabled": user.disabled,
    }
