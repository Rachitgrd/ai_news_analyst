from src.reporting.article_formatter import format_top_articles

class ReportAgent:
    def __init__(self, title: str = "Daily AI News Report"):
        self.title = title

    def generate_markdown(self, analysis: dict) -> str:
        """
        Converts structured analysis into a polished Markdown report.
        """

        report = f"# 📰 {self.title}\n\n"

        if not analysis:
            return report + "No news available today."

        for cluster_id, data in analysis.items():
            topic = data["topic"]
            summary = data["summary"]
            sentiment = data["sentiment"]
            bias = data["bias"]
            metadatas = data["metadatas"]

            report += f"## 🔹 Topic: **{topic}**\n"

            # Sentiment
            sentiment_line = f"{sentiment['sentiment'].capitalize()} ({sentiment['score']})"
            report += f"**Sentiment:** {sentiment_line}\n\n"

            # Bias
            bias_line = f"{bias['bias'].capitalize()} ({bias['confidence']})"
            report += f"**Bias:** {bias_line}\n\n"

            # Summary
            report += f"**Summary:**\n{summary}\n\n"

            # Articles
            top_articles = format_top_articles(metadatas)
            report += f"**Top Articles:**\n{top_articles}\n"

            report += "---\n\n"

        return report
