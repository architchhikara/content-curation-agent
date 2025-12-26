from urllib.parse import urlparse
from .youtube_scraper import YoutubeScraper
from .twitter_scraper import TwitterScraper
from .instagram_scraper import InstagramScraper
from .facebook_scraper import FacebookScraper
from .linkedin_scraper import LinkedinScraper

def get_scraper_for_url(url):
    """
    Factory function to return the correct scraper instance based on the URL domain.
    """
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
