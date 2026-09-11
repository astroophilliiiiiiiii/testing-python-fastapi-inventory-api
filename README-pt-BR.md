# Inventory Management API

[![Português](https://img.shields.io/badge/Portugu%C3%AAs-green?style=plastic&logo=openbadges&logoColor=white)](README-pt-BR.md) [![English](https://img.shields.io/badge/English-blue?style=plastic&logo=openbadges&logoColor=white)](README.md)

[![CI](https://github.com/jessicasalestech/python-fastapi-inventory-api/actions/workflows/ci.yml/badge.svg)](https://github.com/jessicasalestech/python-fastapi-inventory-api/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Uma API REST limpa e bem testada para gerenciamento de inventário, construída
com **FastAPI**, **SQLAlchemy 2.x**, **Pydantic v2** e **SQLite**. Este projeto
é uma demonstração de portfólio que mostra práticas modernas de desenvolvimento
de APIs em Python: arquitetura em camadas, injeção de dependências, validação
de esquemas, testes isolados e um pipeline de CI.

---

## Funcionalidades

- **CRUD completo** para itens de inventário (`POST`, `GET`, `GET por id`, `PUT`, `DELETE`).
- **Filtro por categoria** no endpoint de listagem (`GET /items?category=...`).
- **Validação de entrada rigorosa** com Pydantic v2 — quantidade positiva,
  nome não vazio, preço não negativo — retornando HTTP `422` em cargas inválidas.
- **Semântica HTTP correta** — `201 Created`, `204 No Content` e `404 Not Found`.
- **Arquitetura em camadas** — routers → CRUD → models, com uma sessão de banco
  compartilhada fornecida por uma dependência do FastAPI.
- **Testes automatizados** usando `pytest` e `httpx` contra um banco SQLite
  isolado em memória, para que os testes nunca toquem dados de produção.
- **Linting** com `ruff` e um **workflow de CI** executando em Python 3.11 e 3.12.
- **Pronto para Docker** com uma imagem `slim` multi-stage e health check no contêiner.
- **Documentação de API gerada automaticamente** em `/docs` (Swagger UI) e `/redoc`.

---

## Estrutura do Projeto

```text
python-fastapi-inventory-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # Aplicação FastAPI, wiring dos routers e endpoint /health
│   ├── database.py        # Engine, SessionLocal, Base e dependência get_db
│   ├── models.py          # Modelo InventoryItem do SQLAlchemy
│   ├── schemas.py         # Schemas de requisição/resposta do Pydantic v2
│   ├── crud.py            # Lógica de dados criar / ler / atualizar / excluir
│   └── routers/
│       ├── __init__.py
│       └── items.py       # Router REST para os endpoints de /items
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Banco em memória isolado + fixtures do TestClient
│   ├── test_health.py     # Testes de health e schema OpenAPI
│   └── test_items.py      # Testes de CRUD e validação
├── .github/workflows/ci.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml         # Configuração do ruff + pytest
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Começando

### Pré-requisitos

- Python 3.11 ou mais recente.

### Instalação

```bash
# Clone o repositório
git clone https://github.com/jessicasalestech/python-fastapi-inventory-api.git
cd python-fastapi-inventory-api

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows (git-bash): source .venv/Scripts/activate
                                 # Windows (PowerShell): .venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt -r requirements-dev.txt
```

### Execute a API

```bash
uvicorn app.main:app --reload
```

A API agora está disponível em <http://127.0.0.1:8000>. A documentação
interativa está em <http://127.0.0.1:8000/docs>.

O banco de dados é um arquivo SQLite local (`inventory.db`) criado
automaticamente na inicialização. Substitua-o pela variável de ambiente
`DATABASE_URL` se necessário (veja `.env.example`).

---

## Endpoints da API

| Método   | Caminho            | Descrição                           | Sucesso | Erros             |
| -------- | ------------------- | ----------------------------------- | ------- | ----------------- |
| `GET`    | `/health`           | Verificação de saúde do serviço     | `200`   | —                 |
| `POST`   | `/items`            | Cria um novo item de inventário     | `201`   | `422`             |
| `GET`    | `/items`            | Lista itens (filtro opcional `?category=`) | `200` | —                 |
| `GET`    | `/items/{id}`       | Obtém um único item por id          | `200`   | `404`             |
| `PUT`    | `/items/{id}`       | Atualiza parcialmente um item       | `200`   | `404`, `422`      |
| `DELETE` | `/items/{id}`       | Exclui um item                      | `204`   | `404`             |

### Schema do item

| Campo         | Tipo       | Obrigatório | Restrições                      |
| ------------- | ---------- | ----------- | ------------------------------- |
| `name`        | `string`   | sim         | 1–255 caracteres, não em branco |
| `description` | `string`   | não         | Máx. 1000 caracteres            |
| `category`    | `string`   | não         | Máx. 100 caracteres             |
| `quantity`    | `integer`  | sim         | Deve ser **maior que 0**        |
| `price`       | `number`   | sim         | Deve ser **≥ 0**                |
| `id`          | `integer`  | —           | Gerado pelo servidor (somente nas respostas) |
| `created_at`  | `datetime` | —           | Gerado pelo servidor (somente nas respostas) |
| `updated_at`  | `datetime` | —           | Gerado pelo servidor (somente nas respostas) |

---

## Exemplos de Uso

Todos os exemplos assumem que o servidor está executando em `http://127.0.0.1:8000`.

### Verificação de saúde

```bash
curl -s http://127.0.0.1:8000/health
# {"status":"ok"}
```

### Criar um item

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

### Listar itens (com filtro de categoria opcional)

```bash
curl -s http://127.0.0.1:8000/items
curl -s "http://127.0.0.1:8000/items?category=electronics"
```

### Obter um item por id

```bash
curl -s http://127.0.0.1:8000/items/1
```

### Atualizar um item (atualização parcial)

```bash
curl -s -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 42}'
```

### Excluir um item

```bash
curl -s -X DELETE http://127.0.0.1:8000/items/1 -w "%{http_code}\n"
# 204
```

### Exemplo de erro de validação

```bash
curl -s -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "", "quantity": -1, "price": 5}'
# HTTP 422 com um corpo de erro de validação detalhado
```

---

## Executando os Testes

```bash
pytest -v
```

Cada teste roda contra um banco SQLite em memória, novo e isolado, via um
override de dependência, então a suíte é rápida e sem efeitos colaterais. Os
testes cobrem o endpoint de health, criação (sucesso e falhas de validação),
listagem e filtro, obtenção por id (sucesso e 404), atualização (sucesso,
validação e 404) e exclusão (sucesso e 404).

Execute o linter:

```bash
ruff check .
```

---

## Docker

Compile e execute o contêiner:

```bash
docker build -t inventory-api .
docker run --rm -p 8000:8000 inventory-api
```

A imagem é construída em vários estágios e roda como um usuário não-root. Um
`HEALTHCHECK` do contêiner consulta `/health`.

---

## Stack Tecnológica

| Camada       | Tecnologia            |
| ------------ | --------------------- |
| Framework    | FastAPI               |
| Servidor     | Uvicorn               |
| ORM          | SQLAlchemy 2.x        |
| Banco de dados | SQLite             |
| Validação    | Pydantic v2           |
| Testes       | pytest + httpx        |
| Linting      | ruff                  |
| CI           | GitHub Actions        |

---

## Licença

Este projeto é fornecido para fins educacionais e de portfólio.