from typing import Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import (
    logger,
    GERMAN_TO_ISO,
    COUNTRY_ORDER,
    GOOGLE_SHEET_RANGE,
    GOOGLE_TOKEN,
)


class SheetService:
    def __init__(self, sheet_name: str, worksheet_name: str, creds_path: str) -> None:
        self.sheet_name = sheet_name
        self.creds_path = creds_path
        self.sheet = self.__authorize(worksheet_name)

    def __authorize(self, worksheet_name: str) -> gspread.Worksheet:
        """
        Authorizes and returns a worksheet using service account credentials.

        Args:
            worksheet_name (str): The name of the worksheet tab.

        Returns:
            gspread.Worksheet: The worksheet object
        """
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_TOKEN, scope)
        client = gspread.authorize(creds)
        logger.debug("Authorize complete")

        return client.open(self.sheet).get_worksheet(worksheet_name)

    def get_worksheet(self, worksheet_name: str) -> None:
        """
        Returns a specific worksheet by name

        Args:
            worksheet_name (str): write name worksheet from Google Sheet
        """
        return self.sheet.get_worksheet(worksheet_name)

    def write_country_totals(self, international_data: Dict[str, float], domestic_total: float) -> None:
        """
        Writes country totals to the configured Google Sheet.

        Args:
            international_data (dict[str, float]): Country totals from international invoices.
            domestic_total (float): Total from domestic invoices (Germany).
        """
        country_totals_iso: Dict[str, float] = {}

        for german_name, amount in international_data.items():
            iso_code = GERMAN_TO_ISO.get(german_name)
            if iso_code:
                country_totals_iso[iso_code] = amount
            else:
                logger.warning(f"[!] Unkown country: '{german_name}' - add to GERMAN_TO_ISO map.")

        country_totals_iso["DE"] = domestic_total

        row_data = [round(country_totals_iso.get(code, 0.0), 2) for code in COUNTRY_ORDER]
        self.sheet.update(GOOGLE_SHEET_RANGE, [row_data])
        logger.info(f"Data written to sheet range {GOOGLE_SHEET_RANGE}")
