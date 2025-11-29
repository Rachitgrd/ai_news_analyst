from langchain_google_genai import ChatGoogleGenerativeAI


def generate_structured_report(query: str, rag_summary: str):
    """
    Takes the RAG output and generates a structured analysis report.

    Output format:
    {
        "summary": "...",
        "key_points": [...],
        "risk_factors": [...],
        "opportunities": [...],
        "sentiment": "Positive | Neutral | Negative"
    }
    """

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2
    )

    prompt = f"""
    You are an AI News Analyst.

    Topic: {query}

    Use the following summarized insights:
    {rag_summary}

    Generate a clean structured report in JSON with the following fields:
    - summary: A short summary.
    - key_points: 4–6 main bullet points.
    - risk_factors: Any risks mentioned in the articles.
    - opportunities: Any positive opportunities mentioned.
    - sentiment: Overall sentiment (Positive, Neutral, Negative).

    Ensure the final output is pure JSON with no explanations.
    """

    response = model.invoke(prompt)
    return response.content
