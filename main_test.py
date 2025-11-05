# =============================================================================
# main.py - Entry point and orchestration
# =============================================================================

import logging
from datetime import datetime
import pandas as pd
from config.settings import SCRAPERS_CONFIG, EMAIL_CONFIG
from scrapers.scraper_factory import ScraperFactory
from processors.text_analyzer import TextAnalyzer
from processors.data_filter import DataFilter
from notifications.email_sender import EmailSender
from utils.logger import setup_logger

def main():
    """Main execution function for daily scraping and processing."""
    logger = setup_logger()
    logger.info("Starting daily scraping process")
    
    try:
        email_sender = EmailSender()
        email_sender.send_daily_report(pd.DataFrame({'A': ['Usu', 'Mar'], 'B': ['AA', 'BB']}))

    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()