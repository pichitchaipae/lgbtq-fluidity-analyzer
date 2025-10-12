"""API integration tests."""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_endpoint_returns_scores() -> None:
    client = TestClient(app)
    payload = {
        "media1": 3,
        "media2": 2,
        "family1": 1,
        "family2": 2,
        "family3": 1,
        "community1": 2,
        "community2": 1,
        "culture1": 2,
        "culture2": 2,
        "exploration1": 2,
        "exploration2": 2,
        "school1": 1,
    }

    response = client.post("/api/v1/analysis", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "overall_score" in body
    assert "section_scores" in body
    assert len(body["insights"]) >= 1
