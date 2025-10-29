from pathlib import Path
from config import DATA_DIR, logger, URL
from .scraper import run_scraper
from .tools import clean_folder, unzip_archive
from .invoice_processor import run_invoice_processor

def run_pipeline(start_date: str, end_date: str, download_dir: Path, type: str) -> None:
    """"""
    # Step 1: clear directory
    clean_folder(DATA_DIR)
    logger.info(f"Delete all from dir: {DATA_DIR}")

    # Step 2: run scraper and download all file
    url = f"{URL}?billing-from={start_date}&billing-until={end_date}"
    run_scraper(type, url, download_dir)
    logger.info(f"Run scraper for type:{type} date:{start_date} to {end_date}")

    # Step 3: unzip archive
    unzip_archive(download_dir)
    logger.info("Unzip archive")

    # Step 4: parsing all file and get invoice
    run_invoice_processor(download_dir, type)

    # Step 5: add data to Google Sheet