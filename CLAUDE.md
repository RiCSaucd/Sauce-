# CLAUDE.md

This file provides guidance for AI assistants working with the **Vehicle Buyer Finder** codebase.

## Project Overview

A Python CLI application that identifies potential vehicle buyers by aggregating data from Yellow Pages (public business listings) and authorized DMV API sources. The tool processes, categorizes, scores, and exports prospect data in multiple formats.

**Important**: This application works with personal and DMV data. Legal compliance (DPPA, TCPA, CAN-SPAM) is a first-class concern throughout the codebase. Never add features that bypass legal safeguards.

---

## Repository Structure

```
Sauce-/
├── main.py                  # Application entry point and CLI orchestration
├── yellowpages_scraper.py   # Web scraper for Yellow Pages public listings
├── dmv_integration.py       # DMV API wrapper + MockDMVIntegration for testing
├── prospect_finder.py       # Core analytics: categorize, score, filter, export
├── config.py                # Centralized config via environment variables
├── requirements.txt         # Pinned Python dependencies
├── .env.example             # Environment variable template
├── .gitignore
├── README.md
├── LEGAL_NOTICE.md          # Compliance guide (DPPA, TCPA, CAN-SPAM)
└── .github/
    ├── workflows/           # GitHub Actions CI/CD workflows
    └── steps/               # GitHub Skills course step content
```

Output files are written to `./output/` (git-ignored) with timestamped filenames.

---

## Technology Stack

- **Language**: Python 3.8+
- **Web scraping**: `requests` 2.31.0, `beautifulsoup4` 4.12.2, `lxml` 4.9.4
- **Browser automation**: `selenium` 4.16.0, `webdriver-manager` 4.0.1
- **Data processing**: `pandas` 2.1.4
- **Config management**: `python-dotenv` 1.0.0

---

## Setup and Installation

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd Sauce-

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings (see Configuration section)
```

---

## Running the Application

```bash
# Basic run (uses defaults from .env)
python main.py

# Test with mock DMV data (no credentials required)
python main.py --mock-dmv

# Yellow Pages only (skip DMV)
python main.py --yellowpages-only

# Custom locations and categories
python main.py --locations "Jacksonville,FL" "Saint Augustine,FL" \
               --categories "auto dealers" "car buyers"

# Specify output format
python main.py --output-format excel   # csv | excel | json

# Skip interactive legal notice (automation/CI)
python main.py --no-legal-notice --mock-dmv
```

On first run (without `--no-legal-notice`), the user must type `yes` to acknowledge legal compliance before execution continues.

---

## Application Data Flow (4 Phases)

```
Phase 1: YellowPagesScraper.search_multiple_locations()
         → scrapes public business listings
         ↓
Phase 2: DMVIntegration.find_recent_buyers() (or MockDMVIntegration)
         → queries vehicle registrations for recent buyers
         ↓
Phase 3: ProspectFinder
         → categorize_prospects()  (Auto Dealer / Vehicle Buyer / Body Shop)
         → score_prospects()       (0–40 score based on data completeness)
         → generate_report()       (summary statistics)
         ↓
Phase 4: ProspectFinder.export_prospects()
         → writes CSV/Excel/JSON to ./output/
```

---

## Configuration

All configuration flows through `config.py` which reads from environment variables (loaded from `.env`):

| Variable | Default | Description |
|---|---|---|
| `YELLOWPAGES_BASE_URL` | `https://www.yellowpages.com` | Base URL for Yellow Pages scraping |
| `DMV_API_KEY` | _(none)_ | DMV API key — requires official authorization |
| `DMV_API_ENDPOINT` | _(none)_ | DMV API endpoint URL |
| `DMV_AUTHORIZED_USER_ID` | _(none)_ | Authorized user ID for DMV access |
| `TARGET_LOCATIONS` | `Jacksonville,FL;Saint Augustine,FL` | Semicolon-separated list of locations |
| `SEARCH_CATEGORIES` | `auto dealers,car buyers` | Comma-separated search categories |
| `OUTPUT_FORMAT` | `csv` | Default export format (`csv`, `excel`, `json`) |
| `OUTPUT_DIRECTORY` | `./output` | Directory for exported files |

`Config.validate_dmv_credentials()` returns `False` if `DMV_API_KEY` or `DMV_API_ENDPOINT` is missing — the app will exit unless `--mock-dmv` or `--yellowpages-only` is used.

---

## Code Conventions

### Naming
- **Classes**: PascalCase — `YellowPagesScraper`, `DMVIntegration`, `ProspectFinder`
- **Methods/functions**: snake_case — `search_location`, `score_prospects`
- **Private methods**: prefixed with `_` — `_parse_listing()`
- **Config constants**: UPPER_SNAKE_CASE

### Documentation
- All public methods have docstrings with `Args:` and `Returns:` sections
- Type hints on all function signatures
- Inline comments for non-obvious logic

### Logging
- Use Python's `logging` module throughout — never `print()` for operational output
- Logger per module: `logger = logging.getLogger(__name__)`
- Logging level: `INFO` by default; `WARNING` for mock/degraded modes; `ERROR` for failures

### Data
- Primary in-memory data structure: `pandas.DataFrame`
- All DataFrames share a common schema: `name`, `phone`, `address`, `website`, `source`
- Deduplication by `phone` (Yellow Pages) or `name`+`phone` combination

---

## Module Responsibilities

### `main.py`
Argument parsing, legal notice display, phase orchestration, top-level exception handling. Does not contain business logic — delegates to the other modules.

### `yellowpages_scraper.py` — `YellowPagesScraper`
- Scrapes Yellow Pages public listings using `requests` + `BeautifulSoup`
- Enforces 2-second delays between requests (rate limiting)
- Deduplicates by phone number before returning
- Returns a `pd.DataFrame` with columns: `name`, `phone`, `address`, `website`, `source`

### `dmv_integration.py`
Two classes with identical interfaces:
- **`DMVIntegration`**: Real API — requires `DMV_API_KEY`, `DMV_API_ENDPOINT`, `DMV_AUTHORIZED_USER_ID`. Uses Bearer token auth.
- **`MockDMVIntegration`**: Returns synthetic test data. Use this in development and CI.

Both expose `find_recent_buyers(location, days=90) -> pd.DataFrame`.

### `prospect_finder.py` — `ProspectFinder`
- `add_yellowpages_data(df)` / `add_dmv_data(df)` — append data
- `categorize_prospects()` — assigns `prospect_type` by keyword matching on `name`
- `score_prospects()` — adds `score` column (max 40 pts: phone +10, address +5, website +5, DMV source +20)
- `export_prospects(filename, format)` — writes to `output_directory`
- `generate_report()` — returns dict with totals, breakdowns by source/type

### `config.py` — `Config`
Single class with class-level attributes. Import and use as `Config.SOME_SETTING`. Call `Config.validate_dmv_credentials()` before constructing `DMVIntegration`.

---

## Testing

There is no formal test framework. Use the mock integration for development and verification:

```bash
# Full pipeline test with mock data
python main.py --mock-dmv --no-legal-notice --output-format json

# Yellow Pages only (no credentials required)
python main.py --yellowpages-only --no-legal-notice
```

`MockDMVIntegration` (in `dmv_integration.py`) generates deterministic synthetic records — suitable for CI runs. When adding new features, extend or mirror this class to cover new data paths.

---

## Legal and Compliance Constraints

This application is designed for **authorized use only**. When modifying the codebase:

- **Do not** remove the legal notice prompt (`print_legal_notice()`) or make it easier to bypass
- **Do not** add features that scrape or access personal data beyond what is explicitly authorized
- **Do not** store DMV credentials anywhere other than `.env` (which is git-ignored)
- **Do** maintain rate limiting in the scraper (minimum 2-second delay between requests)
- **Do** keep `LEGAL_NOTICE.md` accurate if data sources or usage patterns change

Relevant regulations: DPPA (Driver's Privacy Protection Act), TCPA, CAN-SPAM Act. See `LEGAL_NOTICE.md` for full compliance guidance.

---

## Git and CI/CD

- **Branch strategy**: Feature branches off `master`; PRs reviewed before merge
- **CI**: GitHub Actions workflows in `.github/workflows/`
- **Dependency updates**: Dependabot configured for monthly GitHub Actions updates
- **Secrets**: Never commit `.env` or real API keys — only `.env.example` with placeholder values
- **Output files**: `./output/` is git-ignored; never commit generated CSV/Excel/JSON files

### Common Git Operations

```bash
# Create and push a feature branch
git checkout -b feature/my-change
git add <files>
git commit -m "feat: describe the change"
git push -u origin feature/my-change
```

---

## Key Files Quick Reference

| File | Lines | Purpose |
|---|---|---|
| `main.py` | 245 | Entry point, CLI args, 4-phase orchestration |
| `yellowpages_scraper.py` | 134 | Public Yellow Pages data collection |
| `dmv_integration.py` | 174 | DMV API + mock test integration |
| `prospect_finder.py` | 201 | Categorize, score, filter, export prospects |
| `config.py` | 33 | Environment-based configuration |
