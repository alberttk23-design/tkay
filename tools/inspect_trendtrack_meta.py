#!/usr/bin/env python3
"""
TrendTrack.io Meta Tab Inspector & Reverse Engineering Tool
Sử dụng authenticated session để phân tích chi tiết:
- Network API calls (Payloads, response JSON, batching)
- Cấu trúc Tab Meta (Ad Library, Ranking, Insights, Contents)
- Cơ chế Infinite Scroll & Filters
"""

import sys
import os
import json
import time
import asyncio
import argparse
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_FILE = os.path.join(BASE_DIR, "data_cache", "trendtrack_auth_state.json")
DUMP_DIR = os.path.join(BASE_DIR, "data_cache", "trendtrack_meta_api_dumps")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "data_cache", "trendtrack_meta_screenshots")

async def inspect(brand_url: str = None, headless: bool = True):
    if not os.path.exists(AUTH_FILE):
        print("❌ Chưa tìm thấy phiên đăng nhập!")
        print("👉 Hãy chạy: python3 tools/login_trendtrack.py để đăng nhập trước.")
        sys.exit(1)

    os.makedirs(DUMP_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    print("=" * 65)
    print("🕵️ KHỞI ĐỘNG CÔNG CỤ PHÂN TÍCH TAB META TRENDTRACK.IO")
    print("=" * 65)

    captured_apis = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            storage_state=AUTH_FILE,
            viewport={"width": 1440, "height": 900}
        )
        page = await context.new_page()

        # Intercept and log all XHR/Fetch API responses
        async def on_response(response):
            url = response.url
            if any(k in url.lower() for k in ["/api/", "graphql", "ads", "meta", "tracking", "insights", "ranking"]):
                try:
                    ctype = response.headers.get("content-type", "")
                    if "application/json" in ctype:
                        body = await response.json()
                        clean_name = url.split("?")[0].split("/")[-1] or "api_response"
                        fname = f"{int(time.time()*1000)}_{clean_name}.json"
                        out_path = os.path.join(DUMP_DIR, fname)
                        with open(out_path, "w", encoding="utf-8") as f:
                            json.dump({
                                "url": url,
                                "status": response.status,
                                "data": body
                            }, f, ensure_ascii=False, indent=2)
                        print(f"📥 [API CAPTURED] {url[:80]}... -> {fname}")
                        captured_apis.append({"url": url, "file": fname})
                except Exception:
                    pass

        page.on("response", on_response)

        target = brand_url or "https://app.trendtrack.io/en/brands"
        print(f"🌐 Đang điều hướng đến: {target}")
        await page.goto(target, wait_until="networkidle")
        await asyncio.sleep(3)

        # Chụp màn hình trang chủ / danh sách
        ss_home = os.path.join(SCREENSHOT_DIR, "01_initial_landing.png")
        await page.screenshot(path=ss_home, full_page=False)
        print(f"📸 Đã chụp: {ss_home}")

        # Thử tìm và click vào shop đầu tiên hoặc shop theoodie nếu ở trang brands
        shop_link = await page.query_selector("a[href*='/brand/'], a[href*='/shop/'], a[href*='/stores/']")
        if shop_link:
            shop_href = await shop_link.get_attribute("href")
            print(f"👉 Tìm thấy store: {shop_href}, đang mở...")
            await shop_link.click()
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)

        # Chụp trang chi tiết store
        ss_store = os.path.join(SCREENSHOT_DIR, "02_store_overview.png")
        await page.screenshot(path=ss_store, full_page=False)
        print(f"📸 Đã chụp: {ss_store}")

        # Tìm và click tab Meta Ads
        meta_tab = await page.query_selector("button:has-text('Meta'), a:has-text('Meta'), [data-tab*='meta']")
        if meta_tab:
            print("👉 Đang chuyển sang tab Meta Ads...")
            await meta_tab.click()
            await asyncio.sleep(3)
            ss_meta = os.path.join(SCREENSHOT_DIR, "03_meta_tab_default.png")
            await page.screenshot(path=ss_meta, full_page=False)
            print(f"📸 Đã chụp: {ss_meta}")

            # Thử cuộn trang (Infinite Scroll)
            print("📜 Đang mô phỏng cuộn chuột (Scroll) để kiểm tra tải thêm ads...")
            for i in range(3):
                await page.evaluate("window.scrollBy(0, 1200)")
                await asyncio.sleep(2)
                print(f"  └─ Đã cuộn lần {i+1}...")

            ss_scroll = os.path.join(SCREENSHOT_DIR, "04_meta_after_scroll.png")
            await page.screenshot(path=ss_scroll, full_page=False)
            print(f"📸 Đã chụp sau khi cuộn: {ss_scroll}")

        print("=" * 65)
        print(f"✅ HOÀN TẤT PHÂN TÍCH! Đã bắt được {len(captured_apis)} API requests.")
        print(f"📁 Dữ liệu JSON API lưu tại: {DUMP_DIR}")
        print(f"🖼️ Ảnh chụp màn hình lưu tại: {SCREENSHOT_DIR}")
        print("=" * 65)

        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TrendTrack Meta Inspector")
    parser.add_argument("--url", type=str, help="Specific brand URL on trendtrack")
    parser.add_argument("--no-headless", action="store_true", help="Run with visible browser")
    args = parser.parse_args()

    asyncio.run(inspect(brand_url=args.url, headless=not args.no_headless))
