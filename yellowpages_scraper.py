"""
Yellow Pages scraper for finding auto-related businesses and contacts.
This module scrapes publicly available Yellow Pages data.
"""
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YellowPagesScraper:
    """Scraper for Yellow Pages business listings."""

    def __init__(self, base_url: str = "https://www.yellowpages.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def search_location(self, category: str, location: str) -> List[Dict]:
        """
        Search Yellow Pages for a specific category in a location.

        Args:
            category: Business category (e.g., 'auto dealers', 'car buyers')
            location: Location string (e.g., 'Jacksonville, FL')

        Returns:
            List of business dictionaries with contact information
        """
        logger.info(f"Searching Yellow Pages: {category} in {location}")

        businesses = []

        # Format the search URL
        search_url = f"{self.base_url}/search"
        params = {
            'search_terms': category,
            'geo_location_terms': location
        }

        try:
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse business listings
            # Note: Yellow Pages structure may change, this is a template
            listings = soup.find_all('div', class_='result')

            for listing in listings:
                business = self._parse_listing(listing)
                if business:
                    businesses.append(business)

            logger.info(f"Found {len(businesses)} businesses")
            time.sleep(2)  # Be respectful with rate limiting

        except requests.RequestException as e:
            logger.error(f"Error fetching Yellow Pages data: {e}")

        return businesses

    def _parse_listing(self, listing) -> Dict:
        """Parse a single business listing."""
        try:
            business = {
                'name': '',
                'phone': '',
                'address': '',
                'website': '',
                'category': '',
                'source': 'YellowPages'
            }

            # Extract business name
            name_elem = listing.find('a', class_='business-name')
            if name_elem:
                business['name'] = name_elem.get_text(strip=True)

            # Extract phone number
            phone_elem = listing.find('div', class_='phones')
            if phone_elem:
                business['phone'] = phone_elem.get_text(strip=True)

            # Extract address
            address_elem = listing.find('div', class_='street-address')
            if address_elem:
                business['address'] = address_elem.get_text(strip=True)

            # Extract website if available
            website_elem = listing.find('a', class_='track-visit-website')
            if website_elem:
                business['website'] = website_elem.get('href', '')

            return business if business['name'] else None

        except Exception as e:
            logger.error(f"Error parsing listing: {e}")
            return None

    def search_multiple_locations(self, categories: List[str],
                                  locations: List[str]) -> pd.DataFrame:
        """
        Search multiple categories across multiple locations.

        Args:
            categories: List of business categories
            locations: List of locations

        Returns:
            DataFrame with all collected business data
        """
        all_businesses = []

        for location in locations:
            for category in categories:
                businesses = self.search_location(category, location)
                all_businesses.extend(businesses)

        df = pd.DataFrame(all_businesses)

        # Remove duplicates based on phone number
        if not df.empty and 'phone' in df.columns:
            df = df.drop_duplicates(subset=['phone'], keep='first')

        return df
