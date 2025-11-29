from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.vector_store import query_similar
import os

class FactCheckAgent:
    def __init__(self, k: int = 3):
        self.k = k
        self.model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.1
        )

    def extract_claims(self, text: str) -> list:
        """
        Uses Gemini to extract key factual claims from a summary.
        """
        prompt = f"""
        Extract the main factual claims from this text:

        \"\"\"{text}\"\"\"

        Return ONLY a JSON list of short claims.
        """

        response = self.model.invoke(prompt).content.strip()
        import json

        try:
            return json.loads(response)
        except:
            return []

    def verify_claim(self, claim: str, collection_name: str) -> dict:
        """
        Checks if a single claim is supported by retrieved evidence.
        """

        # Retrieve evidence from embeddings
        results = query_similar(claim, collection_name, top_k=self.k)

        evidence = "\n".join(r["text"] for r in results)

        prompt = f"""
        Based ONLY on the evidence below, determine whether the claim is supported.

        Claim:
        {claim}

        Evidence:
        \"\"\"{evidence}\"\"\"

        Respond strictly in JSON:
        {{
            "status": "supported" | "contradicted" | "insufficient",
            "explanation": "short explanation based only on evidence provided"
        }}
        """

        response = self.model.invoke(prompt).content.strip()

        import json
        try:
            return json.loads(response)
        except:
            return {
                "status": "insufficient",
                "explanation": "Unable to parse verification."
            }

    def verify_summary(self, summary_text: str, collection_name: str) -> dict:
        """
        Full fact-checking pipeline:
        - extract claims
        - verify each claim
        """
        claims = self.extract_claims(summary_text)
        results = {}

        for claim in claims:
            results[claim] = self.verify_claim(claim, collection_name)

        return results
