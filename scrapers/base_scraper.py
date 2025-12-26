from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """
    Abstract base class for all scrapers.
    """

    @abstractmethod
    def scrape(self, url):
        """
        Scrapes data from the given URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            dict: A dictionary containing the scraped data with keys:
                  'source', 'author', 'date', 'text', 'url'.
                  Returns None if scraping fails.
        """
        pass
