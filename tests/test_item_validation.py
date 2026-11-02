import pytest

def _item_payload(**overrides):
    """Helper to generate a valid payload and apply overrides."""
    payload = {
        "name": "Test Item",
        "description": "A test description",
        "category": "test",
        "quantity": 5,
        "price": 10.0,
    }
    payload.update(overrides)
    return payload

@pytest.mark.parametrize(
    "bad_payload, expected_detail",
    [
        ({"name": ""}, "name must not be empty or whitespace"),
        ({"name": "   "}, "name must not be empty or whitespace"),
        ({"quantity": 0}, "ensure this value is greater than 0"),
        ({"quantity": -1}, "ensure this value is greater than 0"),
        ({"price": -5.0}, "ensure this value is greater than or equal to 0"),
    ],
    ids=[
        "empty-name",
        "whitespace-name",
        "zero-quantity",
        "negative-quantity",
        "negative-price",
    ],
)
def test_create_item_invalid_inputs(client, bad_payload, expected_detail):
    """Each malformed payload should result in a 422 response with a helpful error."""
    response = client.post("/items", json=_item_payload(**bad_payload))
    assert response.status_code == 422
    # FastAPI returns a list of errors; ensure our custom message appears somewhere.
    error_body = response.json()
    # The error detail can be a list of dicts; check that any message contains the expected snippet.
    messages = []
    if isinstance(error_body.get("detail"), list):
        for err in error_body["detail"]:
            messages.append(err.get("msg", ""))
    else:
        messages.append(error_body.get("detail", ""))
    assert any(expected_detail in msg for msg in messages)
