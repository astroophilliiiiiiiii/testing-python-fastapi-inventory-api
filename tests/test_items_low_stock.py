'''Tests for the low_stock filter on the /items endpoint.'''

import pytest
from tests.test_items import _item_payload


def test_list_items_low_stock_true(client):
    """GET /items?low_stock=true should return only items with quantity < 5."""
    # Create a low‑stock item and a regular‑stock item
    client.post("/items", json=_item_payload(name="Pen", quantity=3, category="stationery"))
    client.post("/items", json=_item_payload(name="Mouse", quantity=10, category="electronics"))

    response = client.get("/items", params={"low_stock": "true"})

    assert response.status_code == 200
    body = response.json()
    # Only the low‑stock item should be returned
    assert len(body) == 1
    assert body[0]["name"] == "Pen"
    assert body[0]["quantity"] == 3


def test_list_items_low_stock_false(client):
    """GET /items?low_stock=false (or omitted) should return all items regardless of quantity."""
    client.post("/items", json=_item_payload(name="Keyboard", quantity=2, category="electronics"))
    client.post("/items", json=_item_payload(name="Notebook", quantity=8, category="stationery"))

    # Explicit false
    response_explicit = client.get("/items", params={"low_stock": "false"})
    # Omitted parameter (defaults to False)
    response_default = client.get("/items")

    for response in (response_explicit, response_default):
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2
        names = {item["name"] for item in body}
        assert names == {"Keyboard", "Notebook"}


def test_list_items_category_and_low_stock(client):
    """GET /items with both category and low_stock filters should apply both criteria."""
    # Matching category and low stock
    client.post("/items", json=_item_payload(name="Mouse", quantity=2, category="electronics"))
    # Matching category but not low stock
    client.post("/items", json=_item_payload(name="Headset", quantity=7, category="electronics"))
    # Different category, low stock
    client.post("/items", json=_item_payload(name="Pen", quantity=3, category="stationery"))

    response = client.get(
        "/items",
        params={"category": "electronics", "low_stock": "true"},
    )

    assert response.status_code == 200
    body = response.json()
    # Only the electronics item with low stock should be returned
    assert len(body) == 1
    assert body[0]["name"] == "Mouse"
    assert body[0]["category"] == "electronics"
    assert body[0]["quantity"] < 5
