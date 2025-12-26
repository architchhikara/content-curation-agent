import os
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv
from .base_scraper import BaseScraper

load_dotenv()

class YoutubeScraper(BaseScraper):
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = None
        if self.api_key:
            self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def extract_video_id(self, url):
        """Extracts the video ID from a YouTube URL."""
        # Examples:
        # https://www.youtube.com/watch?v=VIDEO_ID
        # https://youtu.be/VIDEO_ID
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    def scrape(self, url):
        if not self.youtube:
            print("Error: YOUTUBE_API_KEY not found in environment variables.")
            return None

        video_id = self.extract_video_id(url)
        if not video_id:
            print(f"Error: Could not extract video ID from {url}")
            return None

        try:
            request = self.youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()

            if not response["items"]:
                print(f"Error: Video not found for ID {video_id}")
                return None

            snippet = response["items"][0]["snippet"]

            title = snippet.get("title", "")
            description = snippet.get("description", "")
            author = snippet.get("channelTitle", "")
            date = snippet.get("publishedAt", "")

            # Combine title and description for the text field
            text_content = f"Title: {title}\n\nDescription:\n{description}"

            return {
                "source": "YouTube",
                "author": author,
                "date": date,
                "text": text_content,
                "url": url
            }

        except Exception as e:
            print(f"Error scraping YouTube URL {url}: {e}")
            return None
