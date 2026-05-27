# run_agents.py — Run and display all 5 TenderIQ agents

import json
from agents import (
    analyze_tender,
    match_vendor_to_tender,
    check_eligibility,
    analyze_risk,
    generate_bid,
)

# ── Sample Data ───────────────────────────────────────────────────
TENDER = {
    "id": "TND-001",
    "title": "Smart City IoT Infrastructure",
    "client": "Ministry of Urban Development",
    "budget": "$2,500,000",
    "deadline": "2026-09-15",
    "required_skills": ["IoT", "Cloud Architecture", "React.js", "5G", "Python"],
    "category": "Technology",
    "location": "New Delhi, India",
    "duration": "18 months",
    "description": (
        "Deploy comprehensive IoT infrastructure across 50 smart city nodes. "
        "Includes sensors, edge computing, real-time dashboards, "
        "and a predictive analytics engine."
    ),
}

VENDOR = {
    "id": "VND-001",
    "company_name": "TechVision Solutions",
    "description": "Premier IoT and cloud infrastructure firm.",
    "skills": ["IoT", "Cloud Architecture", "React.js", "Python", "Data Analytics"],
    "experience_years": 8,
    "location": "New Delhi",
    "budget_min": 500000,
    "budget_max": 3000000,
    "certifications": ["ISO 27001", "AWS Professional", "GCP Certified"],
    "past_projects": 24,
    "rating": 4.8,
}


def print_result(agent_name, result):
    """Pretty-print agent output with a header."""
    print("\n" + "=" * 60)
    print(f"  🤖  {agent_name}")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    print()


def run_all_agents():
    print("\n🚀 TenderIQ — Running All 5 AI Agents\n")
    print(f"   Tender : {TENDER['title']}")
    print(f"   Vendor : {VENDOR['company_name']}")
    print(f"   Budget : {TENDER['budget']}")
    print()

    # ── Agent 1: Tender Analyzer ──────────────────────────────────
    print("⏳ Running Agent 1: Tender Analyzer...")
    try:
        result = analyze_tender(TENDER)
        print_result("AGENT 1 — Tender Analyzer (Module 2)", result)
    except Exception as e:
        print(f"❌ Tender Analyzer failed: {e}\n")

    # ── Agent 2: Matching ─────────────────────────────────────────
    print("⏳ Running Agent 2: Matching Engine...")
    try:
        result = match_vendor_to_tender(VENDOR, TENDER)
        print_result("AGENT 2 — Smart Matching Engine (Module 4)", result)
        score = result.get("match_score", 0)
        print(f"   💡 Match Score: {score}% — {result.get('recommendation', '')}")
    except Exception as e:
        print(f"❌ Matching Agent failed: {e}\n")

    # ── Agent 3: Eligibility ──────────────────────────────────────
    print("⏳ Running Agent 3: Eligibility Checker...")
    try:
        result = check_eligibility(VENDOR, TENDER)
        print_result("AGENT 3 — Eligibility Checker (Module 5)", result)
        verdict = result.get("verdict", "Unknown")
        eligible = result.get("eligible", False)
        icon = "✅" if eligible else "❌"
        print(f"   {icon} Verdict: {verdict}")
    except Exception as e:
        print(f"❌ Eligibility Agent failed: {e}\n")

    # ── Agent 4: Risk Analysis ────────────────────────────────────
    print("⏳ Running Agent 4: Risk Analyzer...")
    try:
        result = analyze_risk(TENDER)
        print_result("AGENT 4 — Risk Analysis Agent (Module 7)", result)
        risk = result.get("overall_risk", "Unknown")
        gng = result.get("go_no_go", "Unknown")
        print(f"   ⚠️  Risk Level: {risk}  |  Decision: {gng}")
    except Exception as e:
        print(f"❌ Risk Agent failed: {e}\n")

    # ── Agent 5: Bid Generator ────────────────────────────────────
    print("⏳ Running Agent 5: Bid Generator...")
    try:
        result = generate_bid(VENDOR, TENDER)
        print_result("AGENT 5 — Bid Generator (Module 6)", result)
        print(f"   📝 Executive Summary: {result.get('executive_summary', '')[:120]}...")
    except Exception as e:
        print(f"❌ Bid Generator failed: {e}\n")

    print("\n" + "=" * 60)
    print("  ✅  All agents completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_agents()