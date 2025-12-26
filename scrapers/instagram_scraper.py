import instaloader
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from .base_scraper import BaseScraper

load_dotenv()

class InstagramScraper(BaseScraper):
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.login()

    def login(self):
        """Attempts to log in to Instagram if credentials are provided."""
        user = os.getenv("INSTAGRAM_USER")
        password = os.getenv("INSTAGRAM_PASSWORD")

        if user and password:
            try:
                print(f"Attempting Instagram login for user: {user}")
                self.loader.login(user, password)
                print("Instagram login successful.")
            except Exception as e:
                print(f"Warning: Instagram login failed: {e}. Continuing with anonymous session.")
        else:
            print("No Instagram credentials found. Using anonymous session.")

    def extract_shortcode(self, url):
        """Extracts the post shortcode from an Instagram URL."""
        # Example: https://www.instagram.com/p/SHORTCODE/
        pattern = r"instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    def scrape(self, url):
        shortcode = self.extract_shortcode(url)
        if not shortcode:
            print(f"Error: Could not extract shortcode from {url}")
            return None

        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

            return {
                "source": "Instagram",
                "author": post.owner_username,
                "date": str(post.date_local),
                "text": post.caption if post.caption else "",
                "url": url
            }
        except Exception as e:
            print(f"Error scraping Instagram URL {url}: {e}")
            return None
