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
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        """Setup Chrome WebDriver with options."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        return webdriver.Chrome(options=chrome_options)
    
    def _sleep(self):
        # Additional wait time if specified
            if 'wait_time' in self.config:
                time.sleep(self.config['wait_time'])

    def scrape_page(self, page_url: str) -> pd.DataFrame:
        """Scrape a dynamic page."""
        try:
            self.driver.get(page_url)
            
            # Wait for content to load
            wait = WebDriverWait(self.driver, 10)
            
            self._sleep()

            # Seleccionar vigente
            checkbox_vigente = select_by_xpath(self.driver, self.config['selectors']['checkbox_vigente'])
            checkbox_vigente.click()

            # Filtrar departamento
            dropdown_department = select_by_xpath(self.driver, self.config['selectors']['dropdown_department'])
            dropdown_department.click()

            select_department = select_by_xpath(self.driver, self.config['selectors']['select_department'])
            select_department.click()

            self._sleep()

            # Número de registros
            paginator = select_by_xpath(self.driver, self.config['selectors']['paginator'])
            n_records = int(paginator.text.split("of")[-1].strip())

            if n_records > 5:
                dropdown_records_per_page = select_by_xpath(self.driver, self.config['selectors']['dropdown_records_per_page'])
                dropdown_records_per_page.click()

                max_records = select_by_xpath(self.driver, self.config['selectors']['max_records'])
                max_records.click()

                self._sleep()

                all_calls = selects_by_xpath(self.driver, self.config['selectors']['all_calls'])

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


            
            records = []
            record_elements = self.driver.find_elements(By.CLASS_NAME, self.config['selectors']['records_container'])
            
            for element in record_elements:
                record = {}
                
                for field, selector in self.config['selectors'].items():
                    if field not in ['records_container', 'load_more_button']:
                        try:
                            field_element = element.find_element(By.CSS_SELECTOR, selector)
                            record[field] = field_element.text.strip()
                        except:
                            record[field] = ''
                
                if record:
                    records.append(record)
            
            return pd.DataFrame(records)
            
        except Exception as e:
            self.logger.error(f"Error scraping dynamic page {page_url}: {str(e)}")
            return pd.DataFrame()
    
    def get_next_page_url(self, current_url: str, page_num: int) -> str:
        """Handle pagination for dynamic sites."""
        # For dynamic sites, we might need to click buttons instead
        return current_url  # Override this method based on specific site needs
    
    def __del__(self):
        """Cleanup driver."""
        if hasattr(self, 'driver'):
            self.driver.quit()