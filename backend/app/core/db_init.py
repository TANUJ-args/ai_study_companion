"""Database initialization utilities."""

from sqlalchemy.exc import OperationalError

from app.core.database import engine, Base


def init_db():
    """Initialize database tables. Call this on application startup."""
    try:
        # Create all tables from Base metadata
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables initialized successfully")
    except OperationalError as e:
        # Database not available (expected in test environments or if not configured)
        print(
            f"ℹ Database connection not available: {e}. Using in-memory or test database."
        )
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise


def drop_all():
    """Drop all tables. Use with caution!"""
    Base.metadata.drop_all(bind=engine)
    print("✓ All tables dropped")
