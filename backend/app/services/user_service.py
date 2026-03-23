"""User authentication service using SQLAlchemy."""

from sqlalchemy.orm import Session
from app.models import User
from app.core.security import hash_password, verify_password


def get_user_by_username(db: Session, username: str) -> User | None:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    username: str,
    password: str,
    email: str | None = None,
) -> User:
    """Create a new user."""
    hashed_password = hash_password(password)
    user = User(
        username=username,
        email=email,
        full_name=username.title(),
        hashed_password=hashed_password,
        disabled=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_user_password(user: User, password: str) -> bool:
    """Verify user password."""
    return verify_password(password, user.hashed_password)
