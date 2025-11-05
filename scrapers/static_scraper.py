# =============================================================================
# scrapers/static_scraper.py - Static page scraper
# =============================================================================

import pandas as pd
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class StaticScraper(BaseScraper):
    """Scraper for static HTML pages."""
    
    def scrape_page(self, page_url: str) -> pd.DataFrame:
        """Scrape a static page."""
        try:
            response = self.session.get(page_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            records = []
            
            # Find all record containers
            record_elements = soup.select(self.config['selectors']['records_container'])
            
            for element in record_elements:
                record = {}
                
                # Extract data based on selectors
                for field, selector in self.config['selectors'].items():
                    if field not in ['records_container', 'next_page']:
                        field_element = element.select_one(selector)
                        record[field] = field_element.get_text(strip=True) if field_element else ''
                
                if record:  # Only add if we got some data
                    records.append(record)
            
            return pd.DataFrame(records)
            
        except Exception as e:
            self.logger.error(f"Error scraping static page {page_url}: {str(e)}")
            return pd.DataFrame()
    
    def get_next_page_url(self, current_url: str, page_num: int) -> str:
        """Generate next page URL for static sites."""
        if '?' in current_url:
            return f"{current_url}&page={page_num}"
        else:
            return f"{current_url}?page={page_num}"