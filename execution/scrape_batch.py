import os
import sys

# Add the project root to sys.path so we can import scrapers and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import random
from dotenv import load_dotenv

from utils.sheets_handler import SheetsHandler
from utils.helpers import random_sleep
from scrapers import get_scraper_for_url

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
URLS_TO_SCRAPE = [
    # Add your URLs here
    # "https://www.youtube.com/watch?v=EXAMPLE",
    # "https://twitter.com/user/status/1234567890",
]

def main():
    print("Starting Wisdom Batch Scraper...")

    # Initialize Google Sheets Handler
    sheets = SheetsHandler()
    if not sheets.connect():
        print("Failed to connect to Google Sheets. Exiting.")
        return

    sheets.ensure_header()

    for url in URLS_TO_SCRAPE:
        print(f"\nProcessing: {url}")

        # Random Delay
        random_sleep(5, 15)

        scraper = get_scraper_for_url(url)
        if not scraper:
            continue

        try:
            data = scraper.scrape(url)

            if data:
                sheets.append_data(data)
            else:
                print(f"Failed to scrape data for {url}")

        except Exception as e:
            # Basic error handling
            print(f"An unexpected error occurred: {e}")

            # Circuit Breaker for Rate Limiting (HTTP 429)
            # Some libraries raise specific exceptions, but generally we look for '429' in the error message
            if "429" in str(e):
                print("CRITICAL: Rate limit exceeded (429). Stopping script immediately.")
                break

    print("\nScraping complete.")

if __name__ == "__main__":
    main()
