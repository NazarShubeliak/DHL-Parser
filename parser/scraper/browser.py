"""
Handles browser setup and cookie acceptance for Klarna scraping.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config import logger, CHROME_OPTIONS
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def create_driver() -> webdriver.Chrome:
    """Initialize and return a Chrome WebDriver instance"""
    logger.debug("Launching Chrome browser")
    driver = webdriver.Chrome(options=CHROME_OPTIONS)
    return driver

def accept_cookies(wait: WebDriverWait) -> None:
    """Accept DHL's cookie banner if present"""
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
        logger.debug("Cookiew accepted")
    except Exception as e:
        logger.error("Cookie banner not found: {e}")
        raise