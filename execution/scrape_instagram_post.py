import os
import sys

# Add the project root to sys.path so we can import scrapers and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.sheets_handler import SheetsHandler
from scrapers import get_scraper_for_url

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
INSTAGRAM_URL = "https://www.instagram.com/p/C_mX..." # Add link here
SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

def main():
    print(f"Starting Instagram Single Scraper...")

    scraper = get_scraper_for_url(INSTAGRAM_URL)
    if not scraper:
        print(f"Error: Could not determine platform for URL: {INSTAGRAM_URL}")
        return

    print(f"Scraping Instagram URL: {INSTAGRAM_URL} ...")
    data = scraper.scrape(INSTAGRAM_URL)

    if not data:
        print("Scraping failed. No data retrieved.")
        return

    print("Scraping successful!")
    
    sheets = SheetsHandler(sheet_url=SHEET_URL)
    if sheets.connect():
        sheets.ensure_header()
        sheets.append_data(data)
    else:
        print("Could not connect to Google Sheets. Data was NOT saved.")

if __name__ == "__main__":
    main()
