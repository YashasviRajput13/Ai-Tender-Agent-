# agents.py — TenderIQ: All 5 AI Agents (FREE via Groq + Llama)

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"  # Free, fast, great at JSON


def call_agent(system_prompt, user_message):
    """Call Groq's free Llama model and return parsed JSON."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
    )
    raw = response.choices[0].message.content.strip()

    # Remove markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0].strip()

    # Try direct JSON parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Extract JSON object from any surrounding text
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(raw[start:end])
        raise ValueError(f"Could not parse JSON:\n{raw[:300]}")


# ─────────────────────────────────────────────────────────────────
# AGENT 1 — TENDER ANALYZER
# ─────────────────────────────────────────────────────────────────
TENDER_ANALYZER_PROMPT = """
You are TenderIQ's Tender Analysis Agent.
Analyze the tender and return ONLY a valid JSON object.
No markdown, no explanation, no extra text — just the JSON.
{
  "title": "string",
  "client": "string",
  "budget": "string",
  "deadline": "YYYY-MM-DD",
  "required_skills": ["skill1", "skill2"],
  "summary": "2-3 sentence executive summary",
  "complexity": "Low or Medium or High",
  "estimated_effort": "X person-months",
  "key_requirements": ["req1", "req2", "req3"],
  "red_flags": ["any concern"],
  "recommended_team_size": 6,
  "win_probability_factors": ["factor1", "factor2"]
}
""".strip()

def analyze_tender(tender: dict) -> dict:
    return call_agent(
        TENDER_ANALYZER_PROMPT,
        f"Analyze this tender:\n{json.dumps(tender, indent=2)}"
    )


# ─────────────────────────────────────────────────────────────────
# AGENT 2 — MATCHING AGENT
# ─────────────────────────────────────────────────────────────────
MATCHING_AGENT_PROMPT = """
You are TenderIQ's Smart Matching Agent.
Score vendor-tender compatibility and return ONLY a valid JSON object.
No markdown, no explanation, no extra text — just the JSON.
{
  "match_score": 85,
  "skill_score": 90,
  "budget_score": 80,
  "experience_score": 85,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill3"],
  "budget_compatible": true,
  "experience_fit": "Strong or Moderate or Weak",
  "recommendation": "Highly Recommended or Recommended or Consider or Not Recommended",
  "explanation": "2 sentence explanation of the match",
  "strengths": ["strength1", "strength2"],
  "gaps": ["gap1"]
}
All scores must be integers between 0 and 100.
""".strip()

def match_vendor_to_tender(vendor: dict, tender: dict) -> dict:
    return call_agent(
        MATCHING_AGENT_PROMPT,
        f"Match this vendor to this tender.\n\nVENDOR:\n{json.dumps(vendor, indent=2)}\n\nTENDER:\n{json.dumps(tender, indent=2)}"
    )


# ─────────────────────────────────────────────────────────────────
# AGENT 3 — ELIGIBILITY CHECKER
# ─────────────────────────────────────────────────────────────────
ELIGIBILITY_PROMPT = """
You are TenderIQ's Eligibility Checker Agent.
Compare vendor capabilities against tender requirements.
Return ONLY a valid JSON object.
No markdown, no explanation, no extra text — just the JSON.
{
  "eligible": true,
  "eligibility_score": 82,
  "verdict": "Fully Eligible or Conditionally Eligible or Not Eligible",
  "met_requirements": ["req1", "req2"],
  "missing_requirements": ["req3"],
  "partially_met": ["req4"],
  "blocking_issues": [],
  "recommendations": ["action1", "action2"],
  "summary": "One sentence eligibility verdict"
}
""".strip()

def check_eligibility(vendor: dict, tender: dict) -> dict:
    return call_agent(
        ELIGIBILITY_PROMPT,
        f"Check eligibility.\n\nVENDOR:\n{json.dumps(vendor, indent=2)}\n\nTENDER:\n{json.dumps(tender, indent=2)}"
    )


# ─────────────────────────────────────────────────────────────────
# AGENT 4 — RISK ANALYSIS AGENT
# ─────────────────────────────────────────────────────────────────
RISK_PROMPT = """
You are TenderIQ's Risk Analysis Agent.
Analyze the tender for execution risks.
Return ONLY a valid JSON object.
No markdown, no explanation, no extra text — just the JSON.
{
  "overall_risk": "Low or Medium or High",
  "risk_score": 55,
  "budget_viability": "Adequate or Tight or Insufficient",
  "timeline_viability": "Realistic or Aggressive or Unrealistic",
  "risks": [
    {
      "category": "Budget or Timeline or Technical or Compliance or Scope",
      "level": "Low or Medium or High",
      "description": "specific risk description"
    }
  ],
  "mitigation_suggestions": ["suggestion1", "suggestion2"],
  "go_no_go": "Go or Proceed with Caution or No-Go",
  "go_no_go_rationale": "brief reason for the decision"
}
""".strip()

def analyze_risk(tender: dict) -> dict:
    return call_agent(
        RISK_PROMPT,
        f"Analyze all risks for this tender:\n{json.dumps(tender, indent=2)}"
    )


# ─────────────────────────────────────────────────────────────────
# AGENT 5 — BID GENERATOR
# ─────────────────────────────────────────────────────────────────
BID_PROMPT = """
You are TenderIQ's Bid Generation Agent.
Write a professional government tender bid proposal.
Return ONLY a valid JSON object.
No markdown, no explanation, no extra text — just the JSON.
{
  "executive_summary": "3 compelling sentences about why this vendor wins",
  "value_proposition": "one unique positioning statement",
  "cover_letter_opening": "professional opening paragraph",
  "technical_approach": "3-4 sentence methodology description",
  "methodology": [
    "Phase 1: Discovery and Requirements (Weeks 1-3)",
    "Phase 2: Architecture and Design (Weeks 4-7)",
    "Phase 3: Development Sprints (Weeks 8-28)",
    "Phase 4: Testing and UAT (Weeks 29-34)",
    "Phase 5: Deployment and Handover (Weeks 35-40)"
  ],
  "team_composition": [
    {"role": "Project Manager",   "count": 1, "experience": "10+ years"},
    {"role": "Solution Architect","count": 1, "experience": "8+ years"},
    {"role": "Senior Developer",  "count": 3, "experience": "5+ years"},
    {"role": "QA Engineer",       "count": 2, "experience": "4+ years"}
  ],
  "timeline_overview": "high-level delivery timeline description",
  "competitive_advantages": ["advantage1", "advantage2", "advantage3"],
  "cost_breakdown": {
    "development": "55%",
    "testing": "15%",
    "deployment": "15%",
    "support": "10%",
    "contingency": "5%"
  }
}
""".strip()

def generate_bid(vendor: dict, tender: dict) -> dict:
    return call_agent(
        BID_PROMPT,
        f"Generate a winning bid.\n\nVENDOR:\n{json.dumps(vendor, indent=2)}\n\nTENDER:\n{json.dumps(tender, indent=2)}"
    )