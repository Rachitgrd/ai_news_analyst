from src.analysis.topic_labeling import label_topic
from src.analysis.cluster_summary import summarize_cluster
from src.analysis.sentiment_chain import analyze_sentiment
from src.analysis.bias_chain import analyze_bias
from src.reporting.article_formatter import format_top_articles


def generate_daily_report(clusters: dict) -> str:
    """
    Generates a full markdown daily report from the cluster dictionary.
    clusters: {
        cluster_id: {
            "texts": [...],
            "metadatas": [...],
            "centroid": [...]
        }
    }
    """

    report = "# 📰 Daily AI News Report\n\n"

    if not clusters:
        return report + "No news available for analysis today."

    for cluster_id, cluster_data in clusters.items():
        texts = cluster_data["texts"]

        # 1. Topic Label
        topic_name = label_topic(texts)

        # 2. Summary
        summary = summarize_cluster(topic_name, texts)

        # 3. Sentiment
        sentiment_data = analyze_sentiment(" ".join(texts[:5]))
        sentiment = sentiment_data.get("sentiment")
        score = sentiment_data.get("score")
        sentiment_line = f"{sentiment.capitalize()} ({score})"

        # 4. Bias
        bias_data = analyze_bias(" ".join(texts[:5]))
        bias = bias_data.get("bias")
        confidence = bias_data.get("confidence")
        bias_line = f"{bias.capitalize()} ({confidence})"

        # 5. Build Section
        report += f"## 🔹 Topic: **{topic_name}**\n"
        report += f"**Sentiment:** {sentiment_line}\n\n"
        report += f"**Bias:** {bias_line}\n\n"
        report += f"**Summary:**\n{summary}\n\n"
        report += "---\n\n"

    return report
