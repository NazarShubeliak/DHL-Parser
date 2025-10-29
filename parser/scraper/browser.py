"""
Handles browser setup and cookie acceptance for Klarna scraping.
"""

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from config import logger
from parser.tools import get_chrome_options

def create_driver(download_dir_path: Path) -> webdriver.Chrome:
    """Initialize and return a Chrome WebDriver instance"""
    logger.debug("Launching Chrome browser")
    driver = webdriver.Chrome(options=get_chrome_options(download_dir_path))
    return driver

def accept_cookies(driver: WebDriver) -> None:
    """Accept DHL's cookie banner if present"""
    try:
        wait = WebDriverWait(driver, 10)
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
        logger.debug("Cookiew accepted")
    except Exception as e:
        logger.error("Cookie banner not found: {e}")
        raise