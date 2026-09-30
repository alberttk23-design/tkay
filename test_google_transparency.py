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

        async def on_response(response):
            if "rpc" in response.url:
                print("==> RPC URL:", response.url)
                try:
                    text = await response.text()
                    print("RPC RESP (len={}):".format(len(text)), text[:500])
                except Exception as e:
                    pass

        async def on_request(request):
            if "rpc" in request.url:
                print("--> RPC REQ:", request.url)
                print("PAYLOAD:", request.post_data[:300] if request.post_data else "None")

        page.on("request", on_request)
        page.on("response", on_response)

        print("Navigating to Dr. Squatch advertiser page...")
        await page.goto("https://adstransparency.google.com/advertiser/AR10925667841994653697?region=anywhere", wait_until="networkidle")
        await page.wait_for_timeout(5000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
