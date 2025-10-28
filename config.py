"""
Configuration module for Klarna parser.

Loads environment variables and defines constants used across the project.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

# Load environment variable form .env file
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Mode
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"

# General Path
LOG_DIR: Path = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

INVOICE_DIR = BASE_DIR / "data" / "invoice"
INTERNAL_DIR = BASE_DIR / "data" / "internal"

INVOICE_DIR.mkdir(parents=True, exist_ok=True)
INTERNAL_DIR.mkdir(parents=True, exist_ok=True)

# Google Sheet
GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "")
GOOGLE_SHEET_WORKSHEET_NAME: str = os.getenv("GOOGLE_SHEET_WORKSHEET_NAME", "DHL Reports")

# Google Token
GOOGLE_TOKEN: str = os.getenv("GOOGLE_TOKEN", "token.json")

# Date Format
DATE_FORMAT: str = "%Y-%m-%d"

# DHl Config
URL: str = "https://geschaeftskunden.dhl.de/billing/invoice/overview"

# Selenium Setting
CHROME_OPTIONS: Options = Options()

if not DEBUG_MODE:
    # Production mode
    CHROME_OPTIONS.add_argument("--headless")
    CHROME_OPTIONS.add_argument("--disable-gpu")
    CHROME_OPTIONS.add_argument("--window-size=1920,1080")
else:
    # Debug mode
    CHROME_OPTIONS.add_argument("--start-maximized")

# Logging Configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE: Path = LOG_DIR / "dhl_parser.log"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("dhl_parser")