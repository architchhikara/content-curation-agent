import os
import sys
from dotenv import load_dotenv

from utils.sheets_handler import SheetsHandler
from scrapers import get_scraper_for_url

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
# Change these variables to scrape a specific URL
URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
SHEET_URL = None # e.g., "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

def main():
    print(f"Starting Single URL Scraper...")

    # 1. Detect Platform and Select Scraper
    scraper = get_scraper_for_url(URL)
    if not scraper:
        print(f"Error: Could not determine platform or unsupported platform for URL: {URL}")
        return

    # 2. Scrape Data
    print(f"Scraping URL: {URL} ...")
    data = scraper.scrape(URL)

    if not data:
        print("Scraping failed. No data retrieved.")
        return

    print("Scraping successful!")
    print(f"Title/Text Preview: {data.get('text', '')[:100]}...")

    # 3. Append to Google Sheet
    print("Connecting to Google Sheets...")

    # Initialize handler with the specific sheet URL if provided
    sheets = SheetsHandler(sheet_url=SHEET_URL)

    # We attempt to connect. If it fails (e.g. invalid creds in this environment), we print error but don't crash.
    if sheets.connect():
        sheets.ensure_header()
        sheets.append_data(data)
    else:
        print("Could not connect to Google Sheets. Data was NOT saved.")

if __name__ == "__main__":
    main()
