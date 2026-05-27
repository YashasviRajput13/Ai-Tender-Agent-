import logging
import re
from typing import Any, Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)
SOURCES = [
    {"name": "eprocure", "root": "https://eprocure.gov.in/eprocure/app"},
    {"name": "epublish", "root": "https://eprocure.gov.in/epublish/app"},
    {"name": "mptenders", "root": "https://mptenders.gov.in/nicgep/app"},
]
LIST_QUERY = "?page=FrontEndListTendersbyDate&service=page"
TABLE_ROW_SELECTORS = ["tr.even", "tr.odd"]
DETAIL_LINK_SELECTOR = "a[id^='DirectLink']"


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


def extract_tender_id(text: str) -> str:
    if not text:
        return ""
    patterns = [
        r'\[([^\]]+/[^" ]+)\]',
        r"\[([A-Z0-9_\-]{5,})\]",
        r"\b([A-Z]{2,6}[-/]?\d{2,10})\b",
        r"Tender\s*No\.?\s*[:\-]?\s*([A-Z0-9\-/]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return normalize_text(text)


def extract_value_from_detail(soup: BeautifulSoup) -> str:
    labels = [
        "estimated value",
        "tender value",
        "bid value",
        "contract value",
        "approx value",
        "price per",
    ]
    for cell in soup.select("td"):
        text = normalize_text(cell.text)
        lower = text.lower()
        if any(label in lower for label in labels) and len(lower) < 120:
            next_cell = cell.find_next_sibling("td")
            if next_cell:
                return normalize_text(next_cell.text)
            match = re.search(r"(₹|INR|Rs[\.]?)\s*[\d,\.]+", text)
            if match:
                return match.group(0)
    body_text = normalize_text(soup.get_text(separator=" ", strip=True))
    match = re.search(r"(?:₹|INR|Rs\.?)[\s]*[\d,.,,]+", body_text)
    return match.group(0) if match else ""


def parse_tender_rows(html: str, base_url: str, source_name: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: List[Dict[str, Any]] = []
    for selector in TABLE_ROW_SELECTORS:
        rows = soup.select(selector)
        if rows:
            break

    results: List[Dict[str, Any]] = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 5:
            continue
        title_anchor = cells[4].select_one("a")
        title_text = normalize_text(title_anchor.text if title_anchor else cells[4].text)
        title_text = title_text.strip("[] ")
        raw_info = normalize_text(cells[4].text)
        source_tender_id = extract_tender_id(raw_info)
        organisation_chain = normalize_text(cells[5].text if len(cells) > 5 else "")
        authority, category = (organisation_chain.split("||", 1) + [""])[:2]
        authority = authority.strip()
        category = category.strip()
        deadline = normalize_text(cells[2].text) if len(cells) > 2 else ""
        tender_url = urljoin(base_url, title_anchor["href"]) if title_anchor and title_anchor.has_attr("href") else base_url

        if not source_tender_id or not title_text or "view tender information" not in (title_anchor.get("title", "").lower() if title_anchor else ""):
            continue

        results.append(
            {
                "source": source_name,
                "source_tender_id": source_tender_id,
                "title": title_text,
                "authority": authority,
                "deadline": deadline,
                "estimated_value": "",
                "category": category,
                "region": "",
                "tender_url": tender_url,
                "pdf_urls": [],
                "raw_text": raw_info,
            }
        )
    return results


async def extract_detail_data(browser, detail_url: str) -> dict[str, Any]:
    page = await browser.new_page()
    try:
        await page.goto(detail_url, timeout=120000)
        await page.wait_for_load_state("networkidle")
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        pdf_urls = []
        for link in soup.select("a[href$='.pdf']"):
            href = link.get("href")
            if href:
                pdf_urls.append(urljoin(detail_url, href))
        return {
            "pdf_urls": pdf_urls,
            "estimated_value": extract_value_from_detail(soup),
        }
    except Exception as error:
        logger.warning("Failed to load tender detail page %s: %s", detail_url, error)
        return {"pdf_urls": [], "estimated_value": ""}
    finally:
        await page.close()


def build_list_url(root: str) -> str:
    if "page=" in root:
        return root
    return root.rstrip("/") + LIST_QUERY


async def scrape_procurement_portal(source_url: str | None = None) -> List[dict[str, Any]]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        try:
            for source in SOURCES:
                if source_url and source_url not in source["root"] and source_url != source["name"]:
                    continue
                list_url = build_list_url(source["root"])
                try:
                    page = await browser.new_page()
                    await page.goto(list_url, timeout=120000)
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_selector("tr.even, tr.odd", timeout=60000)
                    html = await page.content()
                    tenders = parse_tender_rows(html, list_url, source["name"])
                    if not tenders:
                        await page.close()
                        continue
                    results: List[dict[str, Any]] = []
                    for tender in tenders:
                        detail_data = await extract_detail_data(browser, tender["tender_url"])
                        tender["pdf_urls"] = detail_data.get("pdf_urls", [])
                        tender["estimated_value"] = detail_data.get("estimated_value", "")
                        results.append(tender)
                    await page.close()
                    if results:
                        return results
                except Exception as error:
                    logger.warning("Unable to scrape portal %s: %s", list_url, error)
                    continue
        finally:
            await browser.close()
    raise RuntimeError("Unable to scrape any procurement portal source")


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(scrape_procurement_portal()))
