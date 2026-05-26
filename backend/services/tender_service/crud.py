from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import asc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_tender(db: AsyncSession, tender_id: int) -> Optional[models.Tender]:
    result = await db.execute(select(models.Tender).where(models.Tender.id == tender_id))
    return result.scalars().first()


async def get_tender_by_source_id(db: AsyncSession, source: str, source_tender_id: str) -> Optional[models.Tender]:
    result = await db.execute(
        select(models.Tender).where(
            models.Tender.source == source,
            models.Tender.source_tender_id == source_tender_id,
        )
    )
    return result.scalars().first()


async def list_tenders(
    db: AsyncSession,
    region: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
) -> List[models.Tender]:
    query = select(models.Tender)
    if region:
        query = query.where(models.Tender.region.ilike(f"%{region}%"))
    if category:
        query = query.where(models.Tender.category.ilike(f"%{category}%"))
    if status:
        query = query.where(models.Tender.status == status)
    query = query.order_by(models.Tender.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


async def list_recent_tenders(db: AsyncSession, limit: int = 10) -> List[models.Tender]:
    result = await db.execute(select(models.Tender).order_by(models.Tender.created_at.desc()).limit(limit))
    return result.scalars().all()


async def create_tender(db: AsyncSession, tender_in: schemas.TenderCreate) -> models.Tender:
    tender = models.Tender(**tender_in.model_dump())
    db.add(tender)
    await db.commit()
    await db.refresh(tender)
    return tender


async def import_tenders(db: AsyncSession, tenders: List[schemas.TenderCreate]) -> List[models.Tender]:
    results: List[models.Tender] = []
    for tender_in in tenders:
        if tender_in.source and tender_in.source_tender_id:
            existing = await get_tender_by_source_id(db, tender_in.source, tender_in.source_tender_id)
            if existing:
                continue
        results.append(await create_tender(db, tender_in))
    return results


async def create_document(db: AsyncSession, tender_id: int, document: dict[str, Any]) -> models.TenderDocument:
    record = models.TenderDocument(tender_id=tender_id, **document)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_analysis(db: AsyncSession, tender_id: int) -> Optional[models.TenderAnalysis]:
    result = await db.execute(select(models.TenderAnalysis).where(models.TenderAnalysis.tender_id == tender_id))
    return result.scalars().first()


async def create_or_update_analysis(db: AsyncSession, tender_id: int, payload: dict[str, Any]) -> models.TenderAnalysis:
    existing = await get_analysis(db, tender_id)
    if existing:
        for key, value in payload.items():
            setattr(existing, key, value)
        existing.updated_at = datetime.utcnow()
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        return existing

    record = models.TenderAnalysis(tender_id=tender_id, **payload)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def list_notifications(db: AsyncSession, user_id: Optional[int] = None) -> List[models.Notification]:
    query = select(models.Notification).order_by(models.Notification.created_at.desc())
    if user_id:
        query = query.where(models.Notification.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_notification(db: AsyncSession, notification: schemas.NotificationCreate) -> models.Notification:
    record = models.Notification(**notification.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_dashboard_stats(db: AsyncSession) -> dict[str, int]:
    total = await db.scalar(select(func.count()).select_from(models.Tender))
    active = await db.scalar(select(func.count()).select_from(models.Tender).where(models.Tender.status == "open"))
    high_match = await db.scalar(
        select(func.count()).select_from(models.TenderAnalysis).where(models.TenderAnalysis.match_score >= 80)
    )
    upcoming_deadlines = await db.scalar(
        select(func.count()).select_from(models.Tender).where(models.Tender.deadline >= func.now())
    )
    risk_alerts = await db.scalar(select(func.count()).select_from(models.RiskAssessment))
    return {
        "total_tenders": int(total or 0),
        "active_tenders": int(active or 0),
        "high_match_opportunities": int(high_match or 0),
        "upcoming_deadlines": int(upcoming_deadlines or 0),
        "risk_alerts": int(risk_alerts or 0),
    }


async def list_recommendations(db: AsyncSession, company_id: Optional[int] = None, limit: int = 10) -> List[models.TenderAnalysis]:
    query = select(models.TenderAnalysis).order_by(models.TenderAnalysis.match_score.desc().nullslast()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def log_agent_event(db: AsyncSession, agent_name: str, event_type: str, payload: dict[str, Any]) -> models.AgentLog:
    record = models.AgentLog(agent_name=agent_name, event_type=event_type, payload=payload)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def audit_action(db: AsyncSession, entity_type: str, entity_id: Optional[int], action: str, details: dict[str, Any]) -> models.AuditLog:
    record = models.AuditLog(entity_type=entity_type, entity_id=entity_id, action=action, details=details)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record
