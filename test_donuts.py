from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    page.goto('http://localhost:8765', wait_until='domcontentloaded')
    page.wait_for_timeout(2000)
    page.evaluate('switchShopSubTab("google")')
    page.wait_for_timeout(2500)
    
    # 1. Screenshot default donuts
    donut_card = page.locator('.lg\\:col-span-5.space-y-6')
    donut_card.screenshot(path='check_donuts_default_final.png')
    print('1. Screenshot check_donuts_default_final.png saved')
    
    # 2. Hover over Image in Format Mix legend
    image_legend = page.locator('#formatLegendItem_1')
    image_legend.hover()
    page.wait_for_timeout(500)
    donut_card.screenshot(path='check_donuts_hover_image_final.png')
    print('2. Screenshot check_donuts_hover_image_final.png saved')
    
    # 3. Hover over Search in Platform Mix legend
    search_legend = page.locator('#platformLegendItem_0')
    search_legend.hover()
    page.wait_for_timeout(500)
    donut_card.screenshot(path='check_donuts_hover_search_final.png')
    print('3. Screenshot check_donuts_hover_search_final.png saved')

    browser.close()
