import uuid
from src.tools.news_fetcher import fetch_news
from src.utils.text_splitter import get_splitter
from src.utils.vector_store import (
    get_vector_store, 
    add_embeddings_to_store,
    query_similar
)
from src.chains.embedding_chains import embed_article
from src.chains.rag_chains import answer_with_rag
from src.agents.analyst_agent import generate_structured_report
from src.cleaning.cleaner import clean_article


class Pipeline:
    def __init__(self, collection_name="news_collection"):
        self.collection_name = collection_name
        self.client = get_vector_store()

    def run(self, query: str):
        """
        Full pipeline:
        1. Fetch news
        2. Clean text
        3. Split into chunks
        4. Embed chunks
        5. Store embeddings
        6. Perform RAG analysis
        7. Generate structured final report
        """

        # ----------------------------------------
        # 1. Fetch fresh news
        # ----------------------------------------
        articles = fetch_news(query)
        if not articles:
            return {
                "error": "No news articles found.",
                "query": query
            }

        # ----------------------------------------
        # 2. Clean and process text
        # ----------------------------------------
        splitter = get_splitter()
        embedded_data = []

        for article in articles:
            cleaned_text = clean_article(article)

            if not cleaned_text:
                continue

            # Split into chunks
            chunks = splitter.split_text(cleaned_text)

            # Embed each chunk
            for chunk in chunks:
                embed_result = embed_article({"content": chunk})

                for item in embed_result:
                    embedded_data.append({
                        "id": str(uuid.uuid4()),
                        "text": item["text"],
                        "embedding": item["embedding"]
                    })

        # ----------------------------------------
        # 3. Store in Vector DB
        # ----------------------------------------
        if embedded_data:
            add_embeddings_to_store(self.client, self.collection_name, embedded_data)

        # ----------------------------------------
        # 4. Run RAG for insights
        # ----------------------------------------
        rag_answer = answer_with_rag(
            f"Summarize key insights from the latest news about {query}.",
            self.collection_name
        )

        # ----------------------------------------
        # 5. Generate structured final report
        # ----------------------------------------
        final_report = generate_structured_report(
            query=query,
            rag_summary=rag_answer
        )

        return {
            "query": query,
            "articles_processed": len(articles),
            "rag_summary": rag_answer,
            "final_report": final_report
        }
