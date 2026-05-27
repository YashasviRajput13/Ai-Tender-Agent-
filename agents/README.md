## 🤖 AI Agents — TenderIQ Intelligence Layer

> Built by [Your Name] · Powered by Groq (Llama 3.3 70B)

This module provides 5 AI agents that form the intelligence core of TenderIQ. Each agent is a focused LLM call that takes structured input and returns structured JSON — no hallucinated formats, no markdown, just clean data the frontend can render directly.

---

### Architecture overview

```
Tender / Vendor input
        │
        ▼
┌───────────────────────────────────────────────────────┐
│                    FastAPI Backend                    │
│                                                       │
│  Agent 1        Agent 2        Agent 3                │
│  Tender    →    Matching   →   Eligibility            │
│  Analyzer       Engine         Checker                │
│                                                       │
│  Agent 4        Agent 5                               │
│  Risk      →    Bid                                   │
│  Analyzer       Generator  (only if eligible + ≥60%) │
└───────────────────────────────────────────────────────┘
        │
        ▼
   JSON response → Frontend UI
```

The `/api/pipeline` endpoint runs Agents 1–4 in **parallel** (via `asyncio.gather`) then conditionally runs Agent 5, making the full pipeline ~4× faster than sequential calls.

---

### Agent 1 — Tender Analyzer

**Endpoint:** `POST /api/analyze`  
**Input:** tender details (title, client, budget, deadline, description)  
**What it does:** Reads a tender and extracts everything a vendor needs to decide whether to bid — required skills, complexity, effort estimate, red flags, and win probability factors.

**Output fields:**
| Field | Description |
|---|---|
| `summary` | 2–3 sentence executive summary |
| `complexity` | Low / Medium / High |
| `required_skills` | List of skills extracted from the tender |
| `estimated_effort` | Person-months estimate |
| `key_requirements` | Top requirements to meet |
| `red_flags` | Concerns worth noting before bidding |
| `recommended_team_size` | Suggested headcount |
| `win_probability_factors` | What would make a vendor win this |

---

### Agent 2 — Matching Engine

**Endpoint:** `POST /api/match`  
**Input:** vendor profile + tender details  
**What it does:** Scores how well a vendor matches a tender across three dimensions — skills, budget, and experience — and returns an overall match score with a clear recommendation.

**Output fields:**
| Field | Description |
|---|---|
| `match_score` | 0–100 overall compatibility score |
| `skill_score` | Skills alignment score |
| `budget_score` | Budget range compatibility |
| `experience_score` | Experience fit score |
| `matched_skills` | Skills the vendor has that the tender needs |
| `missing_skills` | Skills gaps to address |
| `recommendation` | Highly Recommended / Recommended / Consider / Not Recommended |
| `strengths` | Vendor's strongest points for this tender |
| `gaps` | Areas where vendor falls short |

---

### Agent 3 — Eligibility Checker

**Endpoint:** `POST /api/eligibility`  
**Input:** vendor profile + tender details  
**What it does:** Checks whether a vendor formally meets the tender's requirements — certifications, experience thresholds, budget range, location. Returns a clear verdict and flags any blocking issues.

**Output fields:**
| Field | Description |
|---|---|
| `eligible` | `true` / `false` |
| `eligibility_score` | 0–100 |
| `verdict` | Fully Eligible / Conditionally Eligible / Not Eligible |
| `met_requirements` | Requirements the vendor satisfies |
| `missing_requirements` | Hard requirements not met |
| `partially_met` | Requirements partially satisfied |
| `blocking_issues` | Disqualifying problems (if any) |
| `recommendations` | Actions vendor can take to become eligible |

---

### Agent 4 — Risk Analyzer

**Endpoint:** `POST /api/risk`  
**Input:** tender details  
**What it does:** Analyzes the tender for execution risks across budget, timeline, technical, compliance, and scope dimensions. Returns a go/no-go recommendation with rationale.

**Output fields:**
| Field | Description |
|---|---|
| `overall_risk` | Low / Medium / High |
| `risk_score` | 0–100 |
| `budget_viability` | Adequate / Tight / Insufficient |
| `timeline_viability` | Realistic / Aggressive / Unrealistic |
| `risks` | List of `{category, level, description}` objects |
| `mitigation_suggestions` | Practical ways to reduce each risk |
| `go_no_go` | Go / Proceed with Caution / No-Go |
| `go_no_go_rationale` | One-line reason for the decision |

---

### Agent 5 — Bid Generator

**Endpoint:** `POST /api/bid`  
**Input:** vendor profile + tender details  
**What it does:** Writes a professional bid proposal tailored to the specific vendor and tender. Only runs in the pipeline if the vendor is eligible **and** match score ≥ 60%.

**Output fields:**
| Field | Description |
|---|---|
| `executive_summary` | 3 compelling sentences on why this vendor wins |
| `value_proposition` | Unique positioning statement |
| `cover_letter_opening` | Professional opening paragraph |
| `technical_approach` | 3–4 sentence methodology |
| `methodology` | Phased delivery plan (array of strings) |
| `team_composition` | `[{role, count, experience}]` |
| `timeline_overview` | High-level delivery timeline |
| `competitive_advantages` | Vendor's strongest differentiators |
| `cost_breakdown` | Budget split by category (%) |

---

### Full pipeline

**Endpoint:** `POST /api/pipeline`  
**Input:** vendor + tender  
**What it does:** Runs all 5 agents in the optimal order. Agents 1–4 run in parallel. Agent 5 only runs if the vendor clears the eligibility and match threshold.

```json
// Example response shape
{
  "success": true,
  "pipeline": "complete",
  "results": {
    "analysis":    { ... },
    "match":       { "match_score": 85, ... },
    "eligibility": { "eligible": true, ... },
    "risk":        { "go_no_go": "Go", ... },
    "bid":         { "executive_summary": "...", ... },
    "bid_generated": true
  },
  "errors": {}
}
```

If the vendor doesn't qualify for a bid, `bid` is `null` and `bid_skip_reason` explains why.

---

### Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure environment**
```bash
cp .env.example .env
# Fill in GROQ_API_KEY and TENDERIQ_API_KEYS
```

**3. Run the backend**
```bash
uvicorn main:app --reload
# API docs available at http://localhost:8000/docs
```

**4. Test all agents**
```bash
python run_agents.py
```

---

### Authentication

All endpoints require an `X-API-Key` header:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "X-API-Key: your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"title": "Smart City IoT", "description": "..."}'
```

Generate a key with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### Tech stack

| Layer | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| LLM | Groq API · Llama 3.3 70B |
| PDF parsing | PyMuPDF (fitz) |
| Web scraping | httpx + BeautifulSoup4 |
| Auth | API key via `X-API-Key` header |
| Rate limiting | slowapi |
