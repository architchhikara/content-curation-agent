import os
import tweepy
import re
from dotenv import load_dotenv
from .base_scraper import BaseScraper

load_dotenv()

class TwitterScraper(BaseScraper):
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        self.client = None

        # Prefer Bearer Token for v2 API (Free/Basic tiers often use v2)
        if self.bearer_token:
             self.client = tweepy.Client(bearer_token=self.bearer_token)
        elif self.api_key and self.api_secret:
             self.client = tweepy.Client(
                 consumer_key=self.api_key,
                 consumer_secret=self.api_secret,
                 access_token=self.access_token,
                 access_token_secret=self.access_token_secret
             )

    def extract_tweet_id(self, url):
        """Extracts the tweet ID from a Twitter/X URL."""
        # Example: https://twitter.com/user/status/1234567890
        # Example: https://x.com/user/status/1234567890
        pattern = r"status\/(\d+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    def scrape(self, url):
        if not self.client:
            print("Error: Twitter API credentials not found in environment variables.")
            return None

        tweet_id = self.extract_tweet_id(url)
        if not tweet_id:
            print(f"Error: Could not extract Tweet ID from {url}")
            return None

        try:
            # Fetch tweet with specific fields
            response = self.client.get_tweet(
                id=tweet_id,
                tweet_fields=["created_at", "author_id", "text"]
            )

            if not response.data:
                print(f"Error: Tweet not found or inaccessible (ID: {tweet_id})")
                return None

            tweet = response.data
            text = tweet.text
            date = str(tweet.created_at)

            # To get author name, we need to expand author_id, but that costs more requests/complexity.
            # We will use author_id as a fallback or try to fetch user if possible.
            # For Basic tier, getting tweet usually includes basic info.
            # To be efficient, we might just store the Author ID or try to fetch user details.
            # Let's try to fetch user details separately if needed, but for now, Author ID is safe.
            author = f"ID: {tweet.author_id}"

            # If we want the username, we can try:
            try:
                user_response = self.client.get_user(id=tweet.author_id)
                if user_response.data:
                    author = f"{user_response.data.name} (@{user_response.data.username})"
            except Exception:
                pass # Fallback to ID if user fetch fails

            return {
                "source": "X (Twitter)",
                "author": author,
                "date": date,
                "text": text,
                "url": url
            }

        except Exception as e:
            print(f"Error scraping Twitter URL {url}: {e}")
            return None
