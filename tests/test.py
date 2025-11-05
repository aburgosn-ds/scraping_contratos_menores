import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from scrapers.base_scraper import BaseScraper
import time
from io import StringIO

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://aplicacionespnsr.vivienda.gob.pe/spsPNSR/consulta#")
wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located(('id', 'tbProcesos')))
elem = driver.find_element(By.ID, 'tbProcesos')

wait.until(lambda d: len(elem.find_elements(By.CSS_SELECTOR, "tbody tr")) > 0)

html = elem.get_attribute('outerHTML')

print(elem, html)

driver.quit()

df = pd.read_html(StringIO(html))
print(df[0]['CONTACTO'])