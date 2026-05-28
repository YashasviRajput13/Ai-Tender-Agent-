import os
import smtplib
import sys
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Any, Optional

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from . import db, models, schemas
    from .analysis_agent import analyze_tender_text
    from . import repository as repo
except ImportError:  # support module execution from the package root
    from backend.services.tender_service import db, models, schemas
    from backend.services.tender_service.analysis_agent import analyze_tender_text
    from backend.services.tender_service import repository as repo
from scrapers.pdf_extractor import download_and_extract_pdf
from scrapers.scraper import run_scraper_job
from scrapers.scheduler import schedule_scraper

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


def get_smtp_settings() -> dict[str, Any]:
    return {
        "host": os.getenv("SMTP_HOST", "localhost"),
        "port": int(os.getenv("SMTP_PORT", "25")),
        "username": os.getenv("SMTP_USERNAME"),
        "password": os.getenv("SMTP_PASSWORD"),
        "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes"),
        "from_address": os.getenv("EMAIL_FROM", "no-reply@agentic-ai-tender.local"),
    }


def send_email(recipient: str, subject: str, body: str) -> None:
    settings = get_smtp_settings()
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings["from_address"]
    message["To"] = recipient
    message.set_content(body)
    if settings["username"] and settings["password"]:
        server = smtplib.SMTP(settings["host"], settings["port"], timeout=30)
        if settings["use_tls"]:
            server.starttls()
        server.login(settings["username"], settings["password"])
    else:
        server = smtplib.SMTP(settings["host"], settings["port"], timeout=30)
    try:
        server.send_message(message)
    finally:
        server.quit()


@app.on_event("startup")
async def startup_event() -> None:
    await create_database()
    async with db.async_session() as session:
        deleted = await repo.delete_demo_tenders(session)
        if deleted > 0:
            await publish_event({"type": "seed.cleanup", "deleted_count": deleted})
    scheduler = schedule_scraper()
    scheduler.start()
    app.state.scraper_scheduler = scheduler


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
    source_url = request.source_url or os.getenv("DEFAULT_SCRAPER_URL", "https://eprocure.gov.in/eprocure/app")
    background_tasks.add_task(run_scraper_job, source_url)
    background_tasks.add_task(publish_event, {"type": "scrape.started", "source_url": source_url})
    return {"status": "started", "source_url": source_url}


@app.get("/scrape/status")
async def scrape_status(db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    logs = await repo.get_scrape_logs(db, limit=1)
    if not logs:
        return {"status": "idle", "message": "No scrape job has run yet."}
    log = logs[0]
    return {
        "status": log.status,
        "source_url": log.source_url,
        "records_scraped": log.records_scraped,
        "records_created": log.records_created,
        "started_at": log.started_at,
        "finished_at": log.finished_at,
        "message": log.message,
    }


@app.get("/scrape/logs", response_model=list[schemas.ScrapeLogRead])
async def scrape_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await repo.get_scrape_logs(db, limit=limit)


@app.post("/analysis/start/{tender_id}")
async def start_analysis(
    tender_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    tender = await repo.get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")

    async def analyze_and_store():
        async with db.async_session() as session:
            current_tender = await repo.get_tender(session, tender_id)
            if current_tender is None:
                return

            pdf_urls = (current_tender.raw_metadata or {}).get("pdf_urls", [])
            raw_texts: list[str] = []
            if pdf_urls:
                async with httpx.AsyncClient(timeout=60) as client:
                    for url in pdf_urls:
                        try:
                            extracted_text, filename = await download_and_extract_pdf(url, client)
                            if extracted_text:
                                raw_texts.append(extracted_text)
                                await repo.create_document(
                                    session,
                                    current_tender.id,
                                    {
                                        "url": url,
                                        "filename": filename,
                                        "raw_text": extracted_text,
                                    },
                                )
                        except Exception:
                            continue

            if current_tender.documents and not raw_texts:
                raw_texts = [doc.raw_text or "" for doc in current_tender.documents]

            document_text = "\n\n".join([current_tender.description or "", *raw_texts]).strip()
            result = await analyze_tender_text(document_text)
            analysis_payload = {
                "summary": result.get("summary"),
                "eligibility": result.get("eligibility"),
                "required_documents": result.get("required_documents"),
                "technical_requirements": result.get("technical_requirements"),
                "risk_factors": result.get("risk_factors"),
                "recommendation": result.get("recommendation"),
                "risk_level": result.get("risk_level"),
                "risk_reasons": result.get("risk_reasons"),
                "category": result.get("category"),
                "deadline": result.get("deadline"),
                "budget": result.get("budget"),
                "confidence_score": result.get("confidence_score"),
                "match_score": result.get("match_score"),
                "success_probability": result.get("success_probability"),
                "raw_response": result,
            }
            analysis_record = await repo.create_or_update_analysis(session, tender_id, analysis_payload)
            if analysis_record.match_score and analysis_record.match_score >= 80:
                await repo.create_notification(
                    session,
                    schemas.NotificationCreate(
                        title="High Match Opportunity",
                        message=f"Tender {current_tender.title} has a high match score of {analysis_record.match_score}%.",
                        notification_type="high_match",
                        tender_id=tender_id,
                    ),
                )
        await publish_event({"type": "analysis.completed", "tender_id": tender_id})

    background_tasks.add_task(analyze_and_store)
    return {"status": "analysis_started", "tender_id": tender_id}


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


@app.post("/notifications/send/{tender_id}")
async def send_notification_email(
    tender_id: int,
    request: schemas.NotificationEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    tender = await repo.get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    analysis = await repo.get_analysis(db, tender_id)
    subject = f"Tender Alert: {tender.title}"
    body = [
        f"Tender: {tender.title}",
        f"Deadline: {tender.deadline}",
        f"Match score: {analysis.match_score if analysis else 'N/A'}",
        f"Recommendation: {analysis.recommendation if analysis else 'Pending analysis'}",
        f"Tender link: {tender.tender_url}",
    ]
    try:
        send_email(request.recipient, subject, "\n".join(body))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email delivery failed: {exc}")

    notification = await repo.create_notification(
        db,
        schemas.NotificationCreate(
            title="Email alert sent",
            message=f"Email alert sent for tender {tender.title} to {request.recipient}.",
            notification_type="new",
            tender_id=tender.id,
        ),
    )
    await publish_event({"type": "notification.email_sent", "tender_id": tender.id, "recipient": request.recipient})
    return {"status": "sent", "recipient": request.recipient, "tender_id": tender.id}


@app.get("/health")
async def health() -> dict[str, Any]:
    database_url = os.getenv("DATABASE_URL") or os.getenv(
        "POSTGRES_URL",
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
            try:
                version_result = await connection.execute(text("SELECT version_num FROM alembic_version"))
                report["alembic_version"] = [row[0] for row in version_result.fetchall()]
            except Exception:
                report["alembic_version"] = None
    except Exception as exc:
        report["status"] = "fail"
        report["connection"] = "FAIL"
        report["error"] = str(exc)
        report["select_1"] = False
    return report
