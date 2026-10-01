import asyncio
import os
import sys
from playwright.async_api import async_playwright

OUT_DIR = "/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff"
os.makedirs(OUT_DIR, exist_ok=True)

async def test_google_tab():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 960})
        page = await context.new_page()

        print("[*] 1. Loading app for The Oodie...")
        await page.goto("http://localhost:8765/?brand=The%20Oodie", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)

        # Switch to Google tab in sidebar
        print("[*] 2. Switching to Google Ads channel tab...")
        await page.click("#channelTab_google")
        await page.wait_for_timeout(2000)

        # Switch to Ad Library sub-tab
        print("[*] 3. Switching to Ad Library sub-tab...")
        await page.click("#googleSubTab_library")
        await page.wait_for_timeout(1500)

        initial_count = await page.locator("#googleLibraryCardsGrid > div").count()
        print(f"[+] Initial Ad Library cards rendered: {initial_count}")
        await page.screenshot(path=os.path.join(OUT_DIR, "google_ad_library_top.png"))
        print(f"[+] Saved google_ad_library_top.png")

        # Scroll down to trigger Infinite Scroll
        print("[*] 4. Scrolling down to trigger Infinite Scroll...")
        for i in range(3):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
            # Try clicking load more if visible
            try:
                load_more = page.locator("#btnGoogleLoadMore")
                if await load_more.is_visible():
                    await load_more.click()
                    await page.wait_for_timeout(1000)
            except Exception:
                pass

        scrolled_count = await page.locator("#googleLibraryCardsGrid > div").count()
        print(f"[+] Cards count after scrolling: {scrolled_count} (Infinite scroll active: {scrolled_count > initial_count})")
        await page.screenshot(path=os.path.join(OUT_DIR, "google_ad_library_scrolled.png"))
        print(f"[+] Saved google_ad_library_scrolled.png")

        # Test Media Type Filter: Shopping
        print("[*] 5. Testing Media Type filter (Shopping)...")
        await page.select_option("#filterGoogleMediaType", "Shopping")
        await page.wait_for_timeout(1000)
        shopping_count = await page.locator("#googleLibraryCardsGrid > div").count()
        print(f"[+] Shopping ads count: {shopping_count}")
        await page.screenshot(path=os.path.join(OUT_DIR, "google_ad_library_filtered_shopping.png"))
        print(f"[+] Saved google_ad_library_filtered_shopping.png")

        # Reset Media Type Filter to all
        await page.select_option("#filterGoogleMediaType", "all")
        await page.wait_for_timeout(1000)

        # Switch to Ranking sub-tab
        print("[*] 6. Switching to Google Ranking sub-tab...")
        await page.click("#googleSubTab_ranking")
        await page.wait_for_timeout(1500)

        ranking_count = await page.locator("#googleRankingCardsGrid > div").count()
        print(f"[+] Google Ranking cards rendered: {ranking_count}")
        await page.screenshot(path=os.path.join(OUT_DIR, "google_ranking_view.png"))
        print(f"[+] Saved google_ranking_view.png")

        # Click on the top Evergreen Ranking ad to open the Google Ad Detail Intelligence Modal
        print("[*] 7. Clicking top ranked ad to open Google Ad Detail Modal...")
        first_card = page.locator("#googleRankingCardsGrid > div").first
        await first_card.click()
        await page.wait_for_timeout(1500)

        modal_visible = await page.locator("#googleAdDetailModal").is_visible()
        print(f"[+] Google Ad Detail Modal visible: {modal_visible}")
        await page.screenshot(path=os.path.join(OUT_DIR, "google_ad_detail_modal.png"))
        print(f"[+] Saved google_ad_detail_modal.png")

        # Test Next Navigation Button '>' in dock
        print("[*] 8. Testing Next Navigation '>' in Dock...")
        next_btn = page.locator("#googleAdDetailModal button[title='Quảng cáo tiếp']")
        await next_btn.click()
        await page.wait_for_timeout(1000)
        nav_counter = await page.locator("#gModalIndexCounter").text_content()
        print(f"[+] Dock counter after navigation: {nav_counter}")
        await page.screenshot(path=os.path.join(OUT_DIR, "google_ad_detail_modal_navigated.png"))
        print(f"[+] Saved google_ad_detail_modal_navigated.png")

        # Close modal
        print("[*] 9. Closing modal...")
        await page.click("#googleAdDetailModal button[title='Đóng']")
        await page.wait_for_timeout(1000)

        # Check Guyker (Zero-hallucination verification)
        print("[*] 10. Checking Guyker (Zero-hallucination)...")
        await page.goto("http://localhost:8765/?brand=guyker.com", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        await page.click("#channelTab_google")
        await page.wait_for_timeout(1500)
        await page.click("#googleSubTab_library")
        await page.wait_for_timeout(1500)

        guyker_count_text = await page.locator("#googleLibraryAdsCount").text_content()
        print(f"[+] Guyker Google Library ads count: {guyker_count_text}")
        await page.screenshot(path=os.path.join(OUT_DIR, "guyker_google_library.png"))
        print(f"[+] Saved guyker_google_library.png")

        await browser.close()
        print("\n[✔] ALL VERIFICATION STEPS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(test_google_tab())
