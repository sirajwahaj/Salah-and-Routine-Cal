# salah-calendar — Generator

Python script that generates the full-year 2026 Islamic daily routine calendar (`.ics` file) for Malmö, Sweden.

## How it works

1. Fetches daily prayer times from the [AlAdhan API](https://aladhan.com/prayer-times-api) for each month
2. Builds RFC 5545 compliant `VEVENT` blocks with alarms, categories, and descriptions
3. Adds Islamic holidays as all-day events
4. Outputs `malmo-sweden.ics` with proper CRLF line endings and line folding

## Run locally

```bash
# With uv (recommended)
cd salah-calendar
uv run python generate.py

# With pip
pip install requests
python generate.py
```

## Configuration

Edit the top of `generate.py` to change:

| Variable | Default | Description |
|----------|---------|-------------|
| `LAT` | 55.6050 | Latitude |
| `LON` | 13.0038 | Longitude |
| `YEAR` | 2026 | Calendar year |
| `METHOD` | 3 | Calculation method (Muslim World League) |
| `OUTPUT_FILE` | `malmo-sweden.ics` | Output filename |

## API

Prayer times are sourced from [api.aladhan.com](https://api.aladhan.com). Method 3 = Muslim World League, which is the standard used by European mosques.
