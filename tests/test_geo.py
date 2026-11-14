import math

import pytest

from app.geo import bounding_box, haversine_km, validate_coordinates


def test_distance_to_same_point_is_zero():
    assert haversine_km(48.57, 13.46, 48.57, 13.46) == 0


def test_known_distance_passau_to_munich():
    # Passau Hbf -> München Hbf is roughly 147 km in a straight line.
    distance = haversine_km(48.5733, 13.4517, 48.1402, 11.5600)
    assert 140 < distance < 155


def test_bounding_box_contains_points_on_the_circle():
    lat, lng, radius = 48.57, 13.46, 5
    min_lat, max_lat, min_lng, max_lng = bounding_box(lat, lng, radius)
    north = lat + math.degrees(radius / 6371.0088)
    assert min_lat < lat < max_lat and min_lng < lng < max_lng
    assert math.isclose(max_lat, north, rel_tol=1e-9)


@pytest.mark.parametrize("lat,lng", [(91, 0), (-91, 0), (0, 181), (0, -181)])
def test_invalid_coordinates_raise(lat, lng):
    with pytest.raises(ValueError):
        validate_coordinates(lat, lng)
