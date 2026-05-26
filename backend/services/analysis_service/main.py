from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Analysis Service")

class AnalysisRequest(BaseModel):
    title: str
    description: str
    requirements: List[str]
    value: float
    region: str

class AnalysisResponse(BaseModel):
    summary: str
    eligibility: str
    risk_score: float
    match_score: float
    next_steps: List[str]

@app.post("/analysis/score", response_model=AnalysisResponse)
async def score_tender(payload: AnalysisRequest):
    eligibility = "pass" if len(payload.requirements) <= 6 else "review"
    risk = 0.2 if payload.value < 500000 else 0.55
    match = 0.85 if payload.region.lower() in ["north america", "europe"] else 0.65
    summary = f"Tender '{payload.title}' is a {payload.region} opportunity worth ${payload.value:,.0f}."
    next_steps = [
        "Validate certifications and financials.",
        "Prepare proposal package.",
        "Notify sales and delivery teams.",
    ]
    return AnalysisResponse(
        summary=summary,
        eligibility=eligibility,
        risk_score=risk,
        match_score=match,
        next_steps=next_steps,
    )

@app.get("/health")
async def health():
    return {"status": "ok", "service": "analysis"}
