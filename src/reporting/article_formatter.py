def format_top_articles(metadatas: list, limit: int = 5) -> str:
    """
    Takes metadata entries for one cluster and returns
    a clean markdown list of top articles.
    """

    if not metadatas:
        return "No articles available."

    # Remove duplicates by URL
    seen = set()
    clean_list = []

    for m in metadatas:
        url = m.get("url")
        if url and url not in seen:
            seen.add(url)
            clean_list.append(m)

    # Sort by published date (if available)
    try:
        clean_list.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
    except:
        pass

    # Limit results
    clean_list = clean_list[:limit]

    md = ""
    for idx, article in enumerate(clean_list, start=1):
        title = article.get("title", "Untitled")
        source = article.get("source", "Unknown Source")
        date = article.get("publishedAt", "Unknown Date")
        url = article.get("url", "#")

        md += f"{idx}. **{title}** — {source} ({date})\n"
        md += f"   [Read Article]({url})\n\n"

    return md
