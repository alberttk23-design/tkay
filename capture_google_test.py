import os
import sys
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\ADMIN\.gemini\antigravity\brain\9b4d6b42-afc0-4371-93ae-8013d8f961e8"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("Navigating to http://localhost:8765...")
        page.goto("http://localhost:8765", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # 1. Load The Oodie by calling loadBrand or clicking hot preset
        print("Loading The Oodie brand...")
        page.evaluate("async () => { await loadBrand('The Oodie'); }")
        time.sleep(3)

        # Switch to Google tab
        print("Switching to Google Ads subnav...")
        page.click("#subNavItemGoogle")
        time.sleep(2)

        # Ensure Insights is selected
        page.click("#googleSubTab_insights")
        time.sleep(1.5)

        # Capture Top Insights
        print("Capturing Google Insights Top for The Oodie...")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_google_insights_top.png"), full_page=False)

        # Scroll to bottom of Insights
        print("Capturing Google Insights Bottom for The Oodie...")
        page.evaluate("window.scrollTo(0, 680)")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_google_insights_bottom.png"), full_page=False)

        # 2. Switch to Ad Library sub-tab
        print("Switching to Ad Library sub-tab...")
        page.evaluate("window.scrollTo(0, 0)")
        page.click("#googleSubTab_library")
        time.sleep(2)
        print("Capturing Google Ad Library for The Oodie...")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_google_library.png"), full_page=False)

        # 3. Switch to Ranking sub-tab
        print("Switching to Ranking sub-tab...")
        page.click("#googleSubTab_ranking")
        time.sleep(2)
        print("Capturing Google Ranking for The Oodie...")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_google_ranking.png"), full_page=False)

        # 4. Search LoopEarplugs.com
        print("Loading loopearplugs.com...")
        page.evaluate("window.scrollTo(0, 0)")
        page.evaluate("async () => { await loadBrand('loopearplugs.com'); }")
        time.sleep(4)

        # Ensure Google tab is visible for Loop
        page.click("#subNavItemGoogle")
        page.click("#googleSubTab_insights")
        time.sleep(2)
        print("Capturing Loop Earplugs Google Ads...")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loopearplugs_google.png"), full_page=False)

        # Switch to Meta tab for Loop Earplugs
        print("Capturing Loop Earplugs Meta Ads...")
        page.click("#subNavItemMeta")
        time.sleep(2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loopearplugs_meta.png"), full_page=False)

        # Switch to Overview tab for Loop Earplugs
        print("Capturing Loop Earplugs Overview...")
        page.click("#subNavItemOverview")
        time.sleep(2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loopearplugs_overview.png"), full_page=False)

        browser.close()
        print("All visual screenshots captured successfully!")

if __name__ == "__main__":
    run()
