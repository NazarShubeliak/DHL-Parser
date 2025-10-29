from pathlib import Path
from .browser import create_driver, accept_cookies
from .login import login
from .downloader import downloader_run
from config import logger
def run_scraper(type: str, url: str, download_dir: Path) -> None:
    """
    """
    logger.debug("Start DHL scraping")

    # Step 1: Create driver
    driver = create_driver(download_dir)
    driver.get(url)
    logger.debug("Create driver")

    # Step 2: Accept Cookies
    accept_cookies(driver)
    logger.debug("Accept Cookies")

    # Step 3: Login to DHL
    login(driver)
    logger.debug("Login to DHL")

    # Step 4: Select all necessary file and download
    downloader_run(driver, type)
    logger.debug("Download all files")