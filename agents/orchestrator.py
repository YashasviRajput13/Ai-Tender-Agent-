from typing import Dict, List

from .analysis_agent import AnalysisAgent
from .discovery_agent import DiscoveryAgent
from .ranking_agent import RankingAgent

class PDFProcessor:
    def process(self, pdf_url: str) -> dict:
        return {"pdf_url": pdf_url, "text": "Extracted text content", "metadata": {}}

class EligibilityEvaluator:
    def evaluate(self, requirements: List[str], profile: dict) -> dict:
        eligible = len(requirements) <= len(profile.get("certifications", []))
        return {"eligible": eligible, "reasons": ["Match count above threshold"]}

class RiskAssessor:
    def assess(self, tender_data: dict) -> dict:
        return {"risk_score": 0.45, "tags": ["medium", "timeline"]}

class MatchingEngine:
    def match(self, tender: dict, profile: dict) -> dict:
        return {"match_score": 0.82, "fit": "strong", "reasons": ["regional alignment", "budget fit"]}

class RecommendNotifier:
    def recommend(self, analysis: dict, eligibility: dict, match: dict) -> dict:
        return {
            "recommendation": "pursue" if eligibility["eligible"] and match["match_score"] > 0.7 else "review",
            "alerts": ["New tender recommendation created."],
        }

class Orchestrator:
    def __init__(self):
        self.discovery = DiscoveryAgent()
        self.analysis = AnalysisAgent()
        self.ranking = RankingAgent()
        self.pdf_processor = PDFProcessor()
        self.eligibility = EligibilityEvaluator()
        self.risk = RiskAssessor()
        self.matching = MatchingEngine()
        self.recommender = RecommendNotifier()

    def process_tender(self, tender_data: dict, profile: dict) -> dict:
        pdf_result = self.pdf_processor.process(tender_data.get("pdf_url", ""))
        analysis = self.analysis.score_tender({
            **tender_data,
            "requirements": tender_data.get("requirements", []),
        })
        eligibility = self.eligibility.evaluate(tender_data.get("requirements", []), profile)
        risk = self.risk.assess(tender_data)
        match = self.matching.match(tender_data, profile)
        recommendation = self.recommender.recommend(analysis, eligibility, match)
        return {
            "tender": tender_data,
            "pdf": pdf_result,
            "analysis": analysis,
            "eligibility": eligibility,
            "risk": risk,
            "match": match,
            "recommendation": recommendation,
        }

    def rank_opportunities(self, opportunities: List[dict], profile: dict) -> List[dict]:
        return self.ranking.rank_opportunities(opportunities, profile)

    def discover_and_process(self, sources: List[str]) -> List[dict]:
        discovery_results = self.discovery.discover_sources(sources)
        return [
            {"source": result["source"], "status": result["status"]}
            for result in discovery_results
        ]
