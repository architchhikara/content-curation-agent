import unittest
import sys
import os

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapers import get_scraper_for_url
from scrapers.youtube_scraper import YoutubeScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.facebook_scraper import FacebookScraper
from scrapers.linkedin_scraper import LinkedinScraper
from utils.sheets_handler import SheetsHandler

class TestSingleExecution(unittest.TestCase):
    def test_get_scraper_for_url(self):
        """Test that the factory function returns the correct scraper class based on URL."""
        self.assertIsInstance(get_scraper_for_url("https://www.youtube.com/watch?v=123"), YoutubeScraper)
        self.assertIsInstance(get_scraper_for_url("https://youtu.be/123"), YoutubeScraper)
        self.assertIsInstance(get_scraper_for_url("https://twitter.com/user/status/123"), TwitterScraper)
        self.assertIsInstance(get_scraper_for_url("https://x.com/user/status/123"), TwitterScraper)
        self.assertIsInstance(get_scraper_for_url("https://www.instagram.com/p/123/"), InstagramScraper)
        self.assertIsInstance(get_scraper_for_url("https://www.facebook.com/post/123"), FacebookScraper)
        self.assertIsInstance(get_scraper_for_url("https://www.linkedin.com/posts/123"), LinkedinScraper)

        self.assertIsNone(get_scraper_for_url("https://example.com"))

    def test_sheets_handler_init(self):
        """Test SheetsHandler initialization with and without URL."""
        # Test with URL
        handler_url = SheetsHandler(sheet_url="https://docs.google.com/spreadsheets/d/123")
        self.assertEqual(handler_url.sheet_url, "https://docs.google.com/spreadsheets/d/123")

        # Test without URL (default)
        handler_default = SheetsHandler()
        self.assertIsNone(handler_default.sheet_url)

if __name__ == '__main__':
    unittest.main()
