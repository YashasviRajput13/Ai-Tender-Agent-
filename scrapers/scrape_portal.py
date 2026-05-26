import requests
from bs4 import BeautifulSoup


def fetch_portal(url: str) -> dict:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tenders = []
    for item in soup.select(".tender-item"):
        title = item.select_one(".title")
        deadline = item.select_one(".deadline")
        tenders.append({
            "title": title.text.strip() if title else "",
            "deadline": deadline.text.strip() if deadline else "",
        })
    return {"source": url, "tenders": tenders}


if __name__ == "__main__":
    site = "https://example.com/tenders"
    print(fetch_portal(site))
