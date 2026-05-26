from typing import Any, List

from playwright.async_api import async_playwright


async def scrape_cppt_portal(url: str) -> List[dict[str, Any]]:
    """Scrape a CPPP portal page and return standardized tender JSON."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        results: List[dict[str, Any]] = []
        rows = await page.locator(".tender-item").all()

        for row in rows:
            title = (await row.locator(".tender-title").text_content()) or ""
            authority = (await row.locator(".tender-authority").text_content()) or ""
            deadline = (await row.locator(".tender-deadline").text_content()) or ""
            estimated_value = (await row.locator(".tender-value").text_content()) or ""
            tender_id = (await row.locator(".tender-id").text_content()) or ""
            tender_url = (await row.locator("a").get_attribute("href")) or url
            pdf_links = await row.locator("a[href$='.pdf']").all()
            pdf_urls = [await link.get_attribute("href") or "" for link in pdf_links]

            results.append(
                {
                    "source": url,
                    "source_tender_id": tender_id.strip(),
                    "title": title.strip(),
                    "authority": authority.strip(),
                    "deadline": deadline.strip(),
                    "estimated_value": estimated_value.strip(),
                    "tender_url": tender_url,
                    "pdf_urls": [href for href in pdf_urls if href],
                }
            )

        await browser.close()
        return results


if __name__ == "__main__":
    import asyncio

    sample_url = "https://cppt.gov.in/tenders"
    print(asyncio.run(scrape_cppt_portal(sample_url)))
