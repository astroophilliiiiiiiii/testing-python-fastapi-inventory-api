import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def create_sample_item(client: TestClient):
    payload = {
        "name": "Sample Item",
        "description": "A test item",
        "category": "test",
        "quantity": 5,
        "price": 10.0,
    }
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    return response.json()

def test_update_reject_blank_name(client: TestClient):
    item = create_sample_item(client)
    item_id = item["id"]
    resp = client.put(f"/items/{item_id}", json={"name": "   "})
    assert resp.status_code == 422

def test_update_reject_negative_price(client: TestClient):
    item = create_sample_item(client)
    item_id = item["id"]
    resp = client.put(f"/items/{item_id}", json={"price": -1.5})
    assert resp.status_code == 422

def test_update_reject_negative_quantity(client: TestClient):
    item = create_sample_item(client)
    item_id = item["id"]
    resp = client.put(f"/items/{item_id}", json={"quantity": -3})
    assert resp.status_code == 422

def test_update_partial_valid_fields(client: TestClient):
    item = create_sample_item(client)
    item_id = item["id"]
    new_price = 15.75
    resp = client.put(f"/items/{item_id}", json={"price": new_price})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["price"] == new_price
    # Ensure other fields remain unchanged
    assert updated["name"] == item["name"]
    assert updated["quantity"] == item["quantity"]
    # Verify via GET
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["price"] == new_price
    assert fetched["name"] == item["name"]
    assert fetched["quantity"] == item["quantity"]
