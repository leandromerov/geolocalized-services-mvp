"""Geospatial helpers: great-circle distance and bounding-box pre-filtering."""
from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Return the great-circle distance between two coordinates in kilometres."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def bounding_box(lat: float, lng: float, radius_km: float) -> tuple[float, float, float, float]:
    """Return (min_lat, max_lat, min_lng, max_lng) enclosing a circle.

    Used as a cheap pre-filter (e.g. an indexed SQL WHERE clause) before computing
    the exact haversine distance for the remaining candidates.
    """
    d_lat = math.degrees(radius_km / EARTH_RADIUS_KM)
    cos_lat = max(math.cos(math.radians(lat)), 1e-12)
    d_lng = math.degrees(radius_km / (EARTH_RADIUS_KM * cos_lat))
    return lat - d_lat, lat + d_lat, lng - d_lng, lng + d_lng


def validate_coordinates(lat: float, lng: float) -> None:
    if not -90 <= lat <= 90:
        raise ValueError("latitude must be between -90 and 90")
    if not -180 <= lng <= 180:
        raise ValueError("longitude must be between -180 and 180")
