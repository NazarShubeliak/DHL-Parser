from concurrent.futures import ThreadPoolExecutor
from parser import run_pipeline
from config import INVOICE_DIR, INTERNAL_DIR

def process_international():
    return run_pipeline("2025-9-1", "2025-9-30", INVOICE_DIR, "invoice")

def process_domestic():
    return run_pipeline("2025-9-1", "2025-9-30", INTERNAL_DIR, "inter")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_int = executor.submit(process_international)
        future_dom = executor.submit(process_domestic)