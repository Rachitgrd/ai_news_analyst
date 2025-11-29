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

def label_topic(cluster_texts: list) -> str:
    """
    Given a list of chunk texts belonging to one cluster,
    returns a clean topic label like: 'AI Regulation and Policy'
    """

    if not cluster_texts:
        return "Unknown Topic"

    model = _get_model()

    
    sample = "\n\n".join(cluster_texts[:5])

    prompt = f"""
    You are a news categorization expert.
    Based on the following content, generate a short, clear topic label.

    Rules:
    - Maximum 5 words
    - No sentences
    - No full stops
    - Be specific, not generic
    - Should read like a news category

    Text Samples:
    \"\"\"{sample}\"\"\"

    Return ONLY the topic name. No explanation.
    """

    response = model.invoke(prompt)

    return response.content.strip()
