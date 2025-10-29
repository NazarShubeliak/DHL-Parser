from pathlib import Path
from parser.tools import clean_folder, unzip_archive
from config import DATA_DIR, logger, URL
from parser.scraper.scraper import run_scraper

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

    # Step 4: parsing all file and get data

    # Step 5: add data to Google Sheet