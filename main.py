#!/usr/bin/env python3
"""
Vehicle Buyer Finder Application

Main application for finding potential vehicle buyers using Yellow Pages
and authorized DMV data sources.

Usage:
    python main.py --help
    python main.py --locations "Jacksonville,FL" "Saint Augustine,FL"
    python main.py --mock-dmv  # Use mock DMV data for testing
"""
import argparse
import logging
import sys
import json
from config import Config
from yellowpages_scraper import YellowPagesScraper
from dmv_integration import DMVIntegration, MockDMVIntegration
from prospect_finder import ProspectFinder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║         VEHICLE BUYER FINDER APPLICATION                 ║
    ║                                                           ║
    ║  Finding potential vehicle buyers in your area           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_legal_notice():
    """Print important legal notice."""
    notice = """
    ⚠️  LEGAL NOTICE ⚠️
    ═════════════════════════════════════════════════════════════

    This application may access personal information subject to:
    - Driver's Privacy Protection Act (DPPA)
    - Telephone Consumer Protection Act (TCPA)
    - CAN-SPAM Act

    YOU MUST:
    ✓ Have proper authorization for DMV data access
    ✓ Comply with all applicable privacy laws
    ✓ Obtain consent before marketing communications
    ✓ Maintain Do Not Call registry compliance

    Unauthorized use may result in civil and criminal penalties.
    ═════════════════════════════════════════════════════════════
    """
    print(notice)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Find potential vehicle buyers using public and authorized data sources'
    )

    parser.add_argument(
        '--locations',
        nargs='+',
        default=Config.TARGET_LOCATIONS,
        help='Target locations (e.g., "Jacksonville,FL" "Saint Augustine,FL")'
    )

    parser.add_argument(
        '--categories',
        nargs='+',
        default=Config.SEARCH_CATEGORIES,
        help='Business categories to search'
    )

    parser.add_argument(
        '--mock-dmv',
        action='store_true',
        help='Use mock DMV data (for testing only)'
    )

    parser.add_argument(
        '--yellowpages-only',
        action='store_true',
        help='Only search Yellow Pages (skip DMV)'
    )

    parser.add_argument(
        '--output-format',
        choices=['csv', 'excel', 'json'],
        default=Config.OUTPUT_FORMAT,
        help='Output format for results'
    )

    parser.add_argument(
        '--no-legal-notice',
        action='store_true',
        help='Skip legal notice (not recommended)'
    )

    args = parser.parse_args()

    # Display banner and legal notice
    print_banner()

    if not args.no_legal_notice:
        print_legal_notice()
        response = input("\nDo you acknowledge and agree to comply with all legal requirements? (yes/no): ")
        if response.lower() != 'yes':
            logger.error("Legal compliance acknowledgment required. Exiting.")
            sys.exit(1)

    logger.info("Starting Vehicle Buyer Finder...")
    logger.info(f"Target locations: {args.locations}")
    logger.info(f"Search categories: {args.categories}")

    # Initialize prospect finder
    finder = ProspectFinder(output_directory=Config.OUTPUT_DIRECTORY)

    # 1. Search Yellow Pages
    logger.info("\n" + "="*60)
    logger.info("PHASE 1: Searching Yellow Pages")
    logger.info("="*60)

    scraper = YellowPagesScraper(Config.YELLOWPAGES_BASE_URL)

    try:
        yp_data = scraper.search_multiple_locations(
            categories=args.categories,
            locations=args.locations
        )

        logger.info(f"Found {len(yp_data)} Yellow Pages listings")
        finder.add_yellowpages_data(yp_data)

    except Exception as e:
        logger.error(f"Error searching Yellow Pages: {e}")

    # 2. Query DMV data (if enabled)
    if not args.yellowpages_only:
        logger.info("\n" + "="*60)
        logger.info("PHASE 2: Querying DMV Data")
        logger.info("="*60)

        try:
            if args.mock_dmv:
                logger.warning("Using MOCK DMV data for testing")
                dmv = MockDMVIntegration()
            else:
                if not Config.validate_dmv_credentials():
                    logger.error(
                        "DMV credentials not configured. "
                        "Use --mock-dmv for testing or configure credentials in .env"
                    )
                    sys.exit(1)

                dmv = DMVIntegration(
                    api_key=Config.DMV_API_KEY,
                    endpoint=Config.DMV_API_ENDPOINT,
                    user_id=Config.DMV_AUTHORIZED_USER_ID
                )

            # Query each location
            for location in args.locations:
                try:
                    dmv_data = dmv.find_recent_buyers(location, days=90)
                    logger.info(f"Found {len(dmv_data)} DMV records for {location}")
                    finder.add_dmv_data(dmv_data)
                except Exception as e:
                    logger.error(f"Error querying DMV for {location}: {e}")

        except Exception as e:
            logger.error(f"DMV integration error: {e}")

    # 3. Process and analyze prospects
    logger.info("\n" + "="*60)
    logger.info("PHASE 3: Processing Prospects")
    logger.info("="*60)

    # Categorize prospects
    finder.prospects = finder.categorize_prospects()

    # Score prospects
    finder.prospects = finder.score_prospects()

    # Generate report
    report = finder.generate_report()

    logger.info("\n" + "="*60)
    logger.info("RESULTS SUMMARY")
    logger.info("="*60)
    print(json.dumps(report, indent=2))

    # 4. Export results
    logger.info("\n" + "="*60)
    logger.info("PHASE 4: Exporting Results")
    logger.info("="*60)

    try:
        output_file = finder.export_prospects(format=args.output_format)
        logger.info(f"✓ Results exported to: {output_file}")

        # Also export as JSON for the report
        report_file = finder.export_prospects(
            filename=f"report_{output_file.split('_')[-1].split('.')[0]}",
            format='json'
        )
        logger.info(f"✓ Report exported to: {report_file}")

    except Exception as e:
        logger.error(f"Error exporting results: {e}")

    logger.info("\n" + "="*60)
    logger.info("APPLICATION COMPLETE")
    logger.info("="*60)

    # Display top prospects
    if not finder.prospects.empty:
        print("\nTop 10 Prospects:")
        print("="*60)

        top_prospects = finder.prospects.head(10)
        display_cols = [col for col in ['name', 'phone', 'prospect_type', 'score']
                       if col in top_prospects.columns]

        print(top_prospects[display_cols].to_string(index=False))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
