"""HTTP-level tests for the FastAPI layer (requires fastapi + httpx)."""
import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)
PASSAU = {"lat": 48.5745, "lng": 13.46}


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_categories():
    assert "plumber" in client.get("/api/categories").json()


def test_nearby_returns_sorted_results():
    res = client.get("/api/providers/nearby", params={**PASSAU, "radius_km": 5})
    assert res.status_code == 200
    distances = [p["distance_km"] for p in res.json()]
    assert distances and distances == sorted(distances)


def test_unknown_category_is_bad_request():
    res = client.get("/api/providers/nearby", params={**PASSAU, "category": "astronaut"})
    assert res.status_code == 400


def test_query_validation():
    res = client.get("/api/providers/nearby", params={**PASSAU, "radius_km": 0})
    assert res.status_code == 422


def test_frontend_is_served():
    res = client.get("/")
    assert res.status_code == 200 and "Nearby Services" in res.text
