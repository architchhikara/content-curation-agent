import os
import sys

# Add the project root to sys.path so we can import scrapers and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.sheets_handler import SheetsHandler
from scrapers.youtube_scraper import YoutubeScraper

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
CHANNEL_URL = "https://www.youtube.com/@ishafoundation" # Example channel
MAX_RESULTS = 25 # Limit for testing
SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

# Advanced Filtering (Apps Script style)
# Format: YYYY-MM-DDTHH:MM:SSZ (RFC 3339)
PUBLISHED_BEFORE = None # e.g., "2024-01-01T00:00:00Z"
PUBLISHED_AFTER = None # e.g., "2023-01-01T00:00:00Z"

# Option to clear the sheet before starting
CLEAR_SHEET = True

def main():
    print(f"Starting Enhanced YouTube Channel Scraper...")
    
    scraper = YoutubeScraper()
    if not scraper.youtube:
        print("Error: YouTube API not initialized. Check your YOUTUBE_API_KEY.")
        return

    # 1. Resolve Channel ID
    print(f"Resolving Channel ID for: {CHANNEL_URL}")
    channel_id = scraper.get_channel_id(CHANNEL_URL)
    if not channel_id:
        print(f"Error: Could not resolve channel ID for {CHANNEL_URL}")
        return
    print(f"Channel ID found: {channel_id}")

    # 2. Initialize Spreadsheet
    sheets = SheetsHandler(sheet_url=SHEET_URL)
    if not sheets.connect():
        print("Could not connect to Google Sheets. Check permissions.")
        return
    
    if CLEAR_SHEET:
        sheets.clear_sheet()
        
    sheets.ensure_header()

    # 3. Get Video URLs (using search for advanced filtering)
    print(f"Fetching up to {MAX_RESULTS} videos from channel...")
    video_urls = scraper.search_videos_in_channel(
        channel_id, 
        max_results=MAX_RESULTS,
        published_before=PUBLISHED_BEFORE,
        published_after=PUBLISHED_AFTER
    )
    
    if not video_urls:
        print("No videos found or error fetching videos.")
        return
    
    print(f"Found {len(video_urls)} videos. Starting optimized batch scrape...")

    # 4. Batch Scrape and Save
    all_data = scraper.scrape_batch(video_urls)
    
    if all_data:
        sheets.append_rows(all_data)
        print(f"\nFinished! Successfully scraped and saved {len(all_data)} videos in one batch.")
    else:
        print("No data retrieved during batch scrape.")

if __name__ == "__main__":
    main()
