import json
import os
from typing import Any

import httpx


OPENROUTER_API_URL = os.getenv(
    "OPENROUTER_API_URL",
    "https://api.openrouter.ai/v1/chat/completions",
)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")
MAX_INPUT_LENGTH = 22000


def fallback_analysis(text: str) -> dict[str, Any]:
    return {
        "summary": text[:300] if text else "No text available.",
        "eligibility": ["Review qualification requirements manually."],
        "required_documents": ["Bid security", "Company profile", "Project plan"],
        "technical_requirements": ["Review the technical specifications in the tender document."],
        "risk_factors": ["Limited submission window", "Incomplete documentation risk"],
        "risk_level": "medium",
        "risk_reasons": ["Limited information", "Standard procurement risk"],
        "category": "General Procurement",
        "deadline": "",
        "budget": "",
        "confidence_score": 0.0,
    }


async def analyze_tender_text(text: str) -> dict[str, Any]:
    if not OPENROUTER_API_KEY:
        return fallback_analysis(text)

    trimmed_text = text[:MAX_INPUT_LENGTH]
    prompt = (
        "You are a procurement intelligence assistant. "
        "Analyze the following tender document text and return a JSON object with exactly these fields: "
        "summary, eligibility, required_documents, technical_requirements, risk_factors, recommendation, risk_level, risk_reasons, category, deadline, budget, confidence_score, match_score, success_probability. "
        "Return only valid JSON with array values for eligibility, required_documents, technical_requirements, risk_factors, and risk_reasons."
        f"\n\nTEXT:\n{trimmed_text}"
    )
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You produce structured JSON for tender analysis."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 1000,
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(OPENROUTER_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
    except Exception:
        return fallback_analysis(text)

    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not content:
        return fallback_analysis(text)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(content[start : end + 1])
            except json.JSONDecodeError:
                pass
        return fallback_analysis(text)
