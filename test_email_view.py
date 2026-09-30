from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 900})
    page.goto('http://localhost:8765', wait_until='domcontentloaded')
    page.wait_for_timeout(2000)

    # 1. Switch to Emails tab
    page.evaluate('switchShopSubTab("emails")')
    page.wait_for_timeout(2000)

    # 2. Screenshot main Email Library view
    page.screenshot(path='verify_email_library.png')
    print('1. Screenshot verify_email_library.png saved')

    # 3. Click first email card (Beetlejuice) to open detail modal
    cards = page.locator('#emailCardsGrid > div')
    count = cards.count()
    print(f'Rendered {count} email cards')
    if count > 0:
        cards.first.click()
        page.wait_for_timeout(1000)
        page.screenshot(path='verify_email_modal.png')
        print('2. Screenshot verify_email_modal.png saved')
        
        # Close modal
        close_btn = page.locator('#emailDetailModal button[title="Close"]')
        close_btn.click()
        page.wait_for_timeout(500)

    # 4. Switch to Insights sub-tab
    page.evaluate('switchEmailSubTab("insights")')
    page.wait_for_timeout(500)
    page.screenshot(path='verify_email_insights.png')
    print('3. Screenshot verify_email_insights.png saved')

    # 5. Switch to Calendar sub-tab
    page.evaluate('switchEmailSubTab("calendar")')
    page.wait_for_timeout(500)
    page.screenshot(path='verify_email_calendar.png')
    print('4. Screenshot verify_email_calendar.png saved')

    # 6. Switch to Flows sub-tab
    page.evaluate('switchEmailSubTab("flows")')
    page.wait_for_timeout(500)
    page.screenshot(path='verify_email_flows.png')
    print('5. Screenshot verify_email_flows.png saved')

    browser.close()
