import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

def summarize_cluster(topic_name: str, cluster_texts: list) -> str:
    """
    Produces a concise multi-article summary for a cluster.
    """

    if not cluster_texts:
        return "No data available for this topic."

    model = _get_model()

    # Use only first ~10 chunks to avoid extreme prompt size
    sample_text = "\n\n".join(cluster_texts[:10])

    prompt = f"""
    You are an expert news analyst.
    Summarize the following cluster of news articles under the topic: "{topic_name}".

    Rules:
    - Use only the given text
    - No invented facts
    - Provide 4-6 bullet points
    - Each bullet point should be specific and actionable
    - Maintain a professional journalistic tone

    Text:
    \"\"\"{sample_text}\"\"\"

    Provide the final output ONLY as bullet points. No extra narration.
    """

    response = model.invoke(prompt)
    return response.content.strip()
