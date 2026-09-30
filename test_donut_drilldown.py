import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        
        # 1. Open app & switch to Google Ads Intelligence
        await page.goto('http://localhost:8765', wait_until='domcontentloaded')
        await page.wait_for_timeout(2500)
        await page.evaluate("""() => {
            if (typeof switchShopSubTab === 'function') switchShopSubTab('google');
        }""")
        await page.wait_for_timeout(2000)
        
        # Screenshot 1: Main bottom section (matching Image 1)
        await page.screenshot(path='verify_bottom_section.png')
        print("[+] Screenshot 1: verify_bottom_section.png")
        
        # 2. Click on Format Mix Donut to trigger the Drilldown Modal
        await page.evaluate("""() => {
            if (typeof openGoogleDonutModal === 'function') {
                openGoogleDonutModal('format', 'Text');
            }
        }""")
        await page.wait_for_timeout(1000)
        
        # Screenshot 2: Donut Drilldown Modal (matching Image 2)
        await page.screenshot(path='verify_donut_modal.png')
        print("[+] Screenshot 2: verify_donut_modal.png")
        
        await b.close()

asyncio.run(run())
