"""
Utility functions for Klarna parser.

Includes helpers for file system cleanup and Chrome options.
"""

import shutil
from pathlib import Path
from config import logger, DEBUG_MODE
from selenium.webdriver.chrome.options import Options


def clean_folder(folder_path: Path) -> None:
    """
    Remove all file and directory from folder

    Args:
        folder_path (Path): Path to the folder to be cleaned.
    """
    if not folder_path.exists():
        logger.error(f"Error not found: {folder_path}")
        raise FileNotFoundError(f"Error not found: {folder_path}")
    for file in folder_path.iterdir():
        try:
            if file.is_file():
                file.unlink()
                logger.debug(f"Delete file: {folder_path}")

            elif file.is_dir():
                shutil.rmtree(file)
                logger.debug(f"Delete directory: {folder_path}")
        except Exception as e:
            logger.error(f"Error while deletring {folder_path}: {e}")


def get_chrome_options(download_dir: Path) -> Options:
    """
    Creates and configures ChromeOptions for Selenium WebDriver.

    Args:
        download_dir (Path): Target directory where downloaded files will be saved.

    Returns:
        Options: Configured ChromeOptions object ready for WebDriver initialization.
    """
    options = Options()

    prefs = {
        "download.default_directory": str(download_dir.resolve()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    options.add_experimental_option("prefs", prefs)

    if not DEBUG_MODE:
        # Production mode
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    else:
        # Debug mode
        options.add_argument("--start-maximized")

    return options
