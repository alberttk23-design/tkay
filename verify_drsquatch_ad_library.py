import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\ADMIN\.gemini\antigravity\brain\9b4d6b42-afc0-4371-93ae-8013d8f961e8"
screenshot_path = os.path.join(artifact_dir, "test_drsquatch_ad_library_perfect.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    page.goto('http://localhost:8765/?query=drsquatch.com', wait_until='networkidle')
    page.wait_for_timeout(2000)

    # Make sure we are on Meta tab
    page.evaluate('switchShopSubTab("meta")')
    page.wait_for_timeout(2000)

    # Capture screenshot first
    page.screenshot(path=screenshot_path)
    print("Screenshot saved to:", screenshot_path)

    # Check header brand name, ads count, reach toggle
    brand_title = page.locator('#metaHeaderBrandName').inner_text()
    ads_count = page.locator('#metaHeaderAdsCount').inner_text()
    reach_label = page.locator('#metaHeaderEuUkLabel').inner_text()
    header_avatar_src = page.locator('#metaHeaderBrandAvatar').get_attribute('src')
    print("Brand Title:", brand_title.encode('ascii', 'ignore').decode())
    print("Ads Count:", ads_count.encode('ascii', 'ignore').decode())
    print("Reach Label:", reach_label.encode('ascii', 'ignore').decode())
    print("Header Avatar Src:", header_avatar_src)

    # Check cards
    cards = page.locator('#metaLibraryCardsGrid .tt-card')
    card_count = cards.count()
    print("Total cards rendered on page 1:", card_count)

    browser.close()
