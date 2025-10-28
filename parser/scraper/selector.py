from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import logger

def select_last_option(driver: WebDriver) -> None:
    """
    Selects the last available option from a DHL-style <select> dropdown.

    This function waits for a <select> element with class 'dhlInputSelect' to appear,
    then selects and clicks the last option in the dropdown. Useful for selecting
    'All' or the most recent report type in DHL interfaces.

    Args:
        driver (WebDriver): Active Selenium WebDriver instance.
    """
    logger.debug("Find drop menu and select option 'All'")
    wait = WebDriverWait(driver, 10)
    button_select = Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select.dhlInputSelect"))))
    last_element_idex = len(button_select) - 1
    button_select.options[last_element_idex].click()