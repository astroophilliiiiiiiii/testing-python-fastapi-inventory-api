"""Database configuration: engine, session factory, and declarative base.

The default database is a local SQLite file. The URL can be overridden via the
``DATABASE_URL`` environment variable, which makes it easy to run against an
alternate database (for example, in CI or production) without code changes.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Default to a local SQLite database file in the project directory.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

# ``check_same_thread`` is required for SQLite when used with FastAPI because a
# single connection may be shared across threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


def get_db():
    """FastAPI dependency that yields a database session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
