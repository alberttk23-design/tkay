import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\ADMIN\.gemini\antigravity\brain\9b4d6b42-afc0-4371-93ae-8013d8f961e8"
screenshot_path = os.path.join(artifact_dir, "test_drsquatch_ad_library_clean.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    page.goto('http://localhost:8765/?query=drsquatch.com', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Make sure we are on Meta tab
    page.evaluate('switchShopSubTab("meta")')
    page.wait_for_timeout(2000)

    # Check header brand name and ads count
    brand_title = page.locator('#metaHeaderBrandName').inner_text()
    ads_count = page.locator('#metaHeaderAdsCount').inner_text()
    print(f"Brand Title: '{brand_title}'")
    print(f"Ads Count: '{ads_count}'")

    # Check cards
    cards = page.locator('#metaLibraryCardsGrid .tt-card')
    card_count = cards.count()
    print(f"Total cards rendered on page 1: {card_count}")

    # Check text inside all cards for any illegal 'loop' hardcoding
    has_loop_leak = False
    for i in range(min(card_count, 12)):
        card_text = cards.nth(i).inner_text()
        card_html = cards.nth(i).inner_html()
        if "loop" in card_text.lower() or "loop" in card_html.lower():
            # Check if it's the brand loop
            print(f"WARNING: Card {i} mentions 'loop'!")
            has_loop_leak = True
        if "110.1k" in card_text.lower():
            print(f"WARNING: Card {i} has hardcoded Loop reach/spend 110.1K!")
            has_loop_leak = True
        if "loopearplugs" in card_html.lower():
            print(f"WARNING: Card {i} has loopearplugs link/domain!")
            has_loop_leak = True

    if not has_loop_leak:
        print("SUCCESS: Zero Loop leaks detected across Dr. Squatch cards!")
    else:
        print("FAIL: Loop leak detected!")

    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    browser.close()
