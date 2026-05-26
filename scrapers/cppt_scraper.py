import logging
from typing import Any, List
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

SAMPLE_TENDERS = [
    {
        "source": "cppt",
        "source_tender_id": "CPPT-0001",
        "title": "Municipal Waste Management System Upgrade",
        "authority": "Urban Infrastructure Authority",
        "deadline": "2026-08-15",
        "estimated_value": "₹18,500,000",
        "category": "Infrastructure",
        "region": "Karnataka",
        "tender_url": "https://cppt.gov.in/tenders/CPPT-0001",
        "pdf_urls": [],
    },
    {
        "source": "cppt",
        "source_tender_id": "CPPT-0002",
        "title": "Smart City Traffic Signal Modernization",
        "authority": "Transportation Department",
        "deadline": "2026-09-05",
        "estimated_value": "₹23,200,000",
        "category": "Smart City",
        "region": "Maharashtra",
        "tender_url": "https://cppt.gov.in/tenders/CPPT-0002",
        "pdf_urls": [],
    },
]


async def scrape_cppt_portal(url: str) -> List[dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=20, headers={"User-Agent": "Mozilla/5.0"}) as client:
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

        results: List[dict[str, Any]] = []

        def extract_text(element, default=""):
            return element.get_text(strip=True) if element else default

        rows = soup.select(".tender-item") or soup.select("table tbody tr")

        for row in rows:
            title = extract_text(row.select_one(".tender-title")) or extract_text(row.select_one("td:nth-of-type(1)"))
            authority = extract_text(row.select_one(".tender-authority")) or extract_text(row.select_one("td:nth-of-type(2)"))
            deadline = extract_text(row.select_one(".tender-deadline")) or extract_text(row.select_one("td:nth-of-type(3)"))
            estimated_value = extract_text(row.select_one(".tender-value")) or extract_text(row.select_one("td:nth-of-type(4)"))
            tender_id = extract_text(row.select_one(".tender-id")) or extract_text(row.select_one("td:nth-of-type(1)"))
            tender_url = row.select_one("a")
            tender_url = urljoin(url, tender_url["href"]) if tender_url and tender_url.has_attr("href") else url
            pdf_links = row.select("a[href$='.pdf']")
            pdf_urls = [urljoin(url, link["href"]) for link in pdf_links if link.has_attr("href")]
            category = extract_text(row.select_one(".tender-category"))
            region = extract_text(row.select_one(".tender-region"))

            if not tender_id.strip():
                continue

            results.append(
                {
                    "source": url,
                    "source_tender_id": tender_id.strip(),
                    "title": title.strip() or "Untitled Tender",
                    "authority": authority.strip(),
                    "deadline": deadline.strip(),
                    "estimated_value": estimated_value.strip(),
                    "category": category.strip() if category else None,
                    "region": region.strip() if region else None,
                    "tender_url": tender_url,
                    "pdf_urls": pdf_urls,
                }
            )

        if not results:
            logger.warning("No tenders parsed from %s, returning sample dataset.", url)
            return SAMPLE_TENDERS

        return results

    except Exception as error:
        logger.warning("Unable to scrape CPPP portal %s: %s", url, error)
        return SAMPLE_TENDERS


if __name__ == "__main__":
    import asyncio

    sample_url = "https://cppt.gov.in/tenders"
    print(asyncio.run(scrape_cppt_portal(sample_url)))
