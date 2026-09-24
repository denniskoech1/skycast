from __future__ import annotations

from pydantic import BaseModel


class Location(BaseModel):
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: str = "auto"


class CurrentWeather(BaseModel):
    temperature: float
    feels_like: float
    humidity: int
    weather_code: int
    wind_speed: float
    wind_direction: int
    precipitation: float
    pressure: float
    visibility: float | None = None
    uv_index: float | None = None


class DailyForecast(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    weather_code: int
    precipitation: float
    wind_speed_max: float
    uv_index_max: float | None = None
    sunrise: str | None = None
    sunset: str | None = None
