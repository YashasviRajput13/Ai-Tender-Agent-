import os
import sys
from datetime import datetime
from typing import Optional

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from . import crud, db, models, schemas
from .analysis_agent import analyze_tender_text
from .matching_agent import score_tender_against_company
from scrapers.scraper_service import run_scraper_job

app = FastAPI(title="Tender Service")


async def create_database() -> None:
    async with db.engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)


async def publish_event(event: dict) -> None:
    gateway_url = os.getenv("GATEWAY_EVENT_URL", "http://localhost:8000/events")
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            await client.post(gateway_url, json=event)
        except Exception:
            pass


@app.on_event("startup")
async def startup_event() -> None:
    await create_database()


async def get_db() -> AsyncSession:
    async with db.async_session() as session:
        yield session


@app.get("/tenders", response_model=list[schemas.TenderRead])
async def list_tenders(
    region: str | None = Query(None),
    category: str | None = Query(None),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_tenders(db, region=region, category=category, status=status)


@app.get("/tenders/{tender_id}", response_model=schemas.TenderRead)
async def get_tender(tender_id: int, db: AsyncSession = Depends(get_db)):
    tender = await crud.get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    return tender


@app.post("/tenders/import", response_model=list[schemas.TenderRead])
async def import_tenders(
    payload: list[schemas.TenderCreate],
    db: AsyncSession = Depends(get_db),
):
    return await crud.import_tenders(db, payload)


@app.post("/scrape/start")
async def start_scrape(
    background_tasks: BackgroundTasks,
    request: schemas.ScrapeRequest,
    db: AsyncSession = Depends(get_db),
):
    source_url = request.source_url or os.getenv("DEFAULT_SCRAPER_URL", "https://cppt.gov.in/tenders")
    background_tasks.add_task(run_scraper_job, source_url)
    background_tasks.add_task(publish_event, {"type": "scrape.started", "source_url": source_url})
    return {"status": "started", "source_url": source_url}


@app.post("/analysis/start")
async def start_analysis(
    background_tasks: BackgroundTasks,
    request: schemas.AnalysisRequest,
    db: AsyncSession = Depends(get_db),
):
    tender = await crud.get_tender(db, request.tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")

    async def analyze_and_store():
        async with db.async_session() as session:
            current_tender = await crud.get_tender(session, request.tender_id)
            if current_tender is None:
                return
            if current_tender.documents:
                document_text = "\n\n".join([doc.raw_text or "" for doc in current_tender.documents])
            else:
                document_text = current_tender.description or ""

            result = await analyze_tender_text(document_text)
            analysis_payload = {
                "summary": result.get("summary"),
                "eligibility": result.get("eligibility"),
                "required_documents": result.get("required_documents"),
                "risk_level": result.get("risk_level"),
                "risk_reasons": result.get("risk_reasons"),
                "category": result.get("category"),
                "deadline": result.get("deadline"),
                "budget": result.get("budget"),
                "confidence_score": result.get("confidence_score"),
                "raw_response": result,
            }
            await crud.create_or_update_analysis(session, request.tender_id, analysis_payload)
        await publish_event({"type": "analysis.completed", "tender_id": request.tender_id})

    background_tasks.add_task(analyze_and_store)
    return {"status": "analysis_started", "tender_id": request.tender_id}


@app.get("/analysis/{tender_id}", response_model=schemas.TenderAnalysisRead)
async def get_analysis(tender_id: int, db: AsyncSession = Depends(get_db)):
    analysis = await crud.get_analysis(db, tender_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@app.get("/recommendations", response_model=list[schemas.RecommendationItem])
async def get_recommendations(
    company_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    items = await crud.list_recommendations(db, company_id=company_id)
    return [
        schemas.RecommendationItem(
            tender_id=record.tender_id,
            title=record.tender.title,
            authority=record.tender.authority,
            match_score=record.match_score or 0.0,
            success_probability=record.success_probability or 0.0,
            risk_level=record.risk_level,
        )
        for record in items
    ]


@app.get("/dashboard/stats", response_model=schemas.DashboardStats)
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    stats = await crud.get_dashboard_stats(db)
    return schemas.DashboardStats(**stats)


@app.get("/notifications", response_model=list[schemas.NotificationRead])
async def notifications(
    user_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_notifications(db, user_id=user_id)


@app.post("/notifications", response_model=schemas.NotificationRead)
async def create_notification(request: schemas.NotificationCreate, db: AsyncSession = Depends(get_db)):
    notification = await crud.create_notification(db, request)
    await publish_event({"type": "notification.created", "notification_id": notification.id})
    return notification


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "tender",
        "database": os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/agentic_ai_tender"),
    }
