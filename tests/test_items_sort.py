import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope='function')
def create_sample_items():
    # Clean up any existing items (depends on test DB fixture, assuming isolated DB per test)
    # Create three items with varying attributes
    items = [
        {
            'name': 'Apple',
            'description': 'Fresh apple',
            'category': 'fruit',
            'quantity': 10,
            'price': 1.5,
        },
        {
            'name': 'Banana',
            'description': 'Yellow banana',
            'category': 'fruit',
            'quantity': 5,
            'price': 0.9,
        },
        {
            'name': 'Carrot',
            'description': 'Orange carrot',
            'category': 'vegetable',
            'quantity': 20,
            'price': 0.6,
        },
    ]
    created = []
    for payload in items:
        response = client.post('/items', json=payload)
        assert response.status_code == 201
        created.append(response.json())
    return created

def test_sort_by_price_ascending(create_sample_items):
    response = client.get('/items?sort_by=price&order=asc')
    assert response.status_code == 200
    data = response.json()
    prices = [item['price'] for item in data]
    assert prices == sorted(prices)

def test_sort_by_name_descending(create_sample_items):
    response = client.get('/items?sort_by=name&order=desc')
    assert response.status_code == 200
    data = response.json()
    names = [item['name'] for item in data]
    assert names == sorted(names, reverse=True)

def test_invalid_sort_by_returns_422(create_sample_items):
    response = client.get('/items?sort_by=invalid_column')
    assert response.status_code == 422

def test_invalid_order_returns_422(create_sample_items):
    response = client.get('/items?order=sideways')
    assert response.status_code == 422
