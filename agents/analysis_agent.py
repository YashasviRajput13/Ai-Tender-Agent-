from typing import Dict, List

class AnalysisAgent:
    def summarize(self, tender_text: str) -> Dict[str, str]:
        return {
            "summary": tender_text[:220] + ("..." if len(tender_text) > 220 else ""),
            "insight": "Identified key requirements and compliance triggers.",
        }

    def score_tender(self, tender: Dict[str, object]) -> Dict[str, object]:
        requirements = tender.get("requirements", [])
        value = tender.get("value", 0)
        score = 0.6 + min(len(requirements) * 0.03, 0.25)
        if isinstance(value, (int, float)) and value > 1000000:
            score += 0.05
        return {
            "score": round(min(score, 0.99), 2),
            "risk_signals": ["timeline", "budget", "compliance"],
        }

    def create_embedding(self, content: str) -> List[float]:
        return [float(ord(c) % 10) / 10.0 for c in content[:64]]
