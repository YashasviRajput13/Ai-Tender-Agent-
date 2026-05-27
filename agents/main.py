# main.py — TenderIQ FastAPI Backend (production-ready)
# Changes from original:
#   - CORS origins read from ALLOWED_ORIGINS env var
#   - All endpoints protected by API key auth (Depends(require_api_key))
#   - Rate limiting via slowapi (20 req/min per IP on agent endpoints)
#   - Pipeline parallelizes the first 4 agents with asyncio.gather
#   - Synchronous agent calls wrapped in asyncio.to_thread (non-blocking)
#   - Live tender scraper results cached for 15 minutes

import asyncio
import os
import tempfile
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from auth import require_api_key
from agents import (
    analyze_tender,
    match_vendor_to_tender,
    check_eligibility,
    analyze_risk,
    generate_bid,
)
from pdf_processor import extract_text_from_pdf, truncate_for_ai
from scraper import fetch_all_tenders, get_categories

# ── Rate limiter ───────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── App setup ──────────────────────────────────────────────────────
app = FastAPI(
    title="TenderIQ API",
    description="AI-Powered Tender Intelligence Platform — 5 Agents",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS — read allowed origins from env var ───────────────────────
# In .env:  ALLOWED_ORIGINS=https://yourapp.com,https://www.yourapp.com
_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
ALLOWED_ORIGINS = [o.strip() for o in _origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Simple in-memory scraper cache ────────────────────────────────
_scraper_cache: dict = {}
CACHE_TTL_SECONDS = 900  # 15 minutes


async def get_tenders_cached(keyword: str, category: str, limit: int) -> dict:
    cache_key = f"{keyword}|{category}|{limit}"
    entry = _scraper_cache.get(cache_key)
    now = datetime.now(timezone.utc).timestamp()
    if entry and (now - entry["ts"]) < CACHE_TTL_SECONDS:
        return entry["data"]
    result = await fetch_all_tenders(keyword=keyword, category=category, limit=limit)
    _scraper_cache[cache_key] = {"ts": now, "data": result}
    return result


# ── Async wrappers for sync agent calls ───────────────────────────
# Prevents blocking the FastAPI event loop during LLM calls.
async def async_analyze_tender(tender):
    return await asyncio.to_thread(analyze_tender, tender)

async def async_match(vendor, tender):
    return await asyncio.to_thread(match_vendor_to_tender, vendor, tender)

async def async_eligibility(vendor, tender):
    return await asyncio.to_thread(check_eligibility, vendor, tender)

async def async_risk(tender):
    return await asyncio.to_thread(analyze_risk, tender)

async def async_bid(vendor, tender):
    return await asyncio.to_thread(generate_bid, vendor, tender)


# ── Request / response models ──────────────────────────────────────
class TenderModel(BaseModel):
    id:              Optional[str]       = "TND-001"
    title:           str
    client:          Optional[str]       = ""
    budget:          Optional[str]       = ""
    deadline:        Optional[str]       = ""
    required_skills: Optional[List[str]] = []
    category:        Optional[str]       = ""
    location:        Optional[str]       = ""
    duration:        Optional[str]       = ""
    description:     Optional[str]       = ""

class VendorModel(BaseModel):
    id:               Optional[str]       = "VND-001"
    company_name:     str
    description:      Optional[str]       = ""
    skills:           Optional[List[str]] = []
    experience_years: Optional[int]       = 0
    location:         Optional[str]       = ""
    budget_min:       Optional[float]     = 0
    budget_max:       Optional[float]     = 0
    certifications:   Optional[List[str]] = []
    past_projects:    Optional[int]       = 0
    rating:           Optional[float]     = 0.0

class MatchRequest(BaseModel):
    vendor: VendorModel
    tender: TenderModel

class BidRequest(BaseModel):
    vendor: VendorModel
    tender: TenderModel


# ── Health (no auth required) ──────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "platform": "TenderIQ",
        "status":   "running ✅",
        "docs":     "/docs",
        "agents":   5,
    }

@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "healthy", "agents_ready": 5}


# ── Agent 1 — tender analyzer ──────────────────────────────────────
@app.post("/api/analyze", tags=["Agents"])
@limiter.limit("20/minute")
async def api_analyze(
    request: Request,
    tender: TenderModel,
    _: str = Depends(require_api_key),
):
    try:
        result = await async_analyze_tender(tender.dict())
        return {"success": True, "agent": "TenderAnalyzer", "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Agent 2 — matching engine ──────────────────────────────────────
@app.post("/api/match", tags=["Agents"])
@limiter.limit("20/minute")
async def api_match(
    request: Request,
    req: MatchRequest,
    _: str = Depends(require_api_key),
):
    try:
        result = await async_match(req.vendor.dict(), req.tender.dict())
        return {"success": True, "agent": "MatchingEngine", "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Agent 3 — eligibility checker ─────────────────────────────────
@app.post("/api/eligibility", tags=["Agents"])
@limiter.limit("20/minute")
async def api_eligibility(
    request: Request,
    req: MatchRequest,
    _: str = Depends(require_api_key),
):
    try:
        result = await async_eligibility(req.vendor.dict(), req.tender.dict())
        return {"success": True, "agent": "EligibilityChecker", "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Agent 4 — risk analyzer ────────────────────────────────────────
@app.post("/api/risk", tags=["Agents"])
@limiter.limit("20/minute")
async def api_risk(
    request: Request,
    tender: TenderModel,
    _: str = Depends(require_api_key),
):
    try:
        result = await async_risk(tender.dict())
        return {"success": True, "agent": "RiskAnalyzer", "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Agent 5 — bid generator ────────────────────────────────────────
@app.post("/api/bid", tags=["Agents"])
@limiter.limit("10/minute")
async def api_bid(
    request: Request,
    req: BidRequest,
    _: str = Depends(require_api_key),
):
    try:
        result = await async_bid(req.vendor.dict(), req.tender.dict())
        return {"success": True, "agent": "BidGenerator", "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Full pipeline — all 5 agents, first 4 in parallel ─────────────
@app.post("/api/pipeline", tags=["Pipeline"])
@limiter.limit("5/minute")
async def api_pipeline(
    request: Request,
    req: BidRequest,
    _: str = Depends(require_api_key),
):
    vendor = req.vendor.dict()
    tender = req.tender.dict()
    results = {}
    errors  = {}

    # Run the first 4 agents in parallel — ~4x faster than sequential
    analysis_task    = async_analyze_tender(tender)
    match_task       = async_match(vendor, tender)
    eligibility_task = async_eligibility(vendor, tender)
    risk_task        = async_risk(tender)

    outcomes = await asyncio.gather(
        analysis_task, match_task, eligibility_task, risk_task,
        return_exceptions=True,
    )

    for key, outcome in zip(["analysis", "match", "eligibility", "risk"], outcomes):
        if isinstance(outcome, Exception):
            errors[key] = str(outcome)
        else:
            results[key] = outcome

    # Only generate bid if eligible AND match >= 60
    score    = results.get("match",       {}).get("match_score", 0)
    eligible = results.get("eligibility", {}).get("eligible",    False)

    if eligible and score >= 60:
        try:
            results["bid"]           = await async_bid(vendor, tender)
            results["bid_generated"] = True
        except Exception as e:
            errors["bid"]            = str(e)
            results["bid_generated"] = False
    else:
        results["bid"]             = None
        results["bid_generated"]   = False
        results["bid_skip_reason"] = (
            "Vendor not eligible" if not eligible
            else f"Match score too low ({score}%)"
        )

    return {
        "success":  True,
        "pipeline": "complete",
        "results":  results,
        "errors":   errors,
    }


# ── Sample data ────────────────────────────────────────────────────
@app.get("/api/sample-data", tags=["Utilities"])
def sample_data(_: str = Depends(require_api_key)):
    return {
        "tender": {
            "id": "TND-001",
            "title": "Smart City IoT Infrastructure",
            "client": "Ministry of Urban Development",
            "budget": "$2,500,000",
            "deadline": "2026-09-15",
            "required_skills": ["IoT", "Cloud Architecture", "React.js", "5G", "Python"],
            "category": "Technology",
            "location": "New Delhi, India",
            "duration": "18 months",
            "description": "Deploy IoT infrastructure across 50 smart city nodes with real-time dashboards.",
        },
        "vendor": {
            "id": "VND-001",
            "company_name": "TechVision Solutions",
            "description": "Premier IoT and cloud infrastructure firm.",
            "skills": ["IoT", "Cloud Architecture", "React.js", "Python", "Data Analytics"],
            "experience_years": 8,
            "location": "New Delhi",
            "budget_min": 500000,
            "budget_max": 3000000,
            "certifications": ["ISO 27001", "AWS Professional"],
            "past_projects": 24,
            "rating": 4.8,
        },
    }


# ── PDF endpoints ──────────────────────────────────────────────────
@app.post("/api/pdf/extract", tags=["PDF"])
@limiter.limit("10/minute")
async def pdf_extract(
    request: Request,
    file: UploadFile = File(...),
    _: str = Depends(require_api_key),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read(maxsize=20 * 1024 * 1024)  # 20 MB limit
        tmp.write(contents)
        tmp_path = tmp.name
    try:
        extracted = extract_text_from_pdf(tmp_path)
        return {
            "success":      True,
            "filename":     file.filename,
            "page_count":   extracted["page_count"],
            "file_size_kb": extracted["file_size_kb"],
            "metadata":     extracted["metadata"],
            "hints":        extracted["hints"],
            "preview":      extracted["full_text"][:800],
            "char_count":   len(extracted["full_text"]),
        }
    except Exception as e:
        raise HTTPException(500, f"PDF extraction failed: {str(e)}")
    finally:
        os.unlink(tmp_path)


@app.post("/api/pdf/analyze", tags=["PDF"])
@limiter.limit("5/minute")
async def pdf_analyze(
    request: Request,
    file: UploadFile = File(...),
    _: str = Depends(require_api_key),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read(maxsize=20 * 1024 * 1024)
        tmp.write(contents)
        tmp_path = tmp.name
    try:
        extracted = extract_text_from_pdf(tmp_path)
        if len(extracted["full_text"].strip()) < 50:
            raise HTTPException(422, "PDF appears to be scanned/image-based. Text extraction returned too little content.")
        ai_text = truncate_for_ai(extracted["full_text"], max_chars=6000)
        tender_input = {
            "source":         "pdf_upload",
            "filename":       file.filename,
            "extracted_text": ai_text,
            "hints":          extracted["hints"],
            "page_count":     extracted["page_count"],
            "metadata":       extracted["metadata"],
        }
        analysis = await async_analyze_tender(tender_input)
        return {
            "success":      True,
            "filename":     file.filename,
            "pages":        extracted["page_count"],
            "size_kb":      extracted["file_size_kb"],
            "hints":        extracted["hints"],
            "analysis":     analysis,
            "text_preview": extracted["full_text"][:500],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")
    finally:
        os.unlink(tmp_path)


@app.post("/api/pdf/full-pipeline", tags=["PDF"])
@limiter.limit("3/minute")
async def pdf_full_pipeline(
    request: Request,
    file: UploadFile = File(...),
    vendor_name:       str   = "TechVision Solutions",
    vendor_skills:     str   = "IoT, Cloud, Python, React.js",
    vendor_experience: int   = 5,
    vendor_budget_min: float = 100000,
    vendor_budget_max: float = 5000000,
    _: str = Depends(require_api_key),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read(maxsize=20 * 1024 * 1024)
        tmp.write(contents)
        tmp_path = tmp.name
    try:
        extracted = extract_text_from_pdf(tmp_path)
        ai_text   = truncate_for_ai(extracted["full_text"])
        tender = {
            "source":         "pdf_upload",
            "filename":       file.filename,
            "extracted_text": ai_text,
            "hints":          extracted["hints"],
            "page_count":     extracted["page_count"],
        }
        vendor = {
            "company_name":     vendor_name,
            "skills":           [s.strip() for s in vendor_skills.split(",")],
            "experience_years": vendor_experience,
            "budget_min":       vendor_budget_min,
            "budget_max":       vendor_budget_max,
        }
        results = {}
        errors  = {}

        # First 4 agents in parallel
        outcomes = await asyncio.gather(
            async_analyze_tender(tender),
            async_match(vendor, tender),
            async_eligibility(vendor, tender),
            async_risk(tender),
            return_exceptions=True,
        )
        for key, outcome in zip(["analysis", "match", "eligibility", "risk"], outcomes):
            if isinstance(outcome, Exception):
                errors[key] = str(outcome)
            else:
                results[key] = outcome

        score    = results.get("match",       {}).get("match_score", 0)
        eligible = results.get("eligibility", {}).get("eligible",    False)

        if eligible and score >= 60:
            try:
                results["bid"]           = await async_bid(vendor, tender)
                results["bid_generated"] = True
            except Exception as e:
                errors["bid"]            = str(e)
                results["bid_generated"] = False
        else:
            results["bid"]             = None
            results["bid_generated"]   = False
            results["bid_skip_reason"] = (
                "Vendor not eligible" if not eligible
                else f"Match score too low ({score}%)"
            )

        return {
            "success":   True,
            "filename":  file.filename,
            "pages":     extracted["page_count"],
            "size_kb":   extracted["file_size_kb"],
            "hints":     extracted["hints"],
            "pipeline":  "complete",
            "results":   results,
            "errors":    errors,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        os.unlink(tmp_path)


# ── Live tenders (cached) ──────────────────────────────────────────
@app.get("/api/tenders/live", tags=["Live Tenders"])
@limiter.limit("30/minute")
async def get_live_tenders(
    request: Request,
    keyword:  str = "",
    category: str = "",
    limit:    int = 20,
    _: str = Depends(require_api_key),
):
    result = await get_tenders_cached(keyword=keyword, category=category, limit=limit)
    return {"success": True, "tenders": result.get("tenders", [])}


@app.get("/api/tenders/categories", tags=["Live Tenders"])
def get_tender_categories(_: str = Depends(require_api_key)):
    return {"categories": get_categories()}


@app.post("/api/tenders/analyze-and-match", tags=["Live Tenders"])
@limiter.limit("5/minute")
async def analyze_and_match_live_tender(
    request: Request,
    data: dict,
    _: str = Depends(require_api_key),
):
    tender = data.get("tender", {})
    vendor = data.get("vendor", {})
    if not tender or not vendor:
        raise HTTPException(400, "Both tender and vendor are required")

    results = {}
    errors  = {}

    outcomes = await asyncio.gather(
        async_analyze_tender(tender),
        async_match(vendor, tender),
        async_eligibility(vendor, tender),
        async_risk(tender),
        return_exceptions=True,
    )
    for key, outcome in zip(["analysis", "match", "eligibility", "risk"], outcomes):
        if isinstance(outcome, Exception):
            errors[key] = str(outcome)
        else:
            results[key] = outcome

    score    = results.get("match",       {}).get("match_score", 0)
    eligible = results.get("eligibility", {}).get("eligible",    False)

    if eligible and score >= 60:
        try:
            results["bid"]           = await async_bid(vendor, tender)
            results["bid_generated"] = True
        except Exception as e:
            errors["bid"]            = str(e)
            results["bid_generated"] = False
    else:
        results["bid"]             = None
        results["bid_generated"]   = False
        results["bid_skip_reason"] = (
            "Vendor not eligible" if not eligible
            else f"Match score too low ({score}%)"
        )

    return {
        "success":      True,
        "tender_title": tender.get("title", ""),
        "vendor_name":  vendor.get("company_name", ""),
        "pipeline":     "complete",
        "results":      results,
        "errors":       errors,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
