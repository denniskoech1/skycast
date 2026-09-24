"""Unit tests for display helpers — no network required."""

from skycast.display.formatters import _condition, _uv_markup, _wind_arrow


class TestCondition:
    def test_clear_sky(self):
        desc, emoji = _condition(0)
        assert desc == "Clear Sky"
        assert emoji == "☀️"

    def test_thunderstorm(self):
        desc, emoji = _condition(95)
        assert "Thunderstorm" in desc

    def test_unknown_code_returns_fallback(self):
        desc, emoji = _condition(999)
        assert desc == "Unknown"
        assert emoji == "❓"

    def test_all_wmo_codes_have_entries(self):
        from skycast.display.formatters import WMO_CODES

        for code, (desc, emoji) in WMO_CODES.items():
            assert desc, f"Code {code} has empty description"
            assert emoji, f"Code {code} has empty emoji"


class TestWindArrow:
    def test_north(self):
        assert _wind_arrow(0) == "↑"

    def test_north_full_circle(self):
        assert _wind_arrow(360) == "↑"

    def test_east(self):
        assert _wind_arrow(90) == "→"

    def test_south(self):
        assert _wind_arrow(180) == "↓"

    def test_west(self):
        assert _wind_arrow(270) == "←"

    def test_northeast(self):
        assert _wind_arrow(45) == "↗"


class TestUVMarkup:
    def test_none_returns_na(self):
        assert _uv_markup(None) == "N/A"

    def test_low(self):
        assert "Low" in _uv_markup(1.0)

    def test_moderate(self):
        assert "Moderate" in _uv_markup(3.5)

    def test_high(self):
        assert "High" in _uv_markup(6.0)

    def test_very_high(self):
        assert "Very High" in _uv_markup(8.5)

    def test_extreme(self):
        assert "Extreme" in _uv_markup(11.0)

    def test_boundary_low_moderate(self):
        assert "Low" in _uv_markup(2.0)
        assert "Moderate" in _uv_markup(2.1)
