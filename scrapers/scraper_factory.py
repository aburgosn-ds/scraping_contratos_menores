# =============================================================================
# scrapers/scraper_factory.py - Factory for creating scrapers
# =============================================================================

from scrapers.static_scraper import StaticScraper
from scrapers.dynamic_scraper import DynamicScraper

class ScraperFactory:
    """Factory for creating appropriate scraper instances."""
    
    @staticmethod
    def create_scraper(config):
        """Create scraper based on configuration type."""
        scraper_type = config.get('type', 'static').lower()
        
        if scraper_type == 'static':
            return StaticScraper(config)
        elif scraper_type == 'dynamic':
            return DynamicScraper(config)
        else:
            raise ValueError(f"Unknown scraper type: {scraper_type}")