# =============================================================================
# scrapers/dynamic_scraper.py - Dynamic page scraper using Selenium
# =============================================================================

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from scrapers.base_scraper import BaseScraper
from utils.helpers import *
import time

class DynamicScraper(BaseScraper):
    """Scraper for dynamic pages using Selenium."""
    
    def __init__(self, config):
        super().__init__(config)
        self.logger.info("Initializing DynamicScraper with config: %s", {k: v for k, v in config.items() if k != 'selectors'})
        try:
            self.driver = self._setup_driver()
            self.logger.info("WebDriver setup completed successfully")
        except Exception as e:
            self.logger.error("Failed to setup WebDriver: %s", str(e))
            # re-raise so caller is aware if initialization fails
            raise
    
    def _setup_driver(self):
        """Setup Chrome WebDriver with options."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        self.logger.debug("Starting Chrome WebDriver with headless options")
        try:
            driver = webdriver.Chrome(options=chrome_options)
            self.logger.debug("Chrome WebDriver started")
            return driver
        except Exception as e:
            self.logger.exception("Error initializing Chrome WebDriver: %s", str(e))
            raise
    
    def _sleep(self):
        # Additional wait time if specified
        wait_time = self.config.get('wait_time')
        if wait_time:
            time.sleep(wait_time)

    def scrape_page(self, page_url: str) -> pd.DataFrame:
        """Scrape a dynamic page."""
        try:
            self.logger.info("Scraping dynamic page: %s", page_url)
            self.driver.get(page_url)

            # Wait for content to load
            wait = WebDriverWait(self.driver, 10)

            self._sleep()

            # Seleccionar vigente
            self.logger.debug("Selecting 'vigente' checkbox using xpath: %s", self.config['selectors'].get('checkbox_vigente'))
            checkbox_vigente = select_by_xpath(self.driver, self.config['selectors']['checkbox_vigente'])
            checkbox_vigente.click()
            self.logger.debug("Clicked 'vigente' checkbox")

            # Filtrar departamento
            self.logger.debug("Opening department dropdown: %s", self.config['selectors'].get('dropdown_department'))
            dropdown_department = select_by_xpath(self.driver, self.config['selectors']['dropdown_department'])
            dropdown_department.click()

            select_department = select_by_xpath(self.driver, self.config['selectors']['select_department'])
            select_department.click()
            self.logger.debug("Department selected: %s", self.config['selectors'].get('select_department'))

            self._sleep()

            # Número de registros
            paginator = select_by_xpath(self.driver, self.config['selectors']['paginator'])
            paginator_text = paginator.text if paginator is not None else ''
            self.logger.debug("Paginator text: %s", paginator_text)
            n_records = int(paginator_text.split("of")[-1].strip()) if paginator_text else 0
            self.logger.info("Found %s records on the page", n_records)

            if n_records > 5:
                dropdown_records_per_page = select_by_xpath(self.driver, self.config['selectors']['dropdown_records_per_page'])
                dropdown_records_per_page.click()

                max_records = select_by_xpath(self.driver, self.config['selectors']['max_records'])
                max_records.click()

                self._sleep()

                all_calls = selects_by_xpath(self.driver, self.config['selectors']['all_calls'])
                self.logger.info("Located %s call elements on page", len(all_calls) if all_calls is not None else 0)

                dict_calls = {'codigo': [],
                            'titulo': [],
                            'empresa': [],
                            'objeto': [], 
                            'descripcion': [], 
                            'cotizacion_comienzo': [], 
                            'cotizacion_fin': [], 
                            'fecha_publicacion': [], 
                            'url': []}

            for call in all_calls:
                ps = call.find_elements(By.XPATH, self.config['selectors']['ps'])
                url = call.find_elements(By.XPATH, self.config['selectors']['url'])[0].get_attribute("href")
                
                temp = [p.text for p in ps]
                dict_calls['codigo'].append(url.split('/')[-1])
                dict_calls['titulo'].append(temp[0])
                dict_calls['empresa'].append(temp[1])
                dict_calls['objeto'].append(temp[2].split(":")[0].lower())
                dict_calls['descripcion'].append(temp[2].split(":")[1].lstrip().upper())
                dict_calls['cotizacion_comienzo'].append(temp[3][14:].split("-")[0].strip())
                dict_calls['cotizacion_fin'].append(temp[3][14:].split("-")[1].strip())
                dict_calls['fecha_publicacion'].append(temp[4][22:].strip())
                dict_calls['url'].append(url)

            # Close driver after scraping this page to free resources
            try:
                self.logger.debug("Quitting WebDriver after scraping page")
                self.driver.quit()
                # avoid double-quitting later
                delattr(self, 'driver')
            except Exception:
                # ignore errors on quit but log them
                self.logger.exception("Exception while quitting WebDriver")

            df = pd.DataFrame(dict_calls)
            self.logger.info("Scraped DataFrame with shape %s", df.shape)
            return df
            
        except Exception as e:
            self.logger.exception("Error scraping dynamic page %s: %s", page_url, str(e))
            # Attempt to close driver if it's still present
            try:
                if hasattr(self, 'driver'):
                    self.driver.quit()
                    delattr(self, 'driver')
            except Exception:
                self.logger.exception("Error while closing WebDriver after exception")
            return pd.DataFrame()
    
    def get_next_page_url(self, current_url: str, page_num: int) -> str:
        """Handle pagination for dynamic sites."""
        # For dynamic sites, we might need to click buttons instead
        return current_url  # Override this method based on specific site needs
    
    def __del__(self):
        """Cleanup driver."""
        self.logger.debug("Destructor called for DynamicScraper")
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                self.logger.info("WebDriver quit in destructor")
            except Exception:
                self.logger.exception("Error quitting WebDriver in destructor")