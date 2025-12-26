import unittest
import sys
import os

# Add root directory to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapers.youtube_scraper import YoutubeScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.facebook_scraper import FacebookScraper
from scrapers.linkedin_scraper import LinkedinScraper
from utils.sheets_handler import SheetsHandler
from utils.helpers import get_random_user_agent

class TestStructure(unittest.TestCase):
    def test_imports(self):
        """Test that all scraper classes can be imported and instantiated."""
        try:
            yt = YoutubeScraper()
            tw = TwitterScraper()
            ig = InstagramScraper()
            fb = FacebookScraper()
            li = LinkedinScraper()
            sh = SheetsHandler()
        except ImportError as e:
            self.fail(f"Import failed: {e}")
        except Exception as e:
            self.fail(f"Instantiation failed: {e}")

    def test_helpers(self):
        """Test helper functions."""
        ua = get_random_user_agent()
        self.assertIsInstance(ua, str)
        self.assertTrue(len(ua) > 0)

    def test_youtube_id_extraction(self):
        scraper = YoutubeScraper()
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(scraper.extract_video_id(url), "dQw4w9WgXcQ")

        url_short = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(scraper.extract_video_id(url_short), "dQw4w9WgXcQ")

    def test_twitter_id_extraction(self):
        scraper = TwitterScraper()
        url = "https://twitter.com/jack/status/20"
        self.assertEqual(scraper.extract_tweet_id(url), "20")

    def test_instagram_shortcode_extraction(self):
        scraper = InstagramScraper()
        url = "https://www.instagram.com/p/B_K4x5_j5-/"
        self.assertEqual(scraper.extract_shortcode(url), "B_K4x5_j5-")

if __name__ == '__main__':
    unittest.main()
