from pathlib import Path
from typing import Dict, Optional
import pdfplumber
import pandas as pd
from config import logger

COUNTRY_COLUMN = "Zielland"
MONEY_COLUMN = "Gesamtpreis\nin EUR"
SUMME_COLUMN = "Produkt / Service"


def get_international_invoices(folder_path: Path) -> Dict[str, float]:
    """
    Aggregates invoice totals per country from international PDF reports.

    Args:
        folder_path (Path): Directory containing PDF files.

    Returns:
        Dict[str, float]: Dictionary of country → total amount.
    """
    country_totals: Dict[str, float] = {}
    df = extract_summary_table(folder_path)
    if MONEY_COLUMN in df.columns and COUNTRY_COLUMN in df.columns:
        df = convert_money(df)
        grouped = df.groupby(COUNTRY_COLUMN)[MONEY_COLUMN].sum()
        for country, amount in grouped.items():
            country_totals[country] = country_totals.get(country, 0) + amount
            logger.info(f"{country}: +{amount:.2f} EUR")


def get_domestic_invoice_total(folder_path: Path) -> float:
    """
    Calculates the total domestic invoice amount from PDF reports.

    Args:
        folder_path (Path): Directory containing PDF files.

    Returns:
        float: Total sum of domestic invoices.
    """
    total: float = 0.0

    df = extract_summary_table(folder_path)
    if MONEY_COLUMN in df.columns and SUMME_COLUMN in df.columns:
        df = convert_money(df)
        summe_row = df[df[SUMME_COLUMN].str.contains("Summe", na=False)]
        if not summe_row.empty:
            amount = summe_row[MONEY_COLUMN].values[0]
            total += amount
            logger.info(f"Summe: +{amount:.2f} EUR")


def extract_summary_table(folder_path: Path) -> Optional[pd.DataFrame]:
    """
    Extracts the first summary table from a PDF file that contains the keyword 'ZUSAMMENFASSUNG'.

    Args:
        folder_path (Path): Path to the folder.

    Returns:
        Optional[pd.DataFrame]: Extracted table as a DataFrame, or None if not found.
    """
    for file_path in folder_path.glob("*.pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if "ZUSAMMENFASSUNG" in page:
                    tables = page.extract_tables()
                    if tables:
                        df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                        return df
    return None


def convert_money(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts German-formatted currency strings to float in the MONEY_COLUMN.

    Args:
        df (pd.DataFrame): DataFrame containing monetary values.

    Returns:
        pd.DataFrame: Updated DataFrame with float values in MONEY_COLUMN.
    """
    df[MONEY_COLUMN] = (
        df[MONEY_COLUMN]
        .replace("", "0")
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    return df
