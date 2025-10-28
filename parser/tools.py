"""
Utility functions for Klarna parser.

Includes helpers for file system cleanup and formatting.
"""

import shutil
from typing import Tuple
from pathlib import Path
from config import logger


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
