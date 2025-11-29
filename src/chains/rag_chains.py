import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.vector_store import get_vector_store, query_similar

load_dotenv()


def _get_model():
    """
    Returns a Gemini chat model for answering questions.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2  
    )
    return model


def _build_context_from_results(results: dict) -> str:
    """
    Converts Chroma query results into a single context string.
    Expects results from query_similar().
    """
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

  
    docs_for_query = documents[0] if documents else []
    meta_for_query = metadatas[0] if metadatas else []

    context_blocks = []
    for doc, meta in zip(docs_for_query, meta_for_query):
        source = meta.get("source", "Unknown source")
        title = meta.get("title", "Untitled")
        published = meta.get("publishedAt", "Unknown date")
        url = meta.get("url", "")

        block = f"Title: {title}\nSource: {source}\nDate: {published}\nURL: {url}\nContent: {doc}"
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)
    return context


from src.utils.embedder import get_embedder

def answer_with_rag(question: str, collection_name: str, top_k: int = 5) -> str:
    """
    Uses RAG: retrieve relevant news chunks from Chroma and answer using Gemini.
    """
 
    client = get_vector_store()
    
    embedder = get_embedder()
    query_embedding = embedder.embed_query(question)

    results = query_similar(
        client=client,
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=top_k
    )

    context = _build_context_from_results(results)

    if not context:
        return "No relevant context found in the news database to answer this question."


    system_instructions = (
        "You are an AI news analyst. Use ONLY the given context to answer the question. "
        "If the answer is not clearly supported by the context, say you are not sure. "
        "Be concise, factual, and avoid speculation."
    )

    prompt = (
        f"{system_instructions}\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        f"Answer in 2–4 short paragraphs."
    )

 
    model = _get_model()
    response = model.invoke(prompt)


    return response.content
