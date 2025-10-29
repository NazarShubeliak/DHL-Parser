"""
Handles DHL login 
"""
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import logger, USERNAME, PASSWORD

def login(driver: WebDriver) -> None:
    """
    Logs into DHL portal

    Args:
        driver (WebDriver): get WebDriver from Chrome
    """
    wait = WebDriverWait(driver, 15)

    # Step 1: Press login button
    login_button = wait.until(EC.presence_of_all_elements_located((By.ID, "button-noName")))
    if login_button:
        driver.execute_script('document.querySelector("#button-noName").click();')
        logger.debug("Click Login button")
    else:
        logger.error("Error not found Login button")
        raise TimeoutError("Not found button")

    # ----- Find Login Form -----
    logger.debug("Find login form")
    try:
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys(USERNAME)

        password = wait .until(EC.presence_of_element_located((By.ID, "password")))
        password.send_keys(PASSWORD)

        wait.until(EC.element_to_be_clickable((By.ID, "kc-login"))).click()
        logger.debug("Success login to DHL")
        sleep(4)
    except Exception as e:
        logger.error(f"Error while login: {e}")
        raise