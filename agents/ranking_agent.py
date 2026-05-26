from typing import Dict, List

class RankingAgent:
    def rank_opportunities(self, opportunities: List[Dict[str, object]], profile: Dict[str, object]) -> List[Dict[str, object]]:
        ranked = []
        for item in opportunities:
            match_score = item.get("match_score", 0)
            risk = item.get("risk_score", 0)
            score = float(match_score) - float(risk) * 0.4
            ranked.append({**item, "rank_score": round(score, 2)})
        return sorted(ranked, key=lambda row: row["rank_score"], reverse=True)

    def sort_by_revenue(self, opportunities: List[Dict[str, object]]) -> List[Dict[str, object]]:
        return sorted(opportunities, key=lambda row: float(row.get("value", 0)), reverse=True)
