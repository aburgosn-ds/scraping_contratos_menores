# =============================================================================
# main.py - Entry point and orchestration
# =============================================================================

import sqlite3
import logging
from datetime import datetime
import pandas as pd
from config.settings import SCRAPERS_CONFIG, EMAIL_CONFIG
from scrapers.scraper_factory import ScraperFactory
from processors.text_analyzer import TextAnalyzer
# from processors.data_filter import DataFilter
from processors.data_filter import DataFilter
from notifications.email_sender import EmailSender
from scrapers.dynamic_scraper import DynamicScraper
from utils.logger import setup_logger
from database import connection
import sqlite3
import warnings


def main():
    """Main execution function for daily scraping and processing."""
    logger = setup_logger()
    logger.info("Starting daily scraping process")
    
    # 1 Scraping
    scraper = DynamicScraper(SCRAPERS_CONFIG['contratos_menores_seace'])
    df_contrataciones_hoy = scraper.scrape_page("https://prod6.seace.gob.pe/buscador-publico/contrataciones")

    # 2 Conexión db
    db = connection.DbManager('./tests/convocatorias.db')
    db_codes = db.select_all_codes('convocatorias')

    # 3 Data filtering
    data_filter = DataFilter(df_contrataciones_hoy)
    result = data_filter.df_filter_old_data(db_codes)

    # 4 Text analysis
    text_analyzer = TextAnalyzer()
    df_result = text_analyzer.analyze_text_topic(result)
    
    # 5 Save data to db
    with sqlite3.connect("./tests/convocatorias.db") as conn:
        df_result.to_sql("convocatorias", con=conn, if_exists='append', index=False)
        logger.info("Data saved successfully to db")

    df_accepted = df_result[df_result.util == 1]

    # Clean df to send
    df_accepted = df_accepted.loc[:, ['empresa', 'objeto', 'descripcion', 'fecha_publicacion', 'url']]
    df_accepted.columns = ['Empresa', 'Tipo', 'Descripcion', 'Fecha de Publicación', 'Link']
    
    
    # 6 Send email
    email_sender = EmailSender()
    email_sender.send_daily_report(df_accepted)
    return result


if __name__ == "__main__":
    main()