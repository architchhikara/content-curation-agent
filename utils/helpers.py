import time
import random
from fake_useragent import UserAgent

def get_random_user_agent():
    """Returns a random user agent string."""
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        # Fallback if fake_useragent fails
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def random_sleep(min_seconds=5, max_seconds=15):
    """Sleeps for a random duration between min_seconds and max_seconds."""
    duration = random.uniform(min_seconds, max_seconds)
    print(f"Sleeping for {duration:.2f} seconds...")
    time.sleep(duration)
