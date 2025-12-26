import os
import time
import random
from urllib.parse import urlparse
from dotenv import load_dotenv

from utils.sheets_handler import SheetsHandler
from utils.helpers import random_sleep

from scrapers.youtube_scraper import YoutubeScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.facebook_scraper import FacebookScraper
from scrapers.linkedin_scraper import LinkedinScraper

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
URLS_TO_SCRAPE = [
    # Add your URLs here
    # "https://www.youtube.com/watch?v=EXAMPLE",
    # "https://twitter.com/user/status/1234567890",
]

def get_scraper_for_url(url):
    domain = urlparse(url).netloc

    if "youtube.com" in domain or "youtu.be" in domain:
        return YoutubeScraper()
    elif "twitter.com" in domain or "x.com" in domain:
        return TwitterScraper()
    elif "instagram.com" in domain:
        return InstagramScraper()
    elif "facebook.com" in domain:
        return FacebookScraper()
    elif "linkedin.com" in domain:
        return LinkedinScraper()
    else:
        print(f"No scraper found for domain: {domain}")
        return None

def main():
    print("Starting Wisdom Scraper...")

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
