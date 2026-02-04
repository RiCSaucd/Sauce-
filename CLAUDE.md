# CLAUDE.md - AI Assistant Guide

This document provides essential context for AI assistants working with the Vehicle Buyer Finder codebase.

## Project Overview

**Vehicle Buyer Finder** is a Python application for identifying potential vehicle buyers by aggregating data from Yellow Pages (public) and authorized DMV sources in the Jacksonville and Saint Augustine, Florida areas.

- **Version**: 1.0.0
- **License**: MIT
- **Python Version**: 3.8+
- **Last Updated**: January 2026

## Repository Structure

```
Sauce-/
├── main.py                   # Application entry point and CLI
├── config.py                 # Environment-based configuration management
├── yellowpages_scraper.py    # Yellow Pages web scraping module
├── dmv_integration.py        # DMV API integration (real + mock)
├── prospect_finder.py        # Data analysis, scoring, and export
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # User documentation
├── LEGAL_NOTICE.md           # Legal compliance guide
├── LICENSE                   # MIT license
├── output/                   # Generated output files (auto-created)
└── .github/
    ├── workflows/            # GitHub Actions workflows
    └── steps/                # Learning path documentation
```

## Core Modules

### main.py (Entry Point)
- Parses command-line arguments
- Orchestrates 4-phase workflow: Yellow Pages → DMV → Analysis → Export
- Handles legal notice acknowledgment
- Displays results and exports data

### config.py (Configuration)
- Loads environment variables via `python-dotenv`
- Provides `Config` class with all settings
- `validate_dmv_credentials()` checks for DMV API authorization

### yellowpages_scraper.py (Web Scraping)
- `YellowPagesScraper` class for collecting business listings
- `search_location()` - Single search
- `search_multiple_locations()` - Batch search across categories/locations
- Rate-limited (2-second delays), deduplicates by phone number

### dmv_integration.py (DMV Data)
- `DMVIntegration` - Real DMV API client (requires authorization)
- `MockDMVIntegration` - Testing substitute with simulated data
- `find_recent_buyers()` - Query vehicle purchasers by location/date range

### prospect_finder.py (Analysis)
- `ProspectFinder` class for data processing
- `categorize_prospects()` - Type classification (Auto Dealer, Vehicle Buyer, Body Shop)
- `score_prospects()` - Relevance scoring (0-100 scale)
- `export_prospects()` - Output in CSV, Excel, or JSON
- `generate_report()` - Statistics and summary

## Quick Commands

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
```

### Running the Application
```bash
# Yellow Pages only (no DMV)
python main.py --yellowpages-only

# With mock DMV data (testing)
python main.py --mock-dmv

# Full search with locations
python main.py --locations "Jacksonville,FL" "Saint Augustine,FL"

# Custom categories
python main.py --categories "auto dealers" "car buyers" "used cars"

# Skip legal notice (testing only)
python main.py --mock-dmv --no-legal-notice
```

### Output Formats
```bash
python main.py --output-format csv    # Default
python main.py --output-format excel  # Excel (.xlsx)
python main.py --output-format json   # JSON
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.31.0 | HTTP client |
| beautifulsoup4 | 4.12.2 | HTML parsing |
| pandas | 2.1.4 | Data manipulation |
| python-dotenv | 1.0.0 | Environment variables |
| selenium | 4.16.0 | Browser automation |
| webdriver-manager | 4.0.1 | WebDriver management |
| lxml | 4.9.4 | XML/HTML processing |

## Code Conventions

### Logging
- Use `logging` module consistently
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- INFO for major operations, WARNING for notices, ERROR for problems

### Data Handling
- Use pandas DataFrames for tabular data
- Deduplicate by phone number
- Consistent schema across modules: `name`, `phone`, `address`, `website`, `category`, `source`

### Web Scraping
- Include User-Agent headers in requests
- Rate limit with 2-second delays between requests
- Handle exceptions gracefully

### Configuration
- All settings via environment variables
- Use `.env` file for local configuration
- Never commit `.env` files (see `.gitignore`)

## Important Legal Considerations

This application handles data subject to strict legal regulations. AI assistants should be aware:

1. **DPPA (Driver's Privacy Protection Act)** - DMV records are federally protected
2. **TCPA (Telephone Consumer Protection Act)** - Telemarketing restrictions
3. **CAN-SPAM Act** - Email marketing compliance

**Key points:**
- DMV data requires explicit authorization
- Always use `--mock-dmv` for testing
- Do not suggest bypassing legal notices
- See `LEGAL_NOTICE.md` for full details

## Application Workflow

```
Phase 1: Yellow Pages Collection
  └─> Scrape public business listings
  └─> Extract: name, phone, address, website, category
  └─> Deduplicate by phone number

Phase 2: DMV Data Integration (optional)
  └─> Query authorized DMV API (or mock)
  └─> Retrieve recent vehicle registrations
  └─> Filter by location and date range

Phase 3: Prospect Analysis
  └─> Combine all data sources
  └─> Categorize by type (keywords)
  └─> Score by data completeness (0-100)
  └─> Remove duplicates

Phase 4: Export
  └─> Generate statistics report
  └─> Export to CSV/Excel/JSON
  └─> Display top 10 prospects
```

## Scoring Algorithm

Prospects are scored 0-100 based on:
- Phone present: +10 points
- Website present: +5 points
- Address present: +5 points
- DMV source: +20 points (verified buyers weighted higher)

## Prospect Categories

Determined by keyword matching in business name:
- **Auto Dealer**: "auto", "car", "dealer", "motors", "automotive"
- **Vehicle Buyer**: "buyer", "cash for cars", "we buy", "wholesale"
- **Body Shop**: "body shop", "collision", "repair"

## Environment Variables

```bash
# Yellow Pages
YELLOWPAGES_BASE_URL=https://www.yellowpages.com

# DMV (requires authorization)
DMV_API_KEY=your_key
DMV_API_ENDPOINT=https://api.dmv.state.fl.us/v1
DMV_AUTHORIZED_USER_ID=your_id

# Search
TARGET_LOCATIONS=Jacksonville,FL;Saint Augustine,FL
SEARCH_CATEGORIES=auto dealers,car buyers

# Output
OUTPUT_FORMAT=csv
OUTPUT_DIRECTORY=./output
```

## Testing Modes

1. **`--mock-dmv`** - Uses `MockDMVIntegration` with simulated data
2. **`--yellowpages-only`** - Skips DMV phase entirely
3. **`--no-legal-notice`** - Bypasses acknowledgment prompt (testing only)

## Common Development Tasks

### Adding a New Data Source
1. Create new module (e.g., `new_source.py`)
2. Implement data collection class with consistent schema
3. Add `add_new_source_data()` method to `ProspectFinder`
4. Integrate into `main.py` workflow

### Modifying Prospect Scoring
Edit `score_prospects()` in `prospect_finder.py:126-150`

### Adding New Prospect Categories
Edit `categorize_prospects()` in `prospect_finder.py:98-124`

### Changing Output Format
Modify `export_prospects()` in `prospect_finder.py:152-180`

## File Locations Reference

| Concern | File | Line Range |
|---------|------|------------|
| CLI argument parsing | main.py | 66-108 |
| Legal notice display | main.py | 41-61 |
| Config validation | config.py | 28-33 |
| Web scraping logic | yellowpages_scraper.py | 25-80 |
| DMV API integration | dmv_integration.py | 15-100 |
| Mock DMV data | dmv_integration.py | 102-174 |
| Prospect scoring | prospect_finder.py | 126-150 |
| Data export | prospect_finder.py | 152-180 |

## Git Workflow

- Main branch contains stable code
- Feature branches for development
- PR-based workflow (see `.github/workflows/`)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "DMV credentials not configured" | Use `--mock-dmv` or configure `.env` |
| "Error fetching Yellow Pages data" | Check internet; Yellow Pages may rate limit |
| Empty results | Try different categories/locations |
| Import errors | Run `pip install -r requirements.txt` |

## Notes for AI Assistants

1. **Always use mock mode for testing** - Never suggest using real DMV credentials without proper authorization
2. **Respect legal boundaries** - Do not help circumvent compliance checks
3. **Keep scraping respectful** - Maintain rate limiting in any modifications
4. **Test with `--yellowpages-only`** - Safest mode for development
5. **Check `.gitignore`** - Never commit `.env`, `output/`, or credential files
6. **Data privacy** - Do not expose or log personal information unnecessarily
