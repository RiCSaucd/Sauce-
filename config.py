"""
Configuration management for Vehicle Buyer Finder application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""

    # Yellow Pages Configuration
    YELLOWPAGES_BASE_URL = os.getenv('YELLOWPAGES_BASE_URL', 'https://www.yellowpages.com')

    # DMV Configuration (REQUIRES AUTHORIZATION)
    DMV_API_KEY = os.getenv('DMV_API_KEY')
    DMV_API_ENDPOINT = os.getenv('DMV_API_ENDPOINT')
    DMV_AUTHORIZED_USER_ID = os.getenv('DMV_AUTHORIZED_USER_ID')

    # Search Configuration
    TARGET_LOCATIONS = os.getenv('TARGET_LOCATIONS', 'Jacksonville,FL;Saint Augustine,FL').split(';')
    SEARCH_CATEGORIES = os.getenv('SEARCH_CATEGORIES', 'auto dealers,car buyers').split(',')

    # Output Configuration
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'csv')
    OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY', './output')

    @classmethod
    def validate_dmv_credentials(cls):
        """Validate DMV API credentials are present."""
        if not cls.DMV_API_KEY or not cls.DMV_API_ENDPOINT:
            return False
        return True
