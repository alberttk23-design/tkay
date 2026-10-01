import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\ADMIN\.gemini\antigravity\brain\9b4d6b42-afc0-4371-93ae-8013d8f961e8"
screenshot_path = os.path.join(artifact_dir, "test_loopearplugs_ad_library.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    page.goto('http://localhost:8765/?query=loopearplugs.com', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Meta tab
    page.evaluate('switchShopSubTab("meta")')
    page.wait_for_timeout(2000)

    brand_title = page.locator('#metaHeaderBrandName').inner_text()
    ads_count = page.locator('#metaHeaderAdsCount').inner_text()
    print(f"Loop Earplugs Brand Title: '{brand_title}'")
    print(f"Loop Earplugs Ads Count: '{ads_count}'")

    cards = page.locator('#metaLibraryCardsGrid .tt-card')
    card_count = cards.count()
    print(f"Loop cards rendered: {card_count}")

    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    browser.close()
