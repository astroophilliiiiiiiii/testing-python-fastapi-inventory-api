"""Pydantic v2 schemas for request validation and response serialization."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ItemBase(BaseModel):
    """Shared fields for inventory item payloads."""

    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    description: str | None = Field(
        default=None, max_length=1000, description="Optional description"
    )
    category: str | None = Field(
        default=None, max_length=100, description="Optional category for filtering"
    )
    quantity: int = Field(..., ge=0, description="Quantity in stock (must be non-negative)")
    price: float = Field(..., ge=0, description="Unit price (must be non-negative)")

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        """Reject names that are empty or only whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("name must not be empty or whitespace")
        return stripped


class ItemCreate(ItemBase):
    """Payload accepted when creating a new inventory item."""


class ItemUpdate(BaseModel):
    """Payload accepted when updating an inventory item.

    All fields are optional so clients can send partial updates.
    """

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=100)
    quantity: int | None = Field(default=None, ge=0)
    price: float | None = Field(default=None, ge=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str | None) -> str | None:
        """Reject names that are empty or only whitespace."""
        if value is None:
            return value
        stripped = value.strip()
        if not stripped:
            raise ValueError("name must not be empty or whitespace")
        return stripped


class ItemRead(ItemBase):
    """Inventory item representation returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
