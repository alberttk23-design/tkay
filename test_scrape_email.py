from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    )
    try:
        resp = page.goto('https://milled.com/@theoodie', timeout=20000, wait_until='domcontentloaded')
        print(f"Status: {resp.status if resp else 'No resp'}")
        page.wait_for_timeout(3000)
        title = page.title()
        print(f"Title: {title}")
        
        # Extract email cards
        emails = page.evaluate("""() => {
            const items = [];
            document.querySelectorAll('.email-card, .card, article, [data-email-id], .grid a').forEach(el => {
                const img = el.querySelector('img');
                const text = el.innerText;
                const link = el.getAttribute('href') || (el.querySelector('a') ? el.querySelector('a').getAttribute('href') : '');
                if (img && (img.src || img.dataset.src)) {
                    items.push({
                        img: img.src || img.dataset.src,
                        text: text.trim().substring(0, 100),
                        link: link
                    });
                }
            });
            return items;
        }""")
        print(f"Found {len(emails)} items")
        if emails:
            print("First 3 items:", emails[:3])
            
        page.screenshot(path='milled_page.png')
        print("Screenshot saved to milled_page.png")
    except Exception as e:
        print("Error:", e)
    browser.close()
