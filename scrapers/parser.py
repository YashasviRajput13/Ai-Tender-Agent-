import re
from typing import Any, Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


def extract_text(element: Any) -> str:
    if element is None:
        return ""
    return normalize_text(element.get_text(separator=" ", strip=True))


def extract_best_text(row: Any, selectors: list[str], default: str = "") -> str:
    for selector in selectors:
        element = row.select_one(selector)
        text = extract_text(element)
        if text:
            return text
    return default


def extract_pdf_urls(row: Any, base_url: str) -> list[str]:
    pdf_urls = []
    for link in row.select("a[href$='.pdf']"):
        href = link.get("href")
        if href:
            pdf_urls.append(urljoin(base_url, href))
    return pdf_urls


def extract_tender_id(text: str) -> str:
    if not text:
        return ""
    match = re.search(r"\b([A-Z]{2,6}[-/]?\d{2,8})\b", text)
    if match:
        return match.group(1).strip()
    match = re.search(r"(Tender\s*No\.?\s*[:\-]?\s*[A-Z0-9\-/]+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


def extract_deadline(text: str) -> str:
    if not text:
        return ""
    date_match = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{1,2}-\d{1,2})\b", text)
    return date_match.group(1) if date_match else text.strip()


def find_anchor_candidates(soup: BeautifulSoup) -> List[Any]:
    anchors = soup.select("a[href]")
    candidates = []
    for anchor in anchors:
        href = anchor.get("href", "")
        if "tender" in href.lower() or "eprocure" in href.lower() or "publish" in href.lower():
            text = extract_text(anchor)
            if len(text) > 10:
                candidates.append(anchor)
    return candidates


def parse_tender_block(block: Any, base_url: str) -> Dict[str, Any]:
    title = extract_text(block.select_one("a[href]"))
    raw_text = extract_text(block)
    tender_id = extract_tender_id(raw_text)
    deadline = extract_deadline(raw_text)
    authority = extract_best_text(block, [".authority", ".org", ".department", "td:nth-of-type(2)"], "")
    category = extract_best_text(block, [".category", ".type", "td:nth-of-type(3)"], "")
    region = extract_best_text(block, [".region", ".state", ".location"], "")
    anchor = block.select_one("a[href]")
    tender_url = urljoin(base_url, anchor["href"]) if anchor and anchor.has_attr("href") else base_url
    pdf_urls = extract_pdf_urls(block, base_url)
    if not tender_id:
        tender_id = extract_tender_id(title)
    return {
        "source": base_url,
        "source_tender_id": tender_id,
        "title": title or "Untitled Tender",
        "authority": authority,
        "deadline": deadline,
        "estimated_value": "",
        "category": category,
        "region": region,
        "tender_url": tender_url,
        "pdf_urls": pdf_urls,
        "raw_text": raw_text,
    }


def parse_tender_listings(html: str, base_url: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")

    rows = []
    for selector in ["tr", "li", "div.tender", "div.product", "div.card", "table tbody tr"]:
        rows = soup.select(selector)
        if rows:
            break

    results: List[Dict[str, Any]] = []
    if not rows:
        anchors = find_anchor_candidates(soup)
        for anchor in anchors:
            block = anchor.find_parent(["div", "li", "tr", "td"]) or anchor
            item = parse_tender_block(block, base_url)
            if item["source_tender_id"] and item["title"]:
                results.append(item)
        return results

    for row in rows:
        item = parse_tender_block(row, base_url)
        if item["source_tender_id"] and item["title"]:
            results.append(item)

    return results
