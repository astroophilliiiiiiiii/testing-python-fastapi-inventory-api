"""Application entry point: creates the FastAPI app and wires the routers."""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import items

# Create database tables on startup. For a portfolio project this is a simple,
# self-contained way to bootstrap SQLite. A production deployment would use a
# migration tool such as Alembic instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    description=(
        "A small REST API for managing inventory items, built with FastAPI, "
        "SQLAlchemy 2.x and Pydantic v2."
    ),
    version="1.0.0",
    contact={"name": "Jessica Sales"},
)

app.include_router(items.router)


@app.get("/health", tags=["health"], summary="Service health check")
def health() -> dict[str, str]:
    """Liveness probe used by CI, Docker and load balancers."""
    return {"status": "ok"}
