#!/usr/bin/env python3
"""
TrendTrack.io Interactive Login Helper
Mở trình duyệt thật để người dùng đăng nhập tài khoản TrendTrack.io,
sau đó tự động lưu session cookies / tokens để Agent phân tích tab Meta chuẩn 1:1.
"""

import sys
import os
import time
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_FILE = os.path.join(BASE_DIR, "data_cache", "trendtrack_auth_state.json")

async def login():
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    
    print("=" * 65)
    print("🚀 KHỞI ĐỘNG TRÌNH DUYỆT ĐĂNG NHẬP TRENDTRACK.IO")
    print("=" * 65)
    print("👉 Trình duyệt Chrome sẽ xuất hiện trên màn hình máy tính của bạn.")
    print("👉 Hãy đăng nhập tài khoản TrendTrack.io của bạn vào cửa sổ đó.")
    print("👉 Ngay khi vào đến Dashboard, hệ thống sẽ tự động bắt lấy session!")
    print("=" * 65)

    async with async_playwright() as p:
        # Launch real visible browser on macOS
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--no-default-browser-check"]
        )
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        login_url = "https://app.trendtrack.io/en/login"
        print(f"🌐 Đang mở: {login_url}")
        await page.goto(login_url)

        print("\n⏳ Đang đợi bạn đăng nhập (tối đa 5 phút)...")
        logged_in = False
        start_time = time.time()

        while time.time() - start_time < 300:
            current_url = page.url.lower()
            # If redirected into the internal app dashboard
            if "app.trendtrack.io" in current_url and "login" not in current_url and "auth.trendtrack.io" not in current_url:
                logged_in = True
                break
            await asyncio.sleep(1)

        if logged_in:
            print("\n🎉 ĐĂNG NHẬP THÀNH CÔNG!")
            print(f"📍 URL hiện tại: {page.url}")
            await asyncio.sleep(2)  # Wait for all tokens/cookies to settle
            await context.storage_state(path=AUTH_FILE)
            print(f"✅ Đã lưu phiên đăng nhập vào: {AUTH_FILE}")
            print("🚀 Bây giờ bạn có thể chạy: python3 tools/inspect_trendtrack_meta.py")
        else:
            print("\n⚠️ Hết thời gian chờ đăng nhập (5 phút). Vui lòng chạy lại khi sẵn sàng.")

        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(login())
    except KeyboardInterrupt:
        print("\nĐã hủy bởi người dùng.")
        sys.exit(0)
