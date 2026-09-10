"""SQLAlchemy ORM models for the inventory domain."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _utcnow() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(UTC)


class InventoryItem(Base):
    """A single item tracked in the inventory.

    Attributes:
        id: Auto-incrementing primary key.
        name: Human-readable item name (required, non-empty).
        description: Optional free-text description.
        category: Optional category used for filtering.
        quantity: Number of units in stock (must be positive).
        price: Unit price in the store currency (must be non-negative).
        created_at: Creation timestamp (UTC).
        updated_at: Last modification timestamp (UTC).
    """

    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<InventoryItem id={self.id} name={self.name!r} quantity={self.quantity}>"
