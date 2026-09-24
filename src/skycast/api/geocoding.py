from __future__ import annotations

import httpx

from ..models.weather import Location

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
IP_API_URL = "http://ip-api.com/json/"


def search_city(name: str) -> Location:
    with httpx.Client(timeout=10) as client:
        resp = client.get(GEOCODING_URL, params={"name": name, "count": 1, "format": "json"})
        resp.raise_for_status()
        data = resp.json()

    if not data.get("results"):
        raise ValueError(f"City '{name}' not found. Check the spelling and try again.")

    result = data["results"][0]
    return Location(
        name=result["name"],
        country=result.get("country", ""),
        latitude=result["latitude"],
        longitude=result["longitude"],
        timezone=result.get("timezone", "auto"),
    )


def detect_location() -> Location:
    with httpx.Client(timeout=10) as client:
        resp = client.get(IP_API_URL)
        resp.raise_for_status()
        data = resp.json()

    if data.get("status") != "success":
        raise RuntimeError(
            "Could not auto-detect your location. "
            "Try: skycast weather <city>"
        )

    return Location(
        name=data.get("city", "Unknown"),
        country=data.get("country", ""),
        latitude=data["lat"],
        longitude=data["lon"],
        timezone=data.get("timezone", "auto"),
    )
