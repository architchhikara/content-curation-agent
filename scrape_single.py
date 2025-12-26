import os
import sys
from dotenv import load_dotenv

from utils.sheets_handler import SheetsHandler
from scrapers.youtube_scraper import YoutubeScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.facebook_scraper import FacebookScraper
from scrapers.linkedin_scraper import LinkedinScraper

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
# Change these variables to scrape a specific URL
PLATFORM = "youtube"  # Options: 'youtube', 'twitter', 'instagram', 'facebook', 'linkedin'
URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def get_scraper_by_platform(platform_name):
    """Returns the scraper instance based on the platform name."""
    platform_name = platform_name.lower().strip()

    if platform_name == "youtube":
        return YoutubeScraper()
    elif platform_name in ["twitter", "x"]:
        return TwitterScraper()
    elif platform_name == "instagram":
        return InstagramScraper()
    elif platform_name == "facebook":
        return FacebookScraper()
    elif platform_name == "linkedin":
        return LinkedinScraper()
    else:
        return None

def main():
    print(f"Starting Single URL Scraper for Platform: {PLATFORM}")

    # 1. Select Scraper
    scraper = get_scraper_by_platform(PLATFORM)
    if not scraper:
        print(f"Error: Unsupported platform '{PLATFORM}'. Please choose from: youtube, twitter, instagram, facebook, linkedin")
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
    sheets = SheetsHandler()

    # We attempt to connect. If it fails (e.g. invalid creds in this environment), we print error but don't crash.
    if sheets.connect():
        sheets.ensure_header()
        sheets.append_data(data)
    else:
        print("Could not connect to Google Sheets. Data was NOT saved.")

if __name__ == "__main__":
    main()
