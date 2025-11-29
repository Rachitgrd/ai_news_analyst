import dotenv
dotenv.load_dotenv()

import os
import requests

api_key = os.getenv("NEWS_API_KEY")

def fetch_news(query: str, language = "en", page_size = 20):
    if not api_key:
        print("Error: news_api_key not found in environment variables.")
        return []

    url = f"https://newsapi.org/v2/everything?"
    params = {
    "q": query,
    "language": language,
    "pageSize": page_size,
    "sortBy": "publishedAt",
    "apiKey": api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return articles
    else:
        print(f"Error: {response.status_code}")
        return []

