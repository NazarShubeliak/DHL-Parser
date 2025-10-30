# DHL Invoice Parser

This project automates the downloading, extraction, parsing, and aggregation of DHL invoice data, then writes the results to a Google Sheet.

## 🔧 Features

- Multi-threaded ZIP file downloading
- Automatic archive extraction and cleanup
- PDF invoice parsing with table extraction
- Separate handling of domestic and international invoices
- Google Sheets integration for reporting
- Parallel processing using threads

## 📁 Project Structure

```bash
root/
├── run.py                   
├── parser/                  
│   ├── __init__.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── browser.py
│   │   ├── login.py
│   │   ├── scraper.py.py
│   │   └── selector.py
│   ├── invoice_processor.py
│   ├── pipeline.py
│   ├── pipeline.py
│   ├── sheet.py
│   └── tools.py
```
## 🚀 How to Run

```bash
python run.py
```

## 🔐 Google Sheets Authorization
Create a service account in Google Cloud Console, download the credentials.json file, and share access to your spreadsheet with the service account email.