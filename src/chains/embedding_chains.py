import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.utils.text_splitter import get_splitter
from src.utils.cleaner import clean_article

load_dotenv()

from src.utils.embedder import get_embedder

def embed_article(article_dict):
    """
    Cleans, splits, and embeds an article using Gemini embedding-001.
    Returns list of dicts: [{"text": chunk, "embedding": [...], "metadata": {...}}]
    """
    cleaned_text = clean_article(article_dict)
    if not cleaned_text:
        return []

    splitter = get_splitter()
    chunks = splitter.split_text(cleaned_text)

    # Gemini embedding model
    embedder = get_embedder()
  
    embedded_data = []
    for chunk in chunks:
        embedding = embedder.embed_query(chunk)
        embedded_data.append({
            "text": chunk,
            "embedding": embedding,
            "metadata": {
                "title": article_dict.get("title"),
                "source": article_dict.get("source", {}).get("name"),
                "publishedAt": article_dict.get("publishedAt"),
                "url": article_dict.get("url")
            }
        })

    return embedded_data
