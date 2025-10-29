from parser import run_pipeline
from config import INVOICE_DIR, INTERNAL_DIR

if __name__ == "__main__":
    run_pipeline("2025-9-1", "2025-9-30", INVOICE_DIR, "inter")