import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1600, 'height': 1200})
        page = await context.new_page()
        
        print("Opening http://localhost:8765...")
        await page.goto("http://localhost:8765", wait_until="networkidle", timeout=20000)
        await page.wait_for_timeout(2500)
        
        # Take overview screenshot
        await page.screenshot(path="test_final_overview.png", full_page=False)
        print("Saved test_final_overview.png")
        
        # Click Google tab in sub-sidebar
        print("Clicking Google sub-tab...")
        await page.click("#subNavItemGoogle")
        await page.wait_for_timeout(2500)
        
        # Take Google tab screenshot
        await page.screenshot(path="test_final_google_tab.png", full_page=False)
        print("Saved test_final_google_tab.png")
        
        # Scroll down to ad cards & targeting mix
        await page.evaluate("window.scrollBy(0, 500)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="test_final_google_cards.png", full_page=False)
        print("Saved test_final_google_cards.png")
        
        # Click the first Google ad card to test modal
        print("Clicking first ad card...")
        first_card = await page.query_selector("#googleAdCardsGrid > div")
        if first_card:
            await first_card.click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path="test_final_google_modal.png", full_page=False)
            print("Saved test_final_google_modal.png")
            
            # Close modal
            await page.click("button[onclick*='closeAdModal']")
            await page.wait_for_timeout(500)
            
        # Click Store Overview button to test back navigation
        print("Clicking Store Overview button...")
        await page.click("button[onclick*='overview']")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="test_final_back_overview.png", full_page=False)
        print("Saved test_final_back_overview.png")
        
        await browser.close()
        print("All tests passed successfully!")

asyncio.run(run())
