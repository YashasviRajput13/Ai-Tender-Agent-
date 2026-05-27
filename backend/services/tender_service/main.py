import os
import sys
from datetime import datetime
from typing import Any, Optional

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from . import db, models, schemas
from .analysis_agent import analyze_tender_text
from . import repository as repo
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
async def list_tenders_endpoint(
    region: str | None = Query(None),
    category: str | None = Query(None),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await repo.list_tenders(db, region=region, category=category, status=status)


@app.get("/tenders/{tender_id}", response_model=schemas.TenderRead)
async def get_tender_endpoint(tender_id: int, db: AsyncSession = Depends(get_db)):
    tender = await repo.get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    return tender


@app.post("/tenders", response_model=schemas.TenderRead)
async def create_tender_endpoint(request: schemas.TenderCreate, db: AsyncSession = Depends(get_db)):
    return await repo.create_tender(db, request)


@app.put("/tenders/{tender_id}", response_model=schemas.TenderRead)
async def update_tender_endpoint(
    tender_id: int,
    request: schemas.TenderCreate,
    db: AsyncSession = Depends(get_db),
):
    tender = await repo.get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    for key, value in request.model_dump().items():
        setattr(tender, key, value)
    await db.commit()
    await db.refresh(tender)
    return tender


@app.delete("/tenders/{tender_id}")
async def delete_tender_endpoint(tender_id: int, db: AsyncSession = Depends(get_db)):
    tender = await repo.get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    await db.delete(tender)
    await db.commit()
    return {"status": "deleted", "tender_id": tender_id}


@app.post("/tenders/import", response_model=list[schemas.TenderRead])
async def import_tenders(
    payload: list[schemas.TenderCreate],
    db: AsyncSession = Depends(get_db),
):
    return await repo.import_tenders(db, payload)


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
    tender = await repo.get_tender(db, request.tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")

    async def analyze_and_store():
        async with db.async_session() as session:
            current_tender = await repo.get_tender(session, request.tender_id)
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
            await repo.create_or_update_analysis(session, request.tender_id, analysis_payload)
        await publish_event({"type": "analysis.completed", "tender_id": request.tender_id})

    background_tasks.add_task(analyze_and_store)
    return {"status": "analysis_started", "tender_id": request.tender_id}


@app.get("/analysis/{tender_id}", response_model=schemas.TenderAnalysisRead)
async def get_analysis(tender_id: int, db: AsyncSession = Depends(get_db)):
    analysis = await repo.get_analysis(db, tender_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@app.get("/recommendations", response_model=list[schemas.RecommendationItem])
async def get_recommendations(
    company_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    items = await repo.list_recommendations(db, company_id=company_id)
    return [
        schemas.RecommendationItem(
            tender_id=record.tender_id,
            title=getattr(record.tender, "title", "Unknown Tender") if record.tender else "Unknown Tender",
            authority=getattr(record.tender, "authority", None) if record.tender else None,
            match_score=record.match_score or 0.0,
            success_probability=record.success_probability or 0.0,
            risk_level=record.risk_level,
            budget=record.budget,
            deadline=record.deadline,
        )
        for record in items
    ]


@app.get("/dashboard/stats", response_model=schemas.DashboardStats)
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    stats = await repo.get_dashboard_stats(db)
    return schemas.DashboardStats(**stats)


@app.get("/notifications", response_model=list[schemas.NotificationRead])
async def notifications(
    user_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await repo.list_notifications(db, user_id=user_id)


@app.post("/notifications", response_model=schemas.NotificationRead)
async def create_notification(request: schemas.NotificationCreate, db: AsyncSession = Depends(get_db)):
    notification = await repo.create_notification(db, request)
    await publish_event({"type": "notification.created", "notification_id": notification.id})
    return notification


@app.get("/health")
async def health() -> dict[str, Any]:
    database_url = os.getenv("POSTGRES_URL") or os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/agentic_ai_tender",
    )
    report = {
        "status": "ok",
        "service": "tender",
        "database_url": database_url,
        "connection": "unknown",
        "select_1": "unknown",
        "tables": [],
        "alembic_version": None,
    }
    try:
        async with db.engine.connect() as connection:
            report["connection"] = "PASS"
            result = await connection.execute(text("SELECT 1"))
            report["select_1"] = result.scalar() == 1
            report["tables"] = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            version_result = await connection.execute(text("SELECT version_num FROM alembic_version"))
            report["alembic_version"] = [row[0] for row in version_result.fetchall()]
    except Exception as exc:
        report["status"] = "fail"
        report["connection"] = "FAIL"
        report["error"] = str(exc)
        report["select_1"] = False
    return report
