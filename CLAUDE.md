# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all spiders
python main.py

# Run specific spider(s)
python main.py pik a101 level

# List all available spiders
python main.py --list

# Run a single spider via Scrapy CLI
scrapy crawl pik
```

Dependency: `pip install scrapy`. No requirements.txt — Scrapy is the only dependency.

## Architecture

**Flat Scraper** collects apartment listings from Russian real estate developer websites and writes them to `flats.csv` (fields: `project_name`, `url`, `title`, `price`).

### URL configuration (`flat_scraper/config.py`)

All spider start URLs live here as `{project_name: url}` dicts (e.g. `PIK_START_URLS`, `A101_START_URLS`). To add new projects or update URLs, edit only this file — spider code doesn't change.

### Spiders (`flat_scraper/spiders/`)

Each spider:
- Reads its URL dict from `config.py` in `start_requests()`, yielding one Request per project with `meta['project_name']`
- Extracts **only the first apartment card** from each page (not all cards) using CSS/XPath selectors with fallbacks for HTML variation
- Converts price strings to integers via a local `clean_price()` method
- Yields plain dicts (not Scrapy Items)
- Declares its own `custom_settings` with `FEEDS` (output to `flats.csv`) and `USER_AGENT`

Active spiders: `pik`, `a101`, `level`, `rg`, `granelle`.  
Disabled (commented out): `donstroy` (broken), `lsr` (JS-rendered cards), `samolet` (401 errors).

### Entry point (`main.py`)

Runs spiders programmatically and sequentially. Supports `--list` and positional spider name args. Spiders write to the same `flats.csv`; each spider run rewrites the CSV headers.

### Settings (`flat_scraper/settings.py`)

Key overrides from Scrapy defaults: `ROBOTSTXT_OBEY = False`, `CONCURRENT_REQUESTS_PER_DOMAIN = 1`, `DOWNLOAD_DELAY = 1`. Individual spiders further override via `custom_settings`.

### Scaffolding files (`items.py`, `pipelines.py`, `middlewares.py`)

Standard Scrapy stubs — not actively used. Pipelines and middlewares are not configured in settings.
