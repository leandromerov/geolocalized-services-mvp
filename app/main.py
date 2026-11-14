"""FastAPI application exposing the nearby-services search."""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .data import PROVIDERS
from .services import CATEGORIES, search_nearby

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(
    title="Geolocalized Services API",
    description="Find nearby home-service providers (plumbers, electricians, locksmiths...)",
    version="1.0.0",
)

allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_methods=["GET"], allow_headers=["*"])


class ProviderOut(BaseModel):
    id: int
    name: str
    category: str
    lat: float
    lng: float
    rating: float
    hourly_rate_eur: int
    available: bool
    distance_km: float


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/categories")
def categories() -> list[str]:
    return list(CATEGORIES)


@app.get("/api/providers/nearby", response_model=list[ProviderOut])
def providers_nearby(
    lat: float = Query(..., description="Latitude of the user"),
    lng: float = Query(..., description="Longitude of the user"),
    radius_km: float = Query(5.0, gt=0, le=100),
    category: str | None = Query(None),
    only_available: bool = Query(True),
    limit: int = Query(20, ge=1, le=100),
) -> list[dict]:
    try:
        results = search_nearby(PROVIDERS, lat, lng, radius_km, category, only_available, limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return [r.to_dict() for r in results]


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
