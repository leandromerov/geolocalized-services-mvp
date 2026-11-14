"""Framework-independent business logic for searching service providers.

Keeping this module free of FastAPI imports makes it easy to unit-test and to reuse
(e.g. from a CLI, a worker or a different web framework).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from .geo import bounding_box, haversine_km, validate_coordinates

CATEGORIES = ("plumber", "electrician", "locksmith", "cleaning", "handyman")


@dataclass(frozen=True)
class Provider:
    id: int
    name: str
    category: str
    lat: float
    lng: float
    rating: float
    hourly_rate_eur: int
    available: bool = True


@dataclass(frozen=True)
class SearchResult:
    provider: Provider
    distance_km: float

    def to_dict(self) -> dict:
        return {**asdict(self.provider), "distance_km": round(self.distance_km, 2)}


def search_nearby(
    providers: list[Provider],
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    category: str | None = None,
    only_available: bool = True,
    limit: int = 20,
) -> list[SearchResult]:
    """Return providers inside the radius, sorted by distance and then rating."""
    validate_coordinates(lat, lng)
    if not 0 < radius_km <= 100:
        raise ValueError("radius_km must be between 0 and 100")
    if category is not None and category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")

    min_lat, max_lat, min_lng, max_lng = bounding_box(lat, lng, radius_km)
    results: list[SearchResult] = []
    for p in providers:
        if category and p.category != category:
            continue
        if only_available and not p.available:
            continue
        # Cheap rectangular pre-filter before the exact distance calculation.
        if not (min_lat <= p.lat <= max_lat and min_lng <= p.lng <= max_lng):
            continue
        distance = haversine_km(lat, lng, p.lat, p.lng)
        if distance <= radius_km:
            results.append(SearchResult(p, distance))

    results.sort(key=lambda r: (r.distance_km, -r.provider.rating))
    return results[:limit]
