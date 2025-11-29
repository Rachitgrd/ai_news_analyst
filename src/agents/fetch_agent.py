import time
from src.tools.news_fetcher import fetch_news

class FetchAgent:
    def __init__(self, retries: int = 3, delay: int = 2):
        self.retries = retries
        self.delay = delay

    def fetch(self, query: str):
        """
        Fetches news with retry logic and basic validation.
        Returns a list of article dicts.
        """

        for attempt in range(1, self.retries + 1):
            try:
                articles = fetch_news(query)

                if not articles:
                    print(f"[FetchAgent] No articles received. Attempt {attempt}/{self.retries}")
                else:
                    print(f"[FetchAgent] Fetched {len(articles)} articles.")
                    return articles

            except Exception as e:
                print(f"[FetchAgent] Error: {e}. Attempt {attempt}/{self.retries}")

            time.sleep(self.delay)

        print("[FetchAgent] Failed to fetch after retries.")
        return []
