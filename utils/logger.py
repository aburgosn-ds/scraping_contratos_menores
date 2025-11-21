import logging
import os
from logging.handlers import RotatingFileHandler


# def setup_logger(log_level=logging.INFO, log_file='logs/app.log'):
#     """Create and return a configured logger for the project.

#     Ensures the `logs/` directory exists and configures a rotating file
#     handler plus a console stream handler. Safe to call multiple times.
#     """
#     os.makedirs(os.path.dirname(log_file), exist_ok=True)

#     logger = logging.getLogger('ConvocatoriasScraper')
#     logger.setLevel(log_level)

#     if not logger.handlers:
#         formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

#         fh = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')
#         fh.setLevel(log_level)
#         fh.setFormatter(formatter)

#         ch = logging.StreamHandler()
#         ch.setLevel(log_level)
#         ch.setFormatter(formatter)

#         logger.addHandler(fh)
#         logger.addHandler(ch)

#     return logger

# =============================================================================
# utils/logger.py - Logging configuration
# =============================================================================

import logging
import os
from datetime import datetime

def setup_logger():
    """Setup logging configuration."""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    log_filename = f"logs/scraping_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    return logging.getLogger('WebScrapingApp')