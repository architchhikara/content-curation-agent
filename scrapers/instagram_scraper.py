import instaloader
import re
from datetime import datetime
from .base_scraper import BaseScraper

class InstagramScraper(BaseScraper):
    def __init__(self):
        self.loader = instaloader.Instaloader()
        # Option to login if credentials are provided in env,
        # but defaulting to anonymous/public access as per requirements.
        # Note: Instaloader often requires login for even public posts nowadays due to IG changes.

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
