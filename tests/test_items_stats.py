import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_database(db_session):
    """Ensure the test database is clean before each test.
    The `db_session` fixture is assumed to provide a fresh session scoped to the test.
    """
    # Assuming the fixture provides a clean DB; no explicit action needed.
    yield

def test_stats_empty_inventory():
    response = client.get('/items/stats')
    assert response.status_code == 200
    data = response.json()
    assert data['total_items'] == 0
    assert data['total_quantity'] == 0
    assert data['total_value'] == 0.0

def test_stats_with_items():
    # Create first item
    item1 = {
        'name': 'Widget',
        'description': 'A useful widget',
        'category': 'tools',
        'quantity': 2,
        'price': 10.5,
    }
    resp1 = client.post('/items', json=item1)
    assert resp1.status_code == 201

    # Create second item
    item2 = {
        'name': 'Gadget',
        'description': 'A fancy gadget',
        'category': 'gadgets',
        'quantity': 3,
        'price': 5.0,
    }
    resp2 = client.post('/items', json=item2)
    assert resp2.status_code == 201

    # Retrieve stats
    stats_resp = client.get('/items/stats')
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats['total_items'] == 2
    assert stats['total_quantity'] == 5
    # Expected total value: (2 * 10.5) + (3 * 5.0) = 21.0 + 15.0 = 36.0
    assert stats['total_value'] == 36.0
