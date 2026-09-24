<div align="center">

# ⛅ skycast

**Beautiful weather for your terminal — current conditions and forecasts for any city, worldwide.**

[![CI](https://github.com/denniskoech1/skycast/actions/workflows/ci.yml/badge.svg)](https://github.com/denniskoech1/skycast/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

---

## What it does

`skycast` is a command-line tool that fetches real-time weather data and renders it beautifully in your terminal. Three commands cover every use-case:

| Command | Description |
|---|---|
| `skycast now` | Auto-detects your location and shows current conditions |
| `skycast weather <city>` | Current weather for any city on Earth |
| `skycast forecast <city>` | Up to 16-day forecast as a rich colour table |

Zero sign-up. Zero API keys. Just install and run.

---

## Demo

### `skycast weather "Nairobi"`

```
╭─ ⛅  Nairobi, Kenya  ·  Thursday 24 September 2026, 14:32 ───╮
│                                                                │
│  22.4°C  Feels like 21.8°C                                    │
│  Partly Cloudy                                                 │
│                                                                │
│  Humidity       68%                                           │
│  Wind           14.2 km/h ↗ 52°                               │
│  Pressure       1014 hPa                                      │
│  Precipitation  0.0 mm                                        │
│  Visibility     10.0 km                                       │
│  UV Index       6.2 High                                      │
╰────────────────────────────────────────────────────────────────╯
```

### `skycast forecast Tokyo --days 5`

```
╭──────────────────────────────────────────────────────────────────────────────────╮
│                     5-Day Forecast · Tokyo, Japan                                │
├──────────────┬────┬────────────────────┬─────────┬──────────┬─────────┬─────────┤
│ Date         │    │ Condition          │  High   │   Low    │  Rain   │ Wind max │
├──────────────┼────┼────────────────────┼─────────┼──────────┼─────────┼─────────┤
│ Today        │ ⛅  │ Partly Cloudy      │ 28.3°C  │  21.1°C  │ 0.0 mm  │ 22 km/h │
│ Fri 25 Sep   │ 🌧️  │ Moderate Rain      │ 24.6°C  │  19.8°C  │ 11.4 mm │ 35 km/h │
│ Sat 26 Sep   │ ☁️  │ Overcast           │ 22.1°C  │  18.3°C  │ 0.2 mm  │ 18 km/h │
│ Sun 27 Sep   │ ☀️  │ Clear Sky          │ 26.8°C  │  17.9°C  │ 0.0 mm  │ 14 km/h │
│ Mon 28 Sep   │ 🌤️  │ Mainly Clear       │ 27.5°C  │  18.4°C  │ 0.0 mm  │ 16 km/h │
╰──────────────┴────┴────────────────────┴─────────┴──────────┴─────────┴─────────╯
```

---

## Installation

### Install directly from GitHub (recommended)

```bash
pip install git+https://github.com/denniskoech1/skycast.git
```

That's it. The `skycast` command is now available globally.

### Install from source (for development)

```bash
git clone https://github.com/denniskoech1/skycast.git
cd skycast
pip install -e ".[dev]"
```

---

## Usage

```
skycast --help
```

```
Usage: skycast [OPTIONS] COMMAND [ARGS]...

  skycast — beautiful weather for your terminal, powered by Open-Meteo.

Options:
  -V, --version  Show version and exit.
  --help         Show this message and exit.

Commands:
  now       Show current weather at your auto-detected location.
  weather   Show current conditions for any city worldwide.
  forecast  Show a multi-day forecast table for any city worldwide.
```

### Current weather — auto-detected location

```bash
skycast now
```

Detects your approximate location from your IP address (no GPS, no sign-in) and displays current conditions.

### Current weather — specific city

```bash
skycast weather London
skycast weather "New York"
skycast weather "Cape Town"
```

### Forecast — any city, up to 16 days

```bash
skycast forecast Tokyo           # defaults to 7 days
skycast forecast Paris --days 10
skycast forecast Sydney -d 3
```

---

## How it works

`skycast` is built on two completely free, open APIs — no account or API key needed:

| Service | Used for |
|---|---|
| [Open-Meteo](https://open-meteo.com/) | Weather conditions + forecast data |
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | City name → coordinates |
| [ip-api.com](https://ip-api.com/) | IP-based location detection (`skycast now`) |

Data is fetched fresh on every run — no stale cache.

---

## Tech stack

| Layer | Library | Why |
|---|---|---|
| CLI | [`typer`](https://typer.tiangolo.com/) | Auto-generates `--help`, shell completions, type-safe commands |
| Output | [`rich`](https://github.com/Textualize/rich) | Coloured panels, tables, progress spinners |
| HTTP | [`httpx`](https://www.python-httpx.org/) | Modern, sync/async capable HTTP client |
| Data models | [`pydantic`](https://docs.pydantic.dev/) | Validates API responses, clean typed models |
| Tests | [`pytest`](https://pytest.org/) | Real integration tests against live APIs |
| Linting | [`ruff`](https://github.com/astral-sh/ruff) | Fast, comprehensive Python linter |
| Packaging | [`hatchling`](https://hatch.pypa.io/) | Modern `pyproject.toml`-native build backend |

---

## Project structure

```
skycast/
├── src/
│   └── skycast/
│       ├── main.py              # CLI entry point (typer app)
│       ├── api/
│       │   ├── geocoding.py     # City search + IP location detection
│       │   └── weather.py       # Open-Meteo weather client
│       ├── models/
│       │   └── weather.py       # Pydantic data models
│       └── display/
│           └── formatters.py    # Rich rendering (panels, tables)
├── tests/
│   ├── test_api.py              # Integration tests (live API)
│   └── test_display.py          # Unit tests (no network)
├── .github/workflows/ci.yml     # CI: test × Python 3.10/3.11/3.12
└── pyproject.toml
```

---

## Development

```bash
# Clone and install in editable mode with dev dependencies
git clone https://github.com/denniskoech1/skycast.git
cd skycast
pip install -e ".[dev]"

# Run the test suite (requires network — tests hit real APIs)
pytest -v

# Lint
ruff check src tests

# Try it immediately
skycast weather Nairobi
```

### Running tests

The test suite includes:

- **Integration tests** (`test_api.py`) — make real HTTP requests to Open-Meteo and ip-api.com. Network access required.
- **Unit tests** (`test_display.py`) — test display helpers in isolation. No network needed.

---

## CI / CD

Every push to `main` runs the full test suite against **Python 3.10, 3.11, and 3.12** on Ubuntu via GitHub Actions. A passing build also produces a distributable wheel as a downloadable artifact.

[![CI](https://github.com/denniskoech1/skycast/actions/workflows/ci.yml/badge.svg)](https://github.com/denniskoech1/skycast/actions/workflows/ci.yml)

---

## Requirements

- Python 3.10 or newer
- Network access (fetches live data on every run)
- A terminal that supports Unicode and colour (Windows Terminal, iTerm2, most Linux terminals)

---

## License

MIT © [Dennis Koech](https://github.com/denniskoech1)

---

<div align="center">
  <sub>Powered by <a href="https://open-meteo.com/">Open-Meteo</a> — free, open-source weather API.</sub>
</div>
