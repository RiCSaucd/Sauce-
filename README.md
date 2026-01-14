# Vehicle Buyer Finder

A Python application for identifying potential vehicle buyers by aggregating data from Yellow Pages and authorized DMV sources in the Jacksonville and Saint Augustine, Florida areas.

## ⚠️ Important Legal Notice

This application is designed to work with **AUTHORIZED DATA SOURCES ONLY**.

### Legal Requirements

**Before using this application, you MUST:**

1. **DMV Data Access**: Obtain proper authorization for DMV data access
   - DMV records are protected by the **Driver's Privacy Protection Act (DPPA)** (18 USC § 2721)
   - Unauthorized access is a federal crime with civil and criminal penalties
   - Contact Florida DMV for API access: https://www.flhsmv.gov/

2. **Marketing Compliance**: Ensure compliance with:
   - **Telephone Consumer Protection Act (TCPA)** - obtain consent before calling
   - **CAN-SPAM Act** - follow email marketing rules
   - **Do Not Call Registry** - check numbers before calling

3. **Permissible Uses** under DPPA include:
   - Motor vehicle or driver safety recalls
   - Market research activities (with proper authorization)
   - Licensed private investigators
   - Authorized government agencies

### Liability Disclaimer

Users of this software are solely responsible for ensuring legal compliance with all applicable laws and regulations. The developers assume no liability for misuse of this application.

## Features

- **Yellow Pages Scraper**: Collect publicly available business listings from Yellow Pages
- **DMV Integration**: Framework for working with authorized DMV data sources
- **Prospect Analysis**: Score and categorize potential buyers
- **Data Export**: Export results in CSV, Excel, or JSON format
- **Mock Mode**: Test the application without accessing real DMV data

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Sauce-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Configure DMV credentials (if authorized):
```bash
# Edit .env and add:
DMV_API_KEY=your_authorized_api_key
DMV_API_ENDPOINT=https://api.dmv.state.fl.us/v1
DMV_AUTHORIZED_USER_ID=your_user_id
```

## Usage

### Basic Usage (Yellow Pages Only)

```bash
python main.py --yellowpages-only
```

### With Mock DMV Data (Testing)

```bash
python main.py --mock-dmv
```

### Full Search with Multiple Locations

```bash
python main.py --locations "Jacksonville,FL" "Saint Augustine,FL"
```

### Custom Categories

```bash
python main.py --categories "auto dealers" "car buyers" "used cars"
```

### Export Options

```bash
# Export as CSV (default)
python main.py --output-format csv

# Export as Excel
python main.py --output-format excel

# Export as JSON
python main.py --output-format json
```

### Command Line Options

```
Options:
  --locations LOC [LOC ...]     Target locations (e.g., "Jacksonville,FL")
  --categories CAT [CAT ...]    Business categories to search
  --mock-dmv                    Use mock DMV data for testing
  --yellowpages-only            Only search Yellow Pages (skip DMV)
  --output-format {csv,excel,json}  Output format
  --no-legal-notice             Skip legal notice (not recommended)
  --help                        Show help message
```

## Project Structure

```
Sauce-/
├── main.py                   # Main application entry point
├── config.py                 # Configuration management
├── yellowpages_scraper.py    # Yellow Pages data collection
├── dmv_integration.py        # DMV API integration (requires authorization)
├── prospect_finder.py        # Prospect analysis and scoring
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── LEGAL_NOTICE.md          # Detailed legal information
└── output/                  # Output directory (created automatically)
```

## How It Works

### Phase 1: Yellow Pages Collection
- Searches Yellow Pages for auto-related businesses
- Collects business names, phone numbers, addresses, websites
- Covers multiple categories and locations

### Phase 2: DMV Data (Authorized Access Only)
- Connects to authorized DMV API
- Retrieves recent vehicle registration data
- Identifies recent vehicle purchasers

### Phase 3: Prospect Analysis
- Combines data from all sources
- Categorizes prospects (dealers, buyers, body shops, etc.)
- Scores prospects based on data completeness and relevance
- Removes duplicates

### Phase 4: Export
- Generates comprehensive report
- Exports data in your chosen format
- Displays top prospects

## Data Fields

The application collects and outputs the following fields:

- **name**: Business or individual name
- **phone**: Contact phone number
- **address**: Physical address
- **website**: Website URL (if available)
- **category**: Business category
- **prospect_type**: Categorized type (Auto Dealer, Vehicle Buyer, etc.)
- **score**: Relevance score (0-100)
- **source**: Data source (YellowPages, DMV, etc.)

## Configuration

### Environment Variables

Edit `.env` to configure:

```bash
# Yellow Pages
YELLOWPAGES_BASE_URL=https://www.yellowpages.com

# DMV (requires authorization)
DMV_API_KEY=your_key
DMV_API_ENDPOINT=your_endpoint
DMV_AUTHORIZED_USER_ID=your_id

# Search parameters
TARGET_LOCATIONS=Jacksonville,FL;Saint Augustine,FL
SEARCH_CATEGORIES=auto dealers,car buyers,vehicle buyers

# Output
OUTPUT_FORMAT=csv
OUTPUT_DIRECTORY=./output
```

## Testing

### Test with Mock Data

```bash
# Test Yellow Pages only
python main.py --yellowpages-only --no-legal-notice

# Test with mock DMV data
python main.py --mock-dmv --no-legal-notice
```

## Troubleshooting

### "DMV credentials not configured"
- You need authorized DMV API access
- Use `--mock-dmv` for testing
- Or use `--yellowpages-only` to skip DMV data

### "Error fetching Yellow Pages data"
- Check your internet connection
- Yellow Pages may have rate limiting
- The HTML structure may have changed (update selectors)

### Empty results
- Try different search categories
- Verify location names are correct
- Check for typos in configuration

## Compliance Checklist

Before using this application for business purposes:

- [ ] Obtained authorized DMV API access
- [ ] Signed Data Use Agreement with DMV
- [ ] Verified permissible use under DPPA
- [ ] Implemented Do Not Call registry checking
- [ ] Prepared TCPA-compliant consent process
- [ ] Reviewed CAN-SPAM requirements
- [ ] Consulted with legal counsel
- [ ] Documented authorization and business purpose

## Contributing

Contributions are welcome! Please ensure any changes maintain legal compliance and include appropriate warnings.

## License

MIT License - See LICENSE file for details

**Note**: While the software is open source, users are responsible for obtaining proper authorization for data access and ensuring legal compliance.

## Support

For issues or questions:
- Create an issue on GitHub
- Contact your legal counsel for compliance questions
- Contact Florida DMV for API access questions

## Disclaimer

This software is provided "as is" for authorized use only. Users are solely responsible for legal compliance. The developers make no warranties and assume no liability for misuse.

---

**Last Updated**: January 2026
**Version**: 1.0.0
