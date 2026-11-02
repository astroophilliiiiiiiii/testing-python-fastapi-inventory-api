"""Tests for the inventory item CRUD endpoints."""

import pytest


def _item_payload(**overrides):
    """Build a valid item payload, applying any overrides."""
    payload = {
        'name': 'Wireless Mouse',
        'description': 'Ergonomic wireless mouse',
        'category': 'electronics',
        'quantity': 10,
        'price': 29.99,
    }
    payload.update(overrides)
    return payload


def test_create_item_success(client):
    """POST /items should create an item and echo the persisted fields."""
    response = client.post('/items', json=_item_payload())

    assert response.status_code == 201
    body = response.json()
    assert body['id'] == 1
    assert body['name'] == 'Wireless Mouse'
    assert body['quantity'] == 10
    assert body['category'] == 'electronics'
    assert 'created_at' in body and 'updated_at' in body


def test_create_item_zero_quantity_success(client):
    """POST /items with quantity 0 should be accepted."""
    response = client.post('/items', json=_item_payload(quantity=0))

    assert response.status_code == 201
    body = response.json()
    assert body['quantity'] == 0

@pytest.mark.parametrize(
    'bad_payload',
    [
        pytest.param({'quantity': -5}, id='negative-quantity'),
        pytest.param({'name': ''}, id='empty-name'),
        pytest.param({'name': '   '}, id='whitespace-name'),
        pytest.param({'price': -1.0}, id='negative-price'),
    ],
)
def test_create_item_validation_error(client, bad_payload):
    """Invalid payloads should be rejected with HTTP 422."""
    response = client.post('/items', json=_item_payload(**bad_payload))

    assert response.status_code == 422

def test_create_item_missing_required_field(client):
    """A payload missing a required field should return 422."""
    payload = _item_payload()
    del payload['name']

    response = client.post('/items', json=payload)

    assert response.status_code == 422

def test_list_items_returns_all(client):
    """GET /items should return every stored item ordered by id."""
    client.post('/items', json=_item_payload(name='Mouse'))
    client.post('/items', json=_item_payload(name='Keyboard', category='electronics'))
    client.post('/items', json=_item_payload(name='Notebook', category='stationery'))

    response = client.get('/items')

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    assert [item['name'] for item in body] == ['Mouse', 'Keyboard', 'Notebook']

def test_list_items_filter_by_category(client):
    """GET /items?category=... should only return matching items."""
    client.post('/items', json=_item_payload(name='Mouse', category='electronics'))
    client.post('/items', json=_item_payload(name='Keyboard', category='electronics'))
    client.post('/items', json=_item_payload(name='Notebook', category='stationery'))

    response = client.get('/items', params={'category': 'electronics'})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {item['name'] for item in body} == {'Mouse', 'Keyboard'}

def test_list_items_filter_no_match(client):
    """Filtering by an unknown category should return an empty list."""
    client.post('/items', json=_item_payload(category='electronics'))

    response = client.get('/items', params={'category': 'unknown'})

    assert response.status_code == 200
    assert response.json() == []

def test_get_item_by_id(client):
    """GET /items/{id} should return the requested item."""
    created = client.post('/items', json=_item_payload()).json()

    response = client.get(f"/items/{created['id']}")

    assert response.status_code == 200
    assert response.json()['id'] == created['id']
    assert response.json()['name'] == created['name']

def test_get_item_not_found(client):
    """GET /items/{id} for a missing id should return 404."""
    response = client.get('/items/9999')

    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()

def test_update_item_success(client):
    """PUT /items/{id} should apply a partial update and persist it."""
    created = client.post('/items', json=_item_payload()).json()

    response = client.put(f"/items/{created['id']}", json={'quantity': 20})
    assert response.status_code == 200
    assert response.json()['quantity'] == 20

def test_update_item_not_found(client):
    """PUT /items/{id} for a missing id should return 404."""
    response = client.put('/items/9999', json={'quantity': 5})
    assert response.status_code == 404

def test_delete_item_success(client):
    """DELETE /items/{id} should remove the item and return 204."""
    created = client.post('/items', json=_item_payload()).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204
    # subsequent get should be 404
    assert client.get(f"/items/{created['id']}").status_code == 404

def test_delete_item_not_found(client):
    """DELETE /items/{id} for a missing id should return 404."""
    response = client.delete('/items/9999')
    assert response.status_code == 404
