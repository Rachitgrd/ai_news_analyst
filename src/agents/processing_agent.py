from src.utils.cleaner import clean_article
from src.utils.text_splitter import get_splitter
from src.chains.embedding_chains import embed_article

class ProcessingAgent:
    def __init__(self):
        self.splitter = get_splitter()

    def process_articles(self, articles: list) -> list:
        """
        Takes raw articles, cleans them, splits them into chunks,
        embeds each chunk, and returns a list of embedded data.
        """

        processed_embeddings = []

        for article in articles:
            try:
                cleaned = clean_article(article)

                if not cleaned:
                    print("[ProcessingAgent] Skipping empty/invalid article.")
                    continue

                # Embedding logic already handles splitting internally
                embeddings = embed_article(article)

                if embeddings:
                    processed_embeddings.extend(embeddings)
                    print(f"[ProcessingAgent] Processed {len(embeddings)} chunks.")
                else:
                    print("[ProcessingAgent] No embeddings produced.")

            except Exception as e:
                print(f"[ProcessingAgent] Error processing article: {e}")

        print(f"[ProcessingAgent] Total embedded chunks: {len(processed_embeddings)}")
        return processed_embeddings
