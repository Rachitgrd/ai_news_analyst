import sys
import os
import shutil

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chains.embedding_chains import embed_article
from src.utils.vector_store import get_vector_store, add_embeddings_to_store
from src.chains.rag_chains import answer_with_rag

def test_rag_flow():
    print("Testing RAG Flow...")
    
    # 1. Prepare dummy data
    articles = [
        {
            "title": "Gemini 1.5 Pro Released",
            "description": "Google releases Gemini 1.5 Pro with 1M context window.",
            "content": "Google has announced Gemini 1.5 Pro. It features a massive 1 million token context window, allowing it to process vast amounts of information. It outperforms previous models in many benchmarks.",
            "url": "http://google.com/news",
            "publishedAt": "2024-02-15",
            "source": {"name": "Google Blog"}
        },
        {
            "title": "Python 3.13 Features",
            "description": "New features in Python 3.13 include JIT compiler.",
            "content": "Python 3.13 is expected to introduce a JIT compiler to improve performance. It also removes the GIL in experimental builds.",
            "url": "http://python.org/news",
            "publishedAt": "2024-03-10",
            "source": {"name": "Python.org"}
        }
    ]
    
    collection_name = "test_rag_collection"
    
    # 2. Embed articles
    print("Embedding articles...")
    all_embedded_data = []
    for article in articles:
        embedded = embed_article(article)
        all_embedded_data.extend(embedded)
    
    print(f"Generated {len(all_embedded_data)} chunks.")
    if all_embedded_data:
        print(f"Embedding dimension: {len(all_embedded_data[0]['embedding'])}")
    
    # 3. Store in Vector DB
    print("Storing in Vector DB...")
    client = get_vector_store()
    # Clean up previous test collection if exists
    try:
        client.delete_collection(collection_name)
    except:
        pass
        
    collection = add_embeddings_to_store(client, collection_name, all_embedded_data)
    print(f"Stored in collection: {collection_name}")
    
    # 4. Query / RAG
    question = "What is the context window of Gemini 1.5 Pro?"
    print(f"\nQuestion: {question}")
    
    answer = answer_with_rag(question, collection_name)
    print(f"Answer: {answer}")
    
    assert "1 million" in answer or "1M" in answer or "1000000" in answer
    
    question2 = "What is new in Python 3.13?"
    print(f"\nQuestion: {question2}")
    answer2 = answer_with_rag(question2, collection_name)
    print(f"Answer: {answer2}")
    
    assert "JIT" in answer2
    
    print("\nRAG Test Passed!")

if __name__ == "__main__":
    test_rag_flow()
