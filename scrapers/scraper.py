import os
import sys
from datetime import datetime
from typing import Any

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.services.tender_service import db, models, schemas
from backend.services.tender_service import repository as repo
from .cppt_scraper import scrape_procurement_portal


def convert_tender_data(tender_data: dict[str, Any]) -> schemas.TenderCreate:
    return schemas.TenderCreate(
        source=tender_data.get("source") or "eprocure",
        source_tender_id=tender_data.get("source_tender_id"),
        title=tender_data.get("title") or "Untitled Tender",
        description=tender_data.get("authority") or "",
        authority=tender_data.get("authority"),
        deadline=tender_data.get("deadline"),
        estimated_value=tender_data.get("estimated_value"),
        category=tender_data.get("category"),
        region=tender_data.get("region"),
        tender_url=tender_data.get("tender_url"),
        raw_metadata={
            "pdf_urls": tender_data.get("pdf_urls", []),
            "source_url": tender_data.get("source"),
            "scrape_source": tender_data.get("source"),
        },
    )


async def ensure_database_schema() -> None:
    async with db.engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)


async def run_scraper_job(source_url: str | None = None) -> int:
    await ensure_database_schema()
    async with db.async_session() as session:
        log = await repo.create_scraper_log(
            session,
            source_url=source_url or "all",
            status="running",
            message="Scrape job started.",
            records_scraped=0,
            records_created=0,
        )
        try:
            tenders = await scrape_procurement_portal(source_url)
            scraped = len(tenders)
            created = 0
            for tender_data in tenders:
                if not tender_data.get("source_tender_id"):
                    continue
                tender_in = convert_tender_data(tender_data)
                created_tenders = await repo.import_tenders(session, [tender_in])
                for tender_obj in created_tenders:
                    created += 1
                    if tender_obj.deadline and tender_obj.deadline <= datetime.utcnow():
                        await repo.create_notification(
                            session,
                            schemas.NotificationCreate(
                                title="Deadline approaching",
                                message=f"Tender {tender_obj.title} closing soon.",
                                notification_type="deadline",
                                tender_id=tender_obj.id,
                            ),
                        )
                    else:
                        await repo.create_notification(
                            session,
                            schemas.NotificationCreate(
                                title="New Tender Imported",
                                message=f"{tender_obj.title} was imported from {tender_obj.source}.",
                                notification_type="new",
                                tender_id=tender_obj.id,
                            ),
                        )

            await repo.update_scraper_log(
                session,
                log.id,
                status="completed",
                finished_at=datetime.utcnow(),
                message=f"Scraped {scraped} tenders and created {created} new records.",
                records_scraped=scraped,
                records_created=created,
            )
            return created
        except Exception as exc:
            await repo.update_scraper_log(
                session,
                log.id,
                status="failed",
                finished_at=datetime.utcnow(),
                message=str(exc),
            )
            raise


if __name__ == "__main__":
    import asyncio

    target = os.getenv("DEFAULT_SCRAPER_URL", "https://eprocure.gov.in/eprocure/app")
    print(asyncio.run(run_scraper_job(target)))
