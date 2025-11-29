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
        temperature=0.1
    )


def analyze_bias(text: str) -> dict:
    """
    Detects political/editorial bias of news text.
    Returns a structured JSON dict:
    {
        "bias": "left" | "right" | "center",
        "confidence": float,
        "explanation": "..."
    }
    """
    if not text or len(text.strip()) == 0:
        return {
            "bias": "center",
            "confidence": 0.0,
            "explanation": "No content available."
        }

    model = _get_model()

    prompt = f"""
    You are a news media bias evaluator.
    Analyze the following news text and classify its political/editorial bias.

    Consider:
    - word choice
    - framing
    - tone
    - implied stance
    - emotional language
    - exaggeration vs. neutrality

    Text:
    \"\"\"{text}\"\"\"

    Return STRICTLY in JSON:
    {{
        "bias": "left" | "right" | "center",
        "confidence": float,
        "explanation": "short explanation"
    }}
    """

    response = model.invoke(prompt)

    import json
    try:
        return json.loads(response.content.strip())
    except:
        return {
            "bias": "center",
            "confidence": 0.0,
            "explanation": "Unable to parse bias."
        }
