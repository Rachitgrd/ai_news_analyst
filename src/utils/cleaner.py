import re

def clean_article(article_dict):
    if not article_dict:
        return ""

    title = article_dict.get("title") or ""
    description = article_dict.get("description") or ""
    content = article_dict.get("content") or ""

    # Remove NewsAPI truncated content marker
    content = re.sub(r"\[\+\d+\schars\]", "", content)

    # Avoid duplicate description
    if description and content and description in content:
        description = ""

    parts = [title, description, content]
    unique_parts = []
    seen = ""

    for part in parts:
        if part and part not in seen:
            unique_parts.append(part)
            seen += part + " "

    full_text = " ".join(unique_parts)

    # Safer clean
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'\"()/-]", "", full_text)

    # Normalize spaces
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text
