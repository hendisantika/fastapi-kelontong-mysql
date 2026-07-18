# fastapi-kelontong-mysql

A FastAPI service for managing a kelontong (grocery store) merchandise catalog, backed by MySQL.

## Requirements

- Python 3.10+
- MySQL server with a `kelontong` database

Python dependencies are pinned in [`requirements.txt`](requirements.txt):

| Package | Version | Purpose |
|---|---|---|
| fastapi | 0.139.2 | Web framework |
| uvicorn | 0.51.0 | ASGI server |
| SQLAlchemy | 2.0.51 | ORM |
| PyMySQL | 1.2.0 | MySQL driver |
| python-dotenv | 1.2.2 | Loads `.env` configuration |
| pytest | 9.1.1 | Test runner (dev) |
| httpx | 0.28.1 | Test client transport (dev) |

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure the database connection
cp .env.example .env             # then edit .env with your credentials
```

### Environment variables

Configuration is read from the environment (or a local `.env` file). Defaults
match a local MySQL instance:

| Variable | Default | Description |
|---|---|---|
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | *(empty)* | MySQL password |
| `DB_HOST` | `localhost` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_NAME` | `kelontong` | Database name |

`.env` is git-ignored — your real credentials never get committed.

## Running

```bash
uvicorn main:app --reload
```

The API is served at http://localhost:8000.

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API endpoints

All merchandise routes are prefixed with `/api`.

| Method | Path | Description |
|---|---|---|
| POST | `/api/merchandises` | Create a merchandise item |
| GET | `/api/merchandise` | List all merchandise |
| GET | `/api/merchandise/{id}` | Get a merchandise item by id |
| GET | `/api/merchandise/search/` | Search by `name` and/or `category` |
| PUT | `/api/merchandise/{id}` | Update a merchandise item |
| DELETE | `/api/merchandise/{id}` | Delete a merchandise item |

## Example requests

Assuming the server is running at `http://localhost:8000`.

Create a merchandise item:

```bash
curl -X POST http://localhost:8000/api/merchandises \
  -H "Content-Type: application/json" \
  -d '{"name": "Indomie Goreng", "category_id": 1, "price": 3000, "stock": 50}'
```

List all merchandise:

```bash
curl http://localhost:8000/api/merchandise
```

Get a merchandise item by id:

```bash
curl http://localhost:8000/api/merchandise/1
```

Search by name and/or category:

```bash
curl "http://localhost:8000/api/merchandise/search/?name=Indomie&category=1"
```

Update a merchandise item:

```bash
curl -X PUT http://localhost:8000/api/merchandise/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Indomie Goreng Jumbo", "category_id": 1, "price": 3500, "stock": 40}'
```

Delete a merchandise item:

```bash
curl -X DELETE http://localhost:8000/api/merchandise/1
```

## Testing

Endpoint tests live in the [`tests/`](tests/) folder and run against a
**dedicated MySQL test database** (`kelontong_test` by default) so your real
`kelontong` data is never touched. The test database is created automatically
if it does not exist, and each test runs against a fresh schema.

Tests use the same `DB_*` variables (and `.env`) as the app. Override the test
database name with `TEST_DB_NAME` if needed.

```bash
# MySQL must be running and reachable with your DB_* credentials
pytest
```
