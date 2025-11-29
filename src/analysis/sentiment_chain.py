def analyze_sentiment(text: str) -> dict:
    if not text:
        return {"sentiment": "neutral", "score": 0.0}

    text_lower = text.lower()

    if any(word in text_lower for word in ["good", "great", "excellent", "positive"]):
        return {"sentiment": "positive", "score": 0.9}

    if any(word in text_lower for word in ["bad", "terrible", "poor", "negative"]):
        return {"sentiment": "negative", "score": -0.8}

    return {"sentiment": "neutral", "score": 0.0}
