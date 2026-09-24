from __future__ import annotations

import httpx

from ..models.weather import CurrentWeather, DailyForecast, Location

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

_CURRENT_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "weather_code",
    "wind_speed_10m",
    "wind_direction_10m",
    "precipitation",
    "surface_pressure",
    "visibility",
    "uv_index",
]

_DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "weather_code",
    "precipitation_sum",
    "wind_speed_10m_max",
    "uv_index_max",
    "sunrise",
    "sunset",
]


def get_current_weather(loc: Location) -> CurrentWeather:
    params = {
        "latitude": loc.latitude,
        "longitude": loc.longitude,
        "current": ",".join(_CURRENT_VARS),
        "wind_speed_unit": "kmh",
        "timezone": loc.timezone,
    }

    with httpx.Client(timeout=15) as client:
        resp = client.get(WEATHER_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    c = data["current"]
    return CurrentWeather(
        temperature=c["temperature_2m"],
        feels_like=c["apparent_temperature"],
        humidity=c["relative_humidity_2m"],
        weather_code=c["weather_code"],
        wind_speed=c["wind_speed_10m"],
        wind_direction=c["wind_direction_10m"],
        precipitation=c["precipitation"],
        pressure=c["surface_pressure"],
        visibility=c.get("visibility"),
        uv_index=c.get("uv_index"),
    )


def get_forecast(loc: Location, days: int = 7) -> list[DailyForecast]:
    params = {
        "latitude": loc.latitude,
        "longitude": loc.longitude,
        "daily": ",".join(_DAILY_VARS),
        "wind_speed_unit": "kmh",
        "timezone": loc.timezone,
        "forecast_days": days,
    }

    with httpx.Client(timeout=15) as client:
        resp = client.get(WEATHER_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    daily = data["daily"]
    n = len(daily["time"])

    def _get(key: str, i: int):
        values = daily.get(key, [])
        return values[i] if i < len(values) else None

    return [
        DailyForecast(
            date=daily["time"][i],
            temp_max=daily["temperature_2m_max"][i],
            temp_min=daily["temperature_2m_min"][i],
            weather_code=daily["weather_code"][i],
            precipitation=daily["precipitation_sum"][i] or 0.0,
            wind_speed_max=daily["wind_speed_10m_max"][i],
            uv_index_max=_get("uv_index_max", i),
            sunrise=_get("sunrise", i),
            sunset=_get("sunset", i),
        )
        for i in range(n)
    ]
