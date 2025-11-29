import chromadb

def get_vector_store():
    client = chromadb.PersistentClient(path="src/utils/chroma_db")
    return client

def add_embeddings_to_store(client, collection_name: str, embedded_data: list):
    # Use embedding_function=None to prevent Chroma from using default SentenceTransformer
    # and to allow any dimension (we provide embeddings manually)
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"}) # Note: Chroma might still default if not None. 
    # Actually, passing None might not work as expected in all versions, but let's try.
    # Better: don't rely on None, but if we provide embeddings in add(), it should work.
    # The issue was likely the collection was created with default before.
    # But to be safe, let's try to force it to accept our data.
    
    # If we want to be sure, we can pass a dummy function or just rely on the fact that we cleared the DB.
    # Let's stick to the previous code but ensure we pass embeddings.
    
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    
    ids = []
    texts = []
    metadatas = []
    embeddings = []

    for i, data in enumerate(embedded_data):
        ids.append(f"id_{collection_name}_{i}")
        texts.append(data["text"])
        metadatas.append(data["metadata"])
        embeddings.append(data["embedding"])
        
    if ids:
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )

    return collection

def query_similar(client, collection_name: str, query_embedding: list, top_k: int = 5):
    collection = client.get_or_create_collection(name=collection_name)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )   
    return results