from __future__ import annotations

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .api.geocoding import detect_location, search_city
from .api.weather import get_current_weather, get_forecast
from .display.formatters import display_current, display_forecast

app = typer.Typer(
    name="skycast",
    help="[bold cyan]skycast[/bold cyan] — beautiful weather for your terminal, powered by Open-Meteo.",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=True,
)

_err = Console(stderr=True)


def _spin(message: str, fn, *args):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=Console(stderr=True),
        transient=True,
    ) as progress:
        progress.add_task(description=message, total=None)
        return fn(*args)


def _version_callback(value: bool) -> None:
    if value:
        from importlib.metadata import version

        typer.echo(f"skycast {version('skycast')}")
        raise typer.Exit()


@app.callback()
def _root(
    version: bool = typer.Option(  # noqa: ARG001
        None,
        "--version",
        "-V",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    pass


@app.command()
def now() -> None:
    """Show current weather at [bold]your auto-detected location[/bold] (uses your IP)."""
    try:
        loc = _spin("Detecting your location…", detect_location)
        weather = _spin(f"Fetching weather for {loc.name}…", get_current_weather, loc)
    except Exception as exc:
        _err.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(1) from exc

    display_current(loc, weather)


@app.command()
def weather(
    city: str = typer.Argument(..., help="City name, e.g. [italic]London[/italic] or [italic]New York[/italic]"),
) -> None:
    """Show [bold]current conditions[/bold] for any city worldwide."""
    try:
        loc = _spin(f"Searching for '{city}'…", search_city, city)
        w = _spin(f"Fetching weather for {loc.name}…", get_current_weather, loc)
    except ValueError as exc:
        _err.print(f"[bold yellow]Not found:[/bold yellow] {exc}")
        raise typer.Exit(1) from exc
    except Exception as exc:
        _err.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(1) from exc

    display_current(loc, w)


@app.command()
def forecast(
    city: str = typer.Argument(..., help="City name, e.g. [italic]Tokyo[/italic] or [italic]Cape Town[/italic]"),
    days: int = typer.Option(7, "--days", "-d", min=1, max=16, help="Forecast length in days (1–16)."),
) -> None:
    """Show a [bold]multi-day forecast table[/bold] for any city worldwide."""
    try:
        loc = _spin(f"Searching for '{city}'…", search_city, city)
        forecasts = _spin(
            f"Fetching {days}-day forecast for {loc.name}…",
            get_forecast,
            loc,
            days,
        )
    except ValueError as exc:
        _err.print(f"[bold yellow]Not found:[/bold yellow] {exc}")
        raise typer.Exit(1) from exc
    except Exception as exc:
        _err.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(1) from exc

    display_forecast(loc, forecasts)


if __name__ == "__main__":
    app()
