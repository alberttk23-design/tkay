import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        await page.goto("http://localhost:8765", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        # Click search or switch to Google tab directly
        # In header strip: click Google channel pill
        await page.evaluate("""() => {
            if (typeof switchShopSubTab === 'function') {
                switchShopSubTab('google');
            }
        }""")
        await page.wait_for_timeout(2000)
        
        # Take screenshot of the Google tab top row (Historic + Format/Platform Mix + Targeted Countries)
        await page.screenshot(path="verify_google_matched.png", full_page=False)
        print("[+] Captured verify_google_matched.png")
        
        # Extract DOM values to verify
        stats = await page.evaluate("""() => {
            return {
                shopName: document.getElementById('googleShopName')?.textContent,
                advName: document.getElementById('googleAdvName')?.textContent,
                ratio: document.getElementById('googleAdRatio')?.textContent,
                histActive: document.getElementById('googleHistoricActive')?.textContent,
                histTotal: document.getElementById('googleHistoricTotal')?.textContent,
                formatTotal: document.getElementById('googleFormatMixTotal')?.textContent,
                platformTotal: document.getElementById('googlePlatformMixTotal')?.textContent,
                countries: document.getElementById('googleTargetedCountriesList')?.innerText
            };
        }""")
        print("[+] Verified UI values:")
        for k, v in stats.items():
            print(f"    - {k}: {v}")
            
        await browser.close()

asyncio.run(run())
