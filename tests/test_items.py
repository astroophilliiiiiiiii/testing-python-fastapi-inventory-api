import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_item_success():
    payload = {"name": "Item A", "quantity": 5, "price": 10.0}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Item A"
    assert data["quantity"] == 5
    assert data["price"] == 10.0


@pytest.mark.parametrize(
    "bad_payload",
    [
        # quantity = 0 is now allowed – it is a valid payload, so we no longer test it here
        pytest.param({"quantity": -5}, id="negative-quantity"),
        pytest.param({"name": ""}, id="empty-name"),
        pytest.param({"name": "   "}, id="whitespace-name"),
        pytest.param({"price": -1.0}, id="negative-price"),
    ],
)
def test_create_item_bad_payload(bad_payload):
    response = client.post("/items", json=bad_payload)
    assert response.status_code == 422
