from typing import Dict, List

from bs4 import BeautifulSoup


def parse_tender_html(html: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, 'html.parser')
    tenders = []
    for item in soup.select('.tender-item'):
        title = item.select_one('.tender-title')
        deadline = item.select_one('.tender-deadline')
        budget = item.select_one('.tender-budget')
        tenders.append({
            'title': title.text.strip() if title else '',
            'deadline': deadline.text.strip() if deadline else '',
            'budget': budget.text.strip() if budget else '',
            'raw_html': str(item),
        })
    return tenders


def normalize_tender_data(tenders: List[Dict[str, str]]) -> List[Dict[str, str]]:
    normalized = []
    for tender in tenders:
        normalized.append({
            'title': tender.get('title', ''),
            'deadline': tender.get('deadline', ''),
            'budget': tender.get('budget', ''),
            'summary': tender.get('title', ''),
        })
    return normalized
