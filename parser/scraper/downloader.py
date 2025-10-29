from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from config import logger


def downloader_run(driver: WebDriver, type: str) -> None:
    """
    Downloads DHL files based on type by selecting appropriate checkboxes.

    Args:
        driver (WebDriver): Active Selenium driver.
        type (str): Type of report to download ("invoice" or "internacional").

    Raises:
        ValueError: If type is invalid or selection fails.
    """
    wait = WebDriverWait(driver, 15)

    # Step 1: Find table
    all_files = find_table(wait)
    logger.debug(f"Table found with files {len(all_files)}")

    # Step 2: Select all the necessary files
    file_filter(all_files, type)
    logger.debug(f"Files selected for type: {type}")

    # Step 3: Download selected files
    download(wait)
    logger.debug(f"Download all selected files")


def find_table(wait: WebDriverWait) -> List[WebElement]:
    """
    Waits for the DHL results table to appear and returns all file rows.

    This function locates the main results table on the DHL page by its class name,
    extracts the <tbody> section, and returns all rows that represent downloadable files.

    Args:
        wait (WebDriverWait): Selenium wait object used to wait for the table to load.

    Returns:
        list[WebElement]: List of table rows with class 'hasDetailView', representing individual files.
    """
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dhlTable")))
    table_body = table.find_element(By.TAG_NAME, "tbody")
    all_file = table_body.find_elements(By.CLASS_NAME, "hasDetailView")
    return all_file


def file_filter(all_files: list[WebElement], type: str) -> None:
    """
    Filters and selects DHL files based on type.

    Args:
        all_files (list[WebElement]): List of table rows representing files.
        type (str): Type of report ("invoice" or "internacional").

    Raises:
        ValueError: If type is invalid.
    """
    for file in all_files:
        cell = file.find_elements(By.TAG_NAME, "td")
        file_text = cell[3].text
        file_value = cell[4].text

        def click_checkbox(element: WebElement) -> None:
            button_check = element.find_element(By.CLASS_NAME, "checkbox")
            if button_check:
                button_check.click()

        if type == "invoice":
            if not "INT" in file_text and not "-" in file_value:
                click_checkbox(file)
        elif type == "internacional":
            if "INT" in file_text and not "-" in file_value:
                click_checkbox(file)
        else:
            logger.error("Failed to select DHL file: unknown type '%s'", type)
            raise ValueError(f"Failed to select DHL file: unknown type '{type}'")


def download(wait: WebDriverWait) -> None:
    """
    Press button to download all file

    Args:
        wait (WebDriverWait): Selenium wait object used to wait for the table to load.
    """
    button = wait.until(
        EC.presence_of_element_located((By.ID, "button-downloadSelectedInvoices"))
    )
    button.click()
