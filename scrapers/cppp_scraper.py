from typing import List

from playwright.async_api import async_playwright

async def scrape_cppp_portal(url: str) -> List[dict]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state('networkidle')

        tenders = await page.locator('.tender-item').all_text_contents()
        results = []
        for raw in tenders:
            results.append({
                'source': url,
                'raw_text': raw,
            })

        await browser.close()
        return results


if __name__ == '__main__':
    import asyncio

    test_url = 'https://example.com/tenders'
    data = asyncio.run(scrape_cppp_portal(test_url))
    print(data)
