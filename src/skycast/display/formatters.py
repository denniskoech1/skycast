from __future__ import annotations

from datetime import datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..models.weather import CurrentWeather, DailyForecast, Location

console = Console()

WMO_CODES: dict[int, tuple[str, str]] = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Icy Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌧️"),
    61: ("Slight Rain", "🌧️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Slight Snow", "🌨️"),
    73: ("Moderate Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    77: ("Snow Grains", "🌨️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Moderate Showers", "🌧️"),
    82: ("Heavy Showers", "⛈️"),
    85: ("Snow Showers", "🌨️"),
    86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm + Hail", "⛈️"),
    99: ("Severe Thunderstorm", "⛈️"),
}

_WIND_ARROWS = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]


def _condition(code: int) -> tuple[str, str]:
    return WMO_CODES.get(code, ("Unknown", "❓"))


def _wind_arrow(degrees: int) -> str:
    return _WIND_ARROWS[round(degrees / 45) % 8]


def _uv_markup(uv: float | None) -> str:
    if uv is None:
        return "N/A"
    if uv <= 2:
        return f"[green]{uv:.1f} Low[/green]"
    if uv <= 5:
        return f"[yellow]{uv:.1f} Moderate[/yellow]"
    if uv <= 7:
        return f"[orange1]{uv:.1f} High[/orange1]"
    if uv <= 10:
        return f"[red]{uv:.1f} Very High[/red]"
    return f"[bold red]{uv:.1f} Extreme[/bold red]"


def display_current(loc: Location, weather: CurrentWeather) -> None:
    description, emoji = _condition(weather.weather_code)
    arrow = _wind_arrow(weather.wind_direction)
    now = datetime.now().strftime("%A %d %B %Y, %H:%M")

    title = Text()
    title.append(f" {emoji}  ", style="bold")
    title.append(f"{loc.name}, {loc.country}", style="bold white")
    title.append(f"  ·  {now}", style="dim")

    vis_line = ""
    if weather.visibility is not None:
        vis_line = f"\n[bold]Visibility[/bold]     {weather.visibility / 1000:.1f} km"

    body = (
        f"[bold cyan]{weather.temperature:.1f}°C[/bold cyan]"
        f"  [dim]Feels like {weather.feels_like:.1f}°C[/dim]\n"
        f"[white]{description}[/white]\n\n"
        f"[bold]Humidity[/bold]       {weather.humidity}%\n"
        f"[bold]Wind[/bold]           {weather.wind_speed:.1f} km/h {arrow} {weather.wind_direction}°\n"
        f"[bold]Pressure[/bold]       {weather.pressure:.0f} hPa\n"
        f"[bold]Precipitation[/bold]  {weather.precipitation:.1f} mm"
        f"{vis_line}\n"
        f"[bold]UV Index[/bold]       {_uv_markup(weather.uv_index)}"
    )

    console.print()
    console.print(
        Panel(
            body,
            title=title,
            border_style="bright_blue",
            padding=(1, 2),
            expand=False,
        )
    )
    console.print()


def display_forecast(loc: Location, forecasts: list[DailyForecast]) -> None:
    table = Table(
        title=f"[bold]{len(forecasts)}-Day Forecast · {loc.name}, {loc.country}[/bold]",
        box=box.ROUNDED,
        border_style="bright_blue",
        header_style="bold bright_cyan",
        show_lines=True,
        padding=(0, 1),
    )

    table.add_column("Date", style="bold", min_width=12)
    table.add_column("", justify="center", min_width=3)
    table.add_column("Condition", min_width=18)
    table.add_column("High", justify="right", style="bold red", min_width=7)
    table.add_column("Low", justify="right", style="bold blue", min_width=7)
    table.add_column("Rain", justify="right", min_width=8)
    table.add_column("Wind max", justify="right", min_width=10)
    table.add_column("UV", justify="center", min_width=14)

    today = datetime.now().date()

    for f in forecasts:
        date_obj = datetime.strptime(f.date, "%Y-%m-%d").date()
        day_label = (
            "[bold green]Today[/bold green]"
            if date_obj == today
            else date_obj.strftime("%a %d %b")
        )

        description, emoji = _condition(f.weather_code)
        rain_style = "blue" if f.precipitation > 0 else "dim"
        rain = f"[{rain_style}]{f.precipitation:.1f} mm[/{rain_style}]"

        table.add_row(
            day_label,
            emoji,
            description,
            f"{f.temp_max:.1f}°C",
            f"{f.temp_min:.1f}°C",
            rain,
            f"{f.wind_speed_max:.1f} km/h",
            _uv_markup(f.uv_index_max),
        )

    console.print()
    console.print(table)
    console.print()
