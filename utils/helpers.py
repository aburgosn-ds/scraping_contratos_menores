from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC



def select_by_xpath(driver, xpath: str):
    return WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
    )

def selects_by_xpath(driver, xpath: str):
    return WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
