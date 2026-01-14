"""
Vehicle Buyer Prospect Finder

Combines data from multiple sources to identify potential vehicle buyers.
"""
import pandas as pd
import logging
from typing import List, Dict
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProspectFinder:
    """Main class for finding and analyzing vehicle buyer prospects."""

    def __init__(self, output_directory: str = './output'):
        self.output_directory = output_directory
        self.prospects = pd.DataFrame()

        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

    def add_yellowpages_data(self, df: pd.DataFrame):
        """Add Yellow Pages data to prospects."""
        if df.empty:
            logger.warning("No Yellow Pages data to add")
            return

        logger.info(f"Adding {len(df)} Yellow Pages records")
        self.prospects = pd.concat([self.prospects, df], ignore_index=True)

    def add_dmv_data(self, df: pd.DataFrame):
        """Add DMV data to prospects (requires authorization)."""
        if df.empty:
            logger.warning("No DMV data to add")
            return

        logger.info(f"Adding {len(df)} DMV records")
        self.prospects = pd.concat([self.prospects, df], ignore_index=True)

    def filter_prospects(self, criteria: Dict = None) -> pd.DataFrame:
        """
        Filter prospects based on criteria.

        Args:
            criteria: Dictionary of filtering criteria

        Returns:
            Filtered DataFrame
        """
        filtered = self.prospects.copy()

        if criteria is None:
            return filtered

        # Example filters
        if 'min_records' in criteria:
            # Remove duplicates, keep unique contacts
            filtered = filtered.drop_duplicates(
                subset=['name', 'phone'],
                keep='first'
            )

        logger.info(f"Filtered to {len(filtered)} prospects")
        return filtered

    def score_prospects(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Score prospects based on likelihood to buy.

        Args:
            df: DataFrame to score (uses self.prospects if None)

        Returns:
            DataFrame with added 'score' column
        """
        if df is None:
            df = self.prospects.copy()

        # Initialize score
        df['score'] = 0

        # Score based on data completeness
        if 'phone' in df.columns:
            df.loc[df['phone'].notna(), 'score'] += 10

        if 'website' in df.columns:
            df.loc[df['website'].notna(), 'score'] += 5

        if 'address' in df.columns:
            df.loc[df['address'].notna(), 'score'] += 5

        # Score based on source
        if 'source' in df.columns:
            df.loc[df['source'].str.contains('DMV', na=False), 'score'] += 20

        # Sort by score
        df = df.sort_values('score', ascending=False)

        logger.info(f"Scored {len(df)} prospects")
        return df

    def categorize_prospects(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Categorize prospects by type (dealer, buyer, etc.).

        Args:
            df: DataFrame to categorize

        Returns:
            DataFrame with 'prospect_type' column
        """
        if df is None:
            df = self.prospects.copy()

        df['prospect_type'] = 'Unknown'

        # Categorization logic
        if 'name' in df.columns:
            name_lower = df['name'].str.lower().fillna('')

            # Auto dealers
            dealer_keywords = ['auto', 'car', 'dealer', 'motors', 'automotive']
            dealer_mask = name_lower.str.contains('|'.join(dealer_keywords))
            df.loc[dealer_mask, 'prospect_type'] = 'Auto Dealer'

            # Wholesalers/Buyers
            buyer_keywords = ['buyer', 'cash for cars', 'we buy', 'wholesale']
            buyer_mask = name_lower.str.contains('|'.join(buyer_keywords))
            df.loc[buyer_mask, 'prospect_type'] = 'Vehicle Buyer'

            # Body shops
            shop_keywords = ['body shop', 'collision', 'repair']
            shop_mask = name_lower.str.contains('|'.join(shop_keywords))
            df.loc[shop_mask, 'prospect_type'] = 'Body Shop'

        return df

    def export_prospects(self, filename: str = None, format: str = 'csv'):
        """
        Export prospects to file.

        Args:
            filename: Output filename (auto-generated if None)
            format: Output format ('csv', 'excel', 'json')
        """
        if self.prospects.empty:
            logger.warning("No prospects to export")
            return

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"vehicle_buyer_prospects_{timestamp}"

        filepath = os.path.join(self.output_directory, filename)

        # Export based on format
        if format == 'csv':
            self.prospects.to_csv(f"{filepath}.csv", index=False)
            logger.info(f"Exported to {filepath}.csv")

        elif format == 'excel':
            self.prospects.to_excel(f"{filepath}.xlsx", index=False)
            logger.info(f"Exported to {filepath}.xlsx")

        elif format == 'json':
            self.prospects.to_json(f"{filepath}.json", orient='records', indent=2)
            logger.info(f"Exported to {filepath}.json")

        return filepath

    def generate_report(self) -> Dict:
        """
        Generate summary report of prospects.

        Returns:
            Dictionary with report statistics
        """
        report = {
            'total_prospects': len(self.prospects),
            'timestamp': datetime.now().isoformat()
        }

        if not self.prospects.empty:
            # Source breakdown
            if 'source' in self.prospects.columns:
                report['by_source'] = self.prospects['source'].value_counts().to_dict()

            # Type breakdown
            if 'prospect_type' in self.prospects.columns:
                report['by_type'] = self.prospects['prospect_type'].value_counts().to_dict()

            # Completeness
            report['with_phone'] = self.prospects['phone'].notna().sum() if 'phone' in self.prospects.columns else 0
            report['with_address'] = self.prospects['address'].notna().sum() if 'address' in self.prospects.columns else 0

        return report
