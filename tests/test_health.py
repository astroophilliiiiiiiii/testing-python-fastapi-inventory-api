"""Tests for the service health endpoint."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok():
    """The /health endpoint should report the service as healthy."""
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_schema_is_available():
    """The OpenAPI schema should be exposed for documentation tooling."""
    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Inventory Management API"
