import unittest
import sys
import os

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrape_single import get_scraper_by_platform
from scrapers.youtube_scraper import YoutubeScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.facebook_scraper import FacebookScraper
from scrapers.linkedin_scraper import LinkedinScraper

class TestSingleExecution(unittest.TestCase):
    def test_get_scraper_by_platform(self):
        """Test that the factory function returns the correct scraper class."""
        self.assertIsInstance(get_scraper_by_platform("youtube"), YoutubeScraper)
        self.assertIsInstance(get_scraper_by_platform("twitter"), TwitterScraper)
        self.assertIsInstance(get_scraper_by_platform("x"), TwitterScraper)
        self.assertIsInstance(get_scraper_by_platform("instagram"), InstagramScraper)
        self.assertIsInstance(get_scraper_by_platform("facebook"), FacebookScraper)
        self.assertIsInstance(get_scraper_by_platform("linkedin"), LinkedinScraper)

        self.assertIsNone(get_scraper_by_platform("invalid_platform"))

if __name__ == '__main__':
    unittest.main()
