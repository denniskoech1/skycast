"""Integration tests — these hit real APIs and require a network connection."""

import pytest

from skycast.api.geocoding import search_city
from skycast.api.weather import get_current_weather, get_forecast


def test_search_city_returns_correct_location():
    loc = search_city("London")
    assert loc.name == "London"
    assert "United Kingdom" in loc.country
    assert 50 < loc.latitude < 52
    assert -2 < loc.longitude < 1


def test_search_city_raises_on_gibberish():
    with pytest.raises(ValueError, match="not found"):
        search_city("xyznotacityxyz99999")


def test_get_current_weather_plausible_values():
    loc = search_city("Tokyo")
    w = get_current_weather(loc)
    assert -60 <= w.temperature <= 60, "Temperature out of realistic range"
    assert 0 <= w.humidity <= 100
    assert w.wind_speed >= 0
    assert 900 <= w.pressure <= 1100, "Pressure out of realistic range"


def test_get_forecast_returns_requested_days():
    loc = search_city("Paris")
    forecasts = get_forecast(loc, days=5)
    assert len(forecasts) == 5


def test_get_forecast_default_is_seven_days():
    loc = search_city("Sydney")
    forecasts = get_forecast(loc)
    assert len(forecasts) == 7


def test_forecast_temp_max_gte_min():
    loc = search_city("Nairobi")
    for day in get_forecast(loc):
        assert day.temp_max >= day.temp_min, (
            f"{day.date}: max {day.temp_max} < min {day.temp_min}"
        )


def test_forecast_dates_are_sequential():
    from datetime import date, timedelta

    loc = search_city("Berlin")
    forecasts = get_forecast(loc, days=7)
    for i in range(1, len(forecasts)):
        prev = date.fromisoformat(forecasts[i - 1].date)
        curr = date.fromisoformat(forecasts[i].date)
        assert curr == prev + timedelta(days=1)
