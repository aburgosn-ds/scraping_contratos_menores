# =============================================================================
# main.py - Entry point and orchestration
# =============================================================================

import logging
from datetime import datetime
import pandas as pd
from config.settings import SCRAPERS_CONFIG, EMAIL_CONFIG, TOPICS_CONFIG
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
        # Initialize components
        scraper_factory = ScraperFactory()
        text_analyzer = TextAnalyzer()
        data_filter = DataFilter(text_analyzer)
        email_sender = EmailSender()
        
        all_filtered_data = []
        
        # Process each configured scraper
        for scraper_config in SCRAPERS_CONFIG:
            logger.info(f"Processing scraper: {scraper_config['name']}")
            
            # Create appropriate scraper
            scraper = scraper_factory.create_scraper(scraper_config)
            
            # Scrape data
            raw_data = scraper.scrape_all_pages()
            
            if not raw_data.empty:
                # Filter data based on topic analysis
                filtered_data = data_filter.filter_by_topics(
                    raw_data, 
                    scraper_config['description_column'],
                    TOPICS_CONFIG['accepted_topics']
                )
                
                if not filtered_data.empty:
                    filtered_data['source'] = scraper_config['name']
                    all_filtered_data.append(filtered_data)
                    logger.info(f"Found {len(filtered_data)} relevant records from {scraper_config['name']}")
                else:
                    logger.info(f"No relevant records found from {scraper_config['name']}")
            else:
                logger.warning(f"No data scraped from {scraper_config['name']}")
        
        # Combine all filtered data and send email
        if all_filtered_data:
            combined_data = pd.concat(all_filtered_data, ignore_index=True)
            email_sender.send_daily_report(combined_data)
            logger.info(f"Daily report sent with {len(combined_data)} total records")
        else:
            logger.info("No relevant data found. No email sent.")
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()