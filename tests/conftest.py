"""Shared pytest fixtures.

Tests run against a **dedicated MySQL test database** (``kelontong_test`` by
default) so the real ``kelontong`` data is never touched. The connection uses
the same ``DB_*`` environment variables as the app (and ``.env``), and the test
database is created automatically if it does not exist. Each test starts with a
fresh, empty schema.

Override the test database name with ``TEST_DB_NAME`` if needed.
"""
import os
from urllib.parse import quote_plus

import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "kelontong_test")

# Ensure the dedicated test database exists *before* the app is imported
# (routers.py creates tables at import time).
_conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
try:
    with _conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{TEST_DB_NAME}`")
    _conn.commit()
finally:
    _conn.close()

# Point the app at the test database via the DATABASE_URL override.
os.environ["DATABASE_URL"] = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

import pytest
from fastapi.testclient import TestClient

import database
import models
from main import app


@pytest.fixture()
def client():
    """A TestClient backed by a fresh, empty test schema for each test."""
    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)
    with TestClient(app) as c:
        yield c
    models.Base.metadata.drop_all(bind=database.engine)
