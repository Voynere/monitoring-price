from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_eval_questions_file_has_minimum_size() -> None:
    path = Path(__file__).parent / "eval_questions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert len(data) >= 20
    for item in data:
        assert "question" in item
        assert "module" in item
