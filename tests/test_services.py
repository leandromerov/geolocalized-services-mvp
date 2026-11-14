import pytest

from app.data import PROVIDERS
from app.services import search_nearby

PASSAU_CENTER = (48.5745, 13.4600)


def test_results_are_sorted_by_distance_and_within_radius():
    results = search_nearby(PROVIDERS, *PASSAU_CENTER, radius_km=3)
    distances = [r.distance_km for r in results]
    assert distances == sorted(distances)
    assert all(d <= 3 for d in distances)
    assert results, "expected providers in central Passau"


def test_far_away_providers_are_excluded():
    names = {r.provider.name for r in search_nearby(PROVIDERS, *PASSAU_CENTER, radius_km=10)}
    assert "Vilshofen Plumbing Pro" not in names  # ~20 km away


def test_category_filter():
    results = search_nearby(PROVIDERS, *PASSAU_CENTER, radius_km=10, category="locksmith")
    assert results and all(r.provider.category == "locksmith" for r in results)


def test_unavailable_providers_hidden_by_default():
    hidden = search_nearby(PROVIDERS, *PASSAU_CENTER, radius_km=10, category="electrician")
    shown = search_nearby(PROVIDERS, *PASSAU_CENTER, radius_km=10, category="electrician", only_available=False)
    assert len(shown) == len(hidden) + 1


def test_limit_and_serialisation():
    results = search_nearby(PROVIDERS, *PASSAU_CENTER, radius_km=10, limit=2)
    assert len(results) == 2
    payload = results[0].to_dict()
    assert {"name", "distance_km", "rating"} <= payload.keys()


@pytest.mark.parametrize("kwargs", [{"radius_km": 0}, {"radius_km": 500}, {"category": "astronaut"}])
def test_invalid_input_raises(kwargs):
    with pytest.raises(ValueError):
        search_nearby(PROVIDERS, *PASSAU_CENTER, **kwargs)
