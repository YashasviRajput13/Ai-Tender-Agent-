import os
import sys
from typing import Any

from dateutil import parser as date_parser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scrapers.cppt_scraper import scrape_cppt_portal
from backend.services.tender_service import crud, db, schemas


def parse_value(value: str) -> float:
    cleaned = "".join(ch for ch in value if ch.isdigit() or ch in ".,")
    if not cleaned:
        return 0.0
    cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_deadline(value: str):
    try:
        return date_parser.parse(value)
    except Exception:
        return None


async def run_scraper_job(source_url: str) -> int:
    try:
        tenders = await scrape_cppt_portal(source_url)
    except Exception:
        tenders = []

    total_created = 0
    if not tenders:
        return total_created

    async with db.async_session() as session:
        for tender_data in tenders:
            if not tender_data.get("source_tender_id"):
                continue

            tender_in = schemas.TenderCreate(
                source="cppt",
                source_tender_id=tender_data.get("source_tender_id"),
                title=tender_data.get("title") or "Untitled Tender",
                description=tender_data.get("authority") or "",
                authority=tender_data.get("authority"),
                deadline=parse_deadline(str(tender_data.get("deadline", ""))),
                estimated_value=parse_value(str(tender_data.get("estimated_value", ""))),
                category=tender_data.get("category") or "",
                region=tender_data.get("region") or "",
                tender_url=tender_data.get("tender_url") or source_url,
                raw_metadata={
                    "pdf_urls": tender_data.get("pdf_urls", []),
                    "source_url": source_url,
                },
            )
            created = await crud.import_tenders(session, [tender_in])
            total_created += len(created)

    return total_created


if __name__ == "__main__":
    import asyncio

    target = os.getenv("DEFAULT_SCRAPER_URL", "https://cppt.gov.in/tenders")
    print(asyncio.run(run_scraper_job(target)))
