import asyncio
import json
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        async def on_request(request):
            if "rpc" in request.url or "anji" in request.url:
                print("REQ:", request.url)
                if request.post_data:
                    print("POST:", request.post_data[:200])

        async def on_response(response):
            if "rpc" in response.url or "anji" in response.url:
                try:
                    text = await response.text()
                    print("RESP from:", response.url, "len:", len(text), "preview:", text[:200])
                except:
                    pass

        page.on("request", on_request)
        page.on("response", on_response)

        print("Navigating...")
        await page.goto("https://adstransparency.google.com/advertiser/AR10925667841994653697?region=anywhere", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Find creative card
        cards = await page.query_selector_all("creative-preview, .creative__preview, [role='listitem'], a[href*='creative']")
        print(f"Found {len(cards)} card elements")
        
        # Click on the first creative preview if found
        if cards:
            await cards[0].click()
            await page.wait_for_timeout(4000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
