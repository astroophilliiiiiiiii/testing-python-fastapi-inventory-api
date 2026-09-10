# Inventory Management API

[![CI](https://github.com/jessicasalestech/python-fastapi-inventory-api/actions/workflows/ci.yml/badge.svg)](https://github.com/jessicasalestech/python-fastapi-inventory-api/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A clean, well-tested REST API for inventory management built with **FastAPI**,
**SQLAlchemy 2.x**, **Pydantic v2** and **SQLite**. This project is a portfolio
showcase demonstrating modern Python API development practices: layered
architecture, dependency injection, schema validation, isolated tests and a
CI pipeline.

---

## Features

- **Full CRUD** for inventory items (`POST`, `GET`, `GET by id`, `PUT`, `DELETE`).
- **Category filtering** on the list endpoint (`GET /items?category=...`).
- **Strict input validation** with Pydantic v2 — positive quantity, non-empty
  name, non-negative price — returning HTTP `422` on invalid payloads.
- **Proper HTTP semantics** — `201 Created`, `204 No Content` and `404 Not Found`.
- **Layered architecture** — routers → CRUD → models, with a shared DB session
  provided via a FastAPI dependency.
- **Automated tests** using `pytest` and `httpx` against an isolated in-memory
  SQLite database, so tests never touch production data.
- **Linting** with `ruff` and a **CI workflow** running on Python 3.11 and 3.12.
- **Docker-ready** with a multi-stage `slim` image and a container health check.
- **Auto-generated API docs** at `/docs` (Swagger UI) and `/redoc`.

---

## Project Structure

```text
python-fastapi-inventory-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app, router wiring and /health endpoint
│   ├── database.py        # Engine, SessionLocal, Base and get_db dependency
│   ├── models.py          # SQLAlchemy InventoryItem model
│   ├── schemas.py         # Pydantic v2 request/response schemas
│   ├── crud.py            # Create / read / update / delete data logic
│   └── routers/
│       ├── __init__.py
│       └── items.py       # REST router for /items endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Isolated in-memory DB + TestClient fixtures
│   ├── test_health.py     # Health and OpenAPI schema tests
│   └── test_items.py      # CRUD and validation tests
├── .github/workflows/ci.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml         # ruff + pytest configuration
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11 or newer.

### Installation

```bash
# Clone the repository
git clone https://github.com/jessicasalestech/python-fastapi-inventory-api.git
cd python-fastapi-inventory-api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows (git-bash): source .venv/Scripts/activate
                                 # Windows (PowerShell): .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt
```

### Run the API

```bash
uvicorn app.main:app --reload
```

The API is now available at <http://127.0.0.1:8000>. Interactive documentation
is at <http://127.0.0.1:8000/docs>.

The database is a local SQLite file (`inventory.db`) created automatically on
startup. Override it with the `DATABASE_URL` environment variable if needed
(see `.env.example`).

---

## API Endpoints

| Method   | Path                | Description                                   | Success | Errors            |
| -------- | ------------------- | --------------------------------------------- | ------- | ----------------- |
| `GET`    | `/health`           | Service health check                          | `200`   | —                 |
| `POST`   | `/items`            | Create a new inventory item                   | `201`   | `422`             |
| `GET`    | `/items`            | List items (optional `?category=` filter)     | `200`   | —                 |
| `GET`    | `/items/{id}`       | Retrieve a single item by id                  | `200`   | `404`             |
| `PUT`    | `/items/{id}`       | Partially update an item                      | `200`   | `404`, `422`      |
| `DELETE` | `/items/{id}`       | Delete an item                                | `204`   | `404`             |

### Item schema

| Field         | Type      | Required | Constraints                        |
| ------------- | --------- | -------- | ---------------------------------- |
| `name`        | `string`  | yes      | 1–255 chars, non-blank             |
| `description` | `string`  | no       | Max 1000 chars                     |
| `category`    | `string`  | no       | Max 100 chars                      |
| `quantity`    | `integer` | yes      | Must be **greater than 0**         |
| `price`       | `number`  | yes      | Must be **≥ 0**                    |
| `id`          | `integer` | —        | Server-generated (responses only)  |
| `created_at`  | `datetime`| —        | Server-generated (responses only)  |
| `updated_at`  | `datetime`| —        | Server-generated (responses only)  |

---

## Usage Examples

All examples assume the server is running on `http://127.0.0.1:8000`.

### Health check

```bash
curl -s http://127.0.0.1:8000/health
# {"status":"ok"}
```

### Create an item

```bash
curl -s -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "category": "electronics",
    "quantity": 10,
    "price": 29.99
  }'
# {"id":1,"name":"Wireless Mouse","description":"Ergonomic wireless mouse",
#  "category":"electronics","quantity":10,"price":29.99,"created_at":"...","updated_at":"..."}
```

### List items (with optional category filter)

```bash
curl -s http://127.0.0.1:8000/items
curl -s "http://127.0.0.1:8000/items?category=electronics"
```

### Get an item by id

```bash
curl -s http://127.0.0.1:8000/items/1
```

### Update an item (partial update)

```bash
curl -s -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 42}'
```

### Delete an item

```bash
curl -s -X DELETE http://127.0.0.1:8000/items/1 -w "%{http_code}\n"
# 204
```

### Validation error example

```bash
curl -s -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "", "quantity": -1, "price": 5}'
# HTTP 422 with a detailed validation error body
```

---

## Running the Tests

```bash
pytest -v
```

Each test runs against a fresh, isolated in-memory SQLite database via a
dependency override, so the suite is fast and side-effect free. The tests cover
the health endpoint, create (success and validation failures), list and list
filtering, get by id (success and 404), update (success, validation and 404) and
delete (success and 404).

Run the linter:

```bash
ruff check .
```

---

## Docker

Build and run the container:

```bash
docker build -t inventory-api .
docker run --rm -p 8000:8000 inventory-api
```

The image is built in multiple stages and runs as a non-root user. A container
`HEALTHCHECK` polls `/health`.

---

## Tech Stack

| Layer      | Technology            |
| ---------- | --------------------- |
| Framework  | FastAPI               |
| Server     | Uvicorn               |
| ORM        | SQLAlchemy 2.x        |
| Database   | SQLite                |
| Validation | Pydantic v2           |
| Testing    | pytest + httpx        |
| Linting    | ruff                  |
| CI         | GitHub Actions        |

---

## License

This project is provided for portfolio and educational purposes.
