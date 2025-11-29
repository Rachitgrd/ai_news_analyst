from fastapi import FastAPI
from pydantic import BaseModel

from src.tools.news_fetcher import fetch_news
from src.pipeline.run_pipeline import Pipeline
from src.chains.rag_chains import answer_with_rag
from src.analysis.sentiment_chain import analyze_sentiment  # keep or replace placeholder


app = FastAPI(
    title="AI News Analyst",
    description="Automatic news fetching, processing, and RAG-based reporting.",
    version="1.0.0",
)

# ---------------------------------------------------
# Request Models
# ---------------------------------------------------

class AnalyzeRequest(BaseModel):
    query: str

class RAGQuery(BaseModel):
    question: str

class SentimentRequest(BaseModel):
    text: str


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get("/")
def health():
    return {"status": "running", "message": "AI News Analyst API is active."}


# ---------------------------------------------------
# Fetch News
# ---------------------------------------------------

@app.get("/fetch-news")
def fetch_news_endpoint(query: str):
    articles = fetch_news(query)
    return {
        "query": query,
        "count": len(articles),
        "articles": articles
    }


# ---------------------------------------------------
# Full Pipeline Analysis
# ---------------------------------------------------

@app.post("/analyze")
def analyze_endpoint(payload: AnalyzeRequest):
    pipeline = Pipeline()
    report = pipeline.run(payload.query)
    return {
        "query": payload.query,
        "report": report
    }


# ---------------------------------------------------
# RAG Search (Ask Questions From Stored News)
# ---------------------------------------------------

@app.get("/search")
def rag_search_endpoint(question: str):
    answer = answer_with_rag(question, "news_collection")
    return {
        "question": question,
        "answer": answer
    }


# ---------------------------------------------------
# Summaries Endpoint (Recent Digests)
# ---------------------------------------------------

@app.get("/summaries")
def summaries_endpoint():
    # Placeholder until you implement summaries
    return {
        "status": "ok",
        "message": "Summary endpoint active. Implement logic to return latest article summaries."
    }


# ---------------------------------------------------
# Sentiment Endpoint (Optional)
# ---------------------------------------------------

@app.post("/sentiment")
def sentiment_endpoint(payload: SentimentRequest):
    result = analyze_sentiment(payload.text)
    return {
        "text": payload.text,
        "sentiment": result
    }
