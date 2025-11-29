import re

def clean_article(text: str) -> str:
    if not text:
        return ""

    # remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove unwanted symbols
    text = re.sub(r"[^\w\s.,!?-]", "", text)

    return text.strip()
