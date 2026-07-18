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
