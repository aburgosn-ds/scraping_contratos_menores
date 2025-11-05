# =============================================================================
# scrapers/base_scraper.py - Abstract base scraper
# =============================================================================

from abc import ABC, abstractmethod
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, Any

class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @abstractmethod
    def scrape_page(self, page_url: str) -> pd.DataFrame:
        """Scrape a single page and return DataFrame."""
        pass
    
    @abstractmethod
    def get_next_page_url(self, current_url: str, page_num: int) -> str:
        """Get the URL for the next page."""
        pass
    
    def scrape_all_pages(self) -> pd.DataFrame:
        """Scrape all pages and return combined DataFrame."""
        all_data = []
        page_num = 1
        max_pages = self.config.get('max_pages', 10)
        
        while page_num <= max_pages:
            try:
                page_url = self.get_next_page_url(self.config['base_url'], page_num)
                self.logger.info(f"Scraping page {page_num}: {page_url}")
                
                page_data = self.scrape_page(page_url)
                
                if page_data.empty:
                    self.logger.info(f"No data found on page {page_num}, stopping")
                    break
                
                all_data.append(page_data)
                page_num += 1
                
                # Add delay between requests
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page_num}: {str(e)}")
                break
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()