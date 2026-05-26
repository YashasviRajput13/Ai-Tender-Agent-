import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .scraper_service import run_scraper_job


DEFAULT_SOURCE = os.getenv("DEFAULT_SCRAPER_URL", "https://cppt.gov.in/tenders")
SCHEDULE_CRON = os.getenv("SCRAPE_CRON", "0 */4 * * *")


def schedule_scraper() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(run_scraper_job, "cron", args=[DEFAULT_SOURCE], id="cppt_scrape", replace_existing=True, minute="0", hour="*/4")
    return scheduler


if __name__ == "__main__":
    scheduler = schedule_scraper()
    scheduler.start()
    print("Scheduler started for CPPP scraping every 4 hours.")
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
