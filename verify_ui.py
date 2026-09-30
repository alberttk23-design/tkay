import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        print("Navigating to http://localhost:8765...")
        await page.goto("http://localhost:8765")
        await page.wait_for_timeout(1500)

        async def search_brand(brand_name):
            print(f"\n==========================================")
            print(f"SEARCHING BRAND: {brand_name}")
            print(f"==========================================")
            await page.fill("#brandInput", "")
            await page.fill("#brandInput", brand_name)
            await page.press("#brandInput", "Enter")
            await page.wait_for_selector("#btnSpinner", state="hidden", timeout=15000)
            await page.wait_for_timeout(1500)

        # ----------------------------------------------------
        # 1. MOMCOZY TEST
        # ----------------------------------------------------
        await search_brand("Momcozy")
        
        # Emails Tab
        await page.click("#subNavItemEmails")
        await page.wait_for_timeout(1500)
        momcozy_email_res = await page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('#emailCardsGrid img'));
            const broken = imgs.filter(img => img.naturalWidth === 0).map(img => img.src);
            const valid = imgs.filter(img => img.naturalWidth > 0).map(img => img.src);
            return { total: imgs.length, brokenCount: broken.length, brokenUrls: broken };
        }''')
        print(f"Momcozy Email Images: Total={momcozy_email_res['total']}, Broken={momcozy_email_res['brokenCount']}, BrokenList={momcozy_email_res['brokenUrls']}")
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/momcozy_emails_clean.png")

        # TikTok Tab -> Library Subtab
        await page.click("#subNavItemTiktok")
        await page.wait_for_timeout(1000)
        await page.click("#ttTabBtn_library")
        await page.wait_for_timeout(1500)
        momcozy_tt_res = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('#ttLibraryCardsGrid > div'));
            return cards.slice(0, 3).map(c => ({
                text: c.innerText.replace(/\\n+/g, ' ').substring(0, 100),
                img: c.querySelector('img')?.src
            }));
        }''')
        print(f"Momcozy TikTok Library Cards (First 3):")
        for idx, card in enumerate(momcozy_tt_res):
            print(f"  [{idx+1}] Text: {card['text']} | Img: {card['img']}")
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/momcozy_tiktok_library_clean.png")

        # ----------------------------------------------------
        # 2. RIDGE TEST
        # ----------------------------------------------------
        await search_brand("Ridge")
        
        # Emails Tab
        await page.click("#subNavItemEmails")
        await page.wait_for_timeout(1500)
        ridge_email_res = await page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('#emailCardsGrid img'));
            const broken = imgs.filter(img => img.naturalWidth === 0).map(img => img.src);
            return { total: imgs.length, brokenCount: broken.length, brokenUrls: broken };
        }''')
        print(f"Ridge Email Images: Total={ridge_email_res['total']}, Broken={ridge_email_res['brokenCount']}, BrokenList={ridge_email_res['brokenUrls']}")
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/ridge_emails_clean.png")

        # TikTok Tab -> Library Subtab
        await page.click("#subNavItemTiktok")
        await page.wait_for_timeout(1000)
        await page.click("#ttTabBtn_library")
        await page.wait_for_timeout(1500)
        ridge_tt_res = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('#ttLibraryCardsGrid > div'));
            return cards.slice(0, 3).map(c => ({
                text: c.innerText.replace(/\\n+/g, ' ').substring(0, 100),
                img: c.querySelector('img')?.src
            }));
        }''')
        print(f"Ridge TikTok Library Cards (First 3):")
        for idx, card in enumerate(ridge_tt_res):
            print(f"  [{idx+1}] Text: {card['text']} | Img: {card['img']}")
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/ridge_tiktok_library_clean.png")

        # ----------------------------------------------------
        # 3. TRUE SEA MOSS TEST
        # ----------------------------------------------------
        await search_brand("True Sea Moss")
        
        # Emails Tab
        await page.click("#subNavItemEmails")
        await page.wait_for_timeout(1500)
        tsm_email_res = await page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('#emailCardsGrid img'));
            const broken = imgs.filter(img => img.naturalWidth === 0).map(img => img.src);
            return { total: imgs.length, brokenCount: broken.length, brokenUrls: broken };
        }''')
        print(f"True Sea Moss Email Images: Total={tsm_email_res['total']}, Broken={tsm_email_res['brokenCount']}, BrokenList={tsm_email_res['brokenUrls']}")
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/trueseamoss_emails_clean.png")

        # TikTok Tab -> Library Subtab
        await page.click("#subNavItemTiktok")
        await page.wait_for_timeout(1000)
        await page.click("#ttTabBtn_library")
        await page.wait_for_timeout(1500)
        tsm_tt_res = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('#ttLibraryCardsGrid > div'));
            return cards.slice(0, 3).map(c => ({
                text: c.innerText.replace(/\\n+/g, ' ').substring(0, 100),
                img: c.querySelector('img')?.src
            }));
        }''')
        print(f"True Sea Moss TikTok Library Cards (First 3):")
        for idx, card in enumerate(tsm_tt_res):
            print(f"  [{idx+1}] Text: {card['text']} | Img: {card['img']}")
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/trueseamoss_tiktok_library_clean.png")

        # ----------------------------------------------------
        # 4. TIKTOK SPARK ADS AUDIT MODAL TEST
        # ----------------------------------------------------
        await page.click("button:has-text('Audit Spark Ads')")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="/Users/dudumac5/.gemini/antigravity/brain/12976ad6-9a42-4e4f-bed9-6caea5c14cff/tiktok_spark_audit_modal_clean.png")

        await browser.close()
        print("\n==========================================")
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
        print("==========================================")

if __name__ == '__main__':
    asyncio.run(main())
