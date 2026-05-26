import re
from typing import Dict, Optional


def match_text_score(reference: str, target: str) -> float:
    if not reference or not target:
        return 0.0
    tokens = set(re.findall(r"\w+", reference.lower()))
    matches = [token for token in tokens if token in target.lower()]
    return min(1.0, len(matches) / max(1, len(tokens))) * 100.0


def score_tender_against_company(company: dict[str, str], tender: dict[str, str], analysis: Optional[dict[str, any]] = None) -> dict[str, float]:
    company_profile = " ".join([str(company.get(key, "")) for key in ["profile", "sector", "location"]])
    tender_text = " ".join([str(tender.get(key, "")) for key in ["title", "description", "authority", "category", "region"]])
    analysis_text = ""
    if analysis:
        analysis_text = " ".join(
            [
                str(analysis.get("summary", "")),
                " ".join(analysis.get("eligibility", []) or []),
                " ".join(analysis.get("required_documents", []) or []),
            ]
        )

    sector_score = match_text_score(company.get("sector", ""), tender.get("category", ""))
    location_score = match_text_score(company.get("location", ""), tender.get("region", ""))
    profile_score = match_text_score(company_profile, tender_text)
    eligibility_score = match_text_score(company_profile, analysis_text)

    match_score = round((sector_score * 0.2) + (location_score * 0.1) + (profile_score * 0.3) + (eligibility_score * 0.4), 2)
    relevance_score = round((profile_score + eligibility_score) / 2, 2)
    success_probability = round(min(100.0, match_score * 0.9 + relevance_score * 0.1), 2)

    return {
        "match_score": match_score,
        "relevance_score": relevance_score,
        "success_probability": success_probability,
    }
