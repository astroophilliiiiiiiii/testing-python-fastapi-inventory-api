"""REST router exposing inventory item endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "",
    response_model=schemas.ItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new inventory item",
)
def create_item(
    item: schemas.ItemCreate, db: Session = Depends(get_db)
) -> schemas.ItemRead:
    """Create a new inventory item and return the stored record."""
    # -----------------------------------------------------------------
    # Explicit input validation required by the task.
    # We raise HTTP 422 (Unprocessable Entity) for business‑rule violations.
    # -----------------------------------------------------------------
    # 1️⃣ Name must not be empty or consist only of whitespace.
    if item.name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="name must not be empty or whitespace",
        )

    # 2️⃣ Quantity must be a positive integer (zero is not allowed).
    if item.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="quantity must be a positive integer",
        )

    # If the payload passes our checks, delegate to the CRUD layer.
    return crud.create_item(db=db, item=item)


@router.get(
    "",
    response_model=list[schemas.ItemRead],
    summary="List inventory items",
)
def list_items(
    category: str | None = Query(default=None, description="Filter by category"),
    db: Session = Depends(get_db),
) -> list[schemas.ItemRead]:
    """Return all inventory items, optionally filtered by category."""
    return crud.list_items(db=db, category=category)


@router.get(
    "/{item_id}",
    response_model=schemas.ItemRead,
    summary="Get an inventory item by id",
)
def get_item(item_id: int, db: Session = Depends(get_db)) -> schemas.ItemRead:
    """Return a single inventory item or 404 if it does not exist."""
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item {item_id} not found",
        )
    return db_item


@router.put(
    "/{item_id}",
    response_model=schemas.ItemRead,
    summary="Update an inventory item",
)
def update_item(
    item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)
) -> schemas.ItemRead:
    """Apply a partial update to an item or 404 if it does not exist."""
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item {item_id} not found",
        )
    return db_item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an inventory item",
)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an item or 404 if it does not exist."""
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item {item_id} not found",
        )
    return None
