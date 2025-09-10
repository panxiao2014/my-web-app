import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config.config import TEST_PING


def test_ping_returns_test_ping_string():
    client = TestClient(app)
    response = client.get("/ping")
    assert response.status_code == 200
    body = response.json()
    assert body.get("message") == TEST_PING

