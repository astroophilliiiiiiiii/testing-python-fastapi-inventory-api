"""Database utilities – switched to an in-memory SQLite DB for tests."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# ----------------------------------------------------------------------
# Database URL configuration.
# ----------------------------------------------------------------------
# In production, set the DATABASE_URL environment variable.
# For the test suite (when no variable is provided) we default to an
# in‑memory SQLite database that is shared across connections.
# The StaticPool ensures the same connection is reused, keeping the
# in‑memory database alive for the duration of the process.
# ----------------------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///:memory:"  # default to in‑memory SQLite for testing
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create all tables at import time so that the in‑memory DB is ready.
Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that provides a database session.

    The session is yielded to the path operation and closed automatically
    after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
