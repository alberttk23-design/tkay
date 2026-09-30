import asyncio
import json
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

test_brands = ["Ridge Wallet", "Gymshark", "Casetify", "Anker"]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("[*] Loading Google Ads Transparency via Headless Chrome...")
        await page.goto("https://adstransparency.google.com/?region=anywhere", wait_until="networkidle")
        print("[+] Base page loaded successfully! Title:", await page.title())

        # Test evaluating in-page fetch using the browser's own session/cookies
        for b in test_brands:
            print(f"\n--- Checking Brand: {b} ---")
            result = await page.evaluate("""async (brand) => {
                const url = 'https://adstransparency.google.com/anji/_/rpc/SearchService/SearchSuggestions?authuser=';
                const body = 'f.req=' + encodeURIComponent(JSON.stringify({
                    "1": brand,
                    "2": 5,
                    "3": 5,
                    "5": {"1": 1}
                }));
                const resp = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                    },
                    body: body
                });
                if (!resp.ok) {
                    return { status: resp.status, error: resp.statusText };
                }
                const data = await resp.json();
                return { status: resp.status, data: data };
            }""", b)

            status = result.get("status")
            print(f"Fetch HTTP Status: {status}")
            if status != 200:
                print("Error:", result)
                continue

            data = result.get("data", {})
            items = data.get("1", [])
            print(f"Suggestions count: {len(items)}")
            for it in items:
                if "1" in it:
                    adv = it["1"]
                    print(f"  -> Entity: {adv.get('1')} | ID: {adv.get('2')} | Country: {adv.get('3')}")
                elif "2" in it:
                    print(f"  -> Domain: {it['2'].get('1')}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
