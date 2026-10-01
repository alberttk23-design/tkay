import os
import sys
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\ADMIN\.gemini\antigravity\brain\9b4d6b42-afc0-4371-93ae-8013d8f961e8"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using 1500px width so all 6 columns in lg:grid-cols-6 are fully rendered
        context = browser.new_context(viewport={"width": 1500, "height": 950})
        page = context.new_page()

        print("Navigating to http://localhost:8765...")
        page.goto("http://localhost:8765", wait_until="networkidle", timeout=30000)
        time.sleep(2)

        print("Loading loopearplugs.com...")
        page.evaluate("async () => { await loadBrand('loopearplugs.com'); }")
        time.sleep(4)

        # 1. Meta Ad Library (6 columns)
        print("Capturing Meta Ad Library (6 cols)...")
        page.click("#subNavItemMeta")
        time.sleep(1)
        # Ensure Ad Library sub-tab
        try:
            page.click("#metaSubTabBtn_library")
        except Exception:
            pass
        time.sleep(2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loop_meta_library_6col.png"), full_page=False)

        # 2. TikTok Tab
        print("Capturing TikTok Tab (7,043 ads)...")
        page.click("#subNavItemTiktok")
        time.sleep(2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loop_tiktok_7043.png"), full_page=False)

        # 3. Email Tab
        print("Capturing Email Tab (118 emails)...")
        page.click("#subNavItemEmails")
        time.sleep(2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loop_emails_118.png"), full_page=False)

        # 4. Google Ads Tab
        print("Capturing Google Ads Tab (6,082 ads)...")
        page.click("#subNavItemGoogle")
        time.sleep(2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "test_loop_google_6082.png"), full_page=False)

        browser.close()
        print("All tabs for Loop Earplugs captured successfully!")

if __name__ == "__main__":
    run()
