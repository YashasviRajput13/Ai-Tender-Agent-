import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .scraper import run_scraper_job


DEFAULT_SOURCE = os.getenv("DEFAULT_SCRAPER_URL", "https://eprocure.gov.in/eprocure/app")
SCRAPE_INTERVAL_HOURS = int(os.getenv("SCRAPE_INTERVAL_HOURS", "6"))


def schedule_scraper() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        run_scraper_job,
        "cron",
        args=[DEFAULT_SOURCE],
        id="procurement_scrape",
        replace_existing=True,
        minute="0",
        hour=f"*/{SCRAPE_INTERVAL_HOURS}",
    )
    return scheduler


if __name__ == "__main__":
    scheduler = schedule_scraper()
    scheduler.start()
    print("Scheduler started for CPPP scraping every 6 hours.")
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
