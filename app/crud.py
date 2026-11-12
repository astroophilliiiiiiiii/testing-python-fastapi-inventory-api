'''CRUD operations for inventory items.

This module contains all database access logic so the routers stay thin and the
data layer stays testable in isolation.
'''

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_item(db: Session, item: schemas.ItemCreate) -> models.InventoryItem:
    '''Persist a new inventory item and return the stored record.'''
    db_item = models.InventoryItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list_items(
    db: Session,
    category: str | None = None,
    sort_by: str = 'id',
    order: str = 'asc',
) -> list[models.InventoryItem]:
    '''Return all inventory items, optionally filtered by category and sorted.

    Parameters
    ----------
    db: Session
        Database session.
    category: str | None
        Optional category filter.
    sort_by: str
        Field name to sort by. Must be one of 'id', 'name', 'price', 'quantity'.
    order: str
        Sort direction, either 'asc' or 'desc'.
    '''
    allowed_sort_fields = {'id', 'name', 'price', 'quantity'}
    allowed_orders = {'asc', 'desc'}

    if sort_by not in allowed_sort_fields:
        raise ValueError(f'Invalid sort_by value: {sort_by}')
    if order not in allowed_orders:
        raise ValueError(f'Invalid order value: {order}')

    stmt = select(models.InventoryItem)
    if category is not None:
        stmt = stmt.where(models.InventoryItem.category == category)

    # Dynamically build order clause
    column = getattr(models.InventoryItem, sort_by)
    stmt = stmt.order_by(column.asc() if order == 'asc' else column.desc())

    return list(db.execute(stmt).scalars().all())


def get_item(db: Session, item_id: int) -> models.InventoryItem | None:
    '''Return a single inventory item by id, or ``None`` if not found.'''
    return db.get(models.InventoryItem, item_id)


def update_item(
    db: Session, item_id: int, item: schemas.ItemUpdate
) -> models.InventoryItem | None:
    '''Apply a partial update to an item and return it, or ``None`` if missing.'''
    db_item = db.get(models.InventoryItem, item_id)
    if db_item is None:
        return None

    changes = item.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> models.InventoryItem | None:
    '''Delete an item and return the deleted record, or ``None`` if missing.'''
    db_item = db.get(models.InventoryItem, item_id)
    if db_item is None:
        return None

    db.delete(db_item)
    db.commit()
    return db_item
