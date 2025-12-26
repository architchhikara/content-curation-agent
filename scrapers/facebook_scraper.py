import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from utils.helpers import get_random_user_agent

class FacebookScraper(BaseScraper):
    def scrape(self, url):
        """
        Scrapes Facebook public post using OpenGraph metadata.
        This is the "Non-Login" approach.
        """
        try:
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Error: Facebook request failed with status {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract Open Graph tags
            title = soup.find("meta", property="og:title")
            description = soup.find("meta", property="og:description")

            # For FB, og:title is often the author or post summary,
            # and og:description contains the snippet of the post text.

            text_content = ""
            if title:
                text_content += f"Title: {title.get('content', '')}\n"
            if description:
                text_content += f"Description: {description.get('content', '')}"

            # It's hard to get exact author/date from OG tags reliably across all FB post types
            # without complex parsing. We will use available metadata.

            return {
                "source": "Facebook",
                "author": "Unknown (Public Metadata)", # Hard to parse reliably without login/API
                "date": "Unknown", # OG tags usually don't have date
                "text": text_content,
                "url": url
            }

        except Exception as e:
            print(f"Error scraping Facebook URL {url}: {e}")
            return None
