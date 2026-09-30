#!/usr/bin/env python3
"""
TrendTrack Connector - Kết nối Playwright với Google Chrome
Tự động mở trình duyệt Chrome thật, lưu trữ phiên đăng nhập (session/cookies)
và đồng bộ dữ liệu từ app.trendtrack.io vào cache của tkay.
"""

import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "out", "spy_cache")
PROFILE_DIR = os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\ADMIN"), ".trendtrack_chrome_profile")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PROFILE_DIR, exist_ok=True)

def connect_trendtrack():
    print("=" * 65)
    print("🚀 KHỞI ĐỘNG KẾT NỐI PLAYWRIGHT VỚI GOOGLE CHROME THẬT")
    print("=" * 65)
    print(f"📁 Chrome Profile: {PROFILE_DIR}")
    print(f"💾 Thư mục Cache: {CACHE_DIR}")
    print("🌐 Đang mở: https://app.trendtrack.io ...")
    print("-" * 65)

    with sync_playwright() as p:
        # Mở Chrome thật với profile riêng biệt để không xung đột với tab đang mở
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-default-browser-check"
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Tự động bắt và lưu các API response từ trendtrack.io
        def handle_response(response):
            try:
                url = response.url
                if "trendtrack.io" in url and ("api" in url or "data" in url or "graphql" in url or "json" in response.headers.get("content-type", "")):
                    try:
                        data = response.json()
                        # Tự động trích xuất tên file nếu có
                        slug = url.split("?")[0].split("/")[-1] or "trendtrack_api"
                        save_path = os.path.join(CACHE_DIR, f"tt_sync_{slug}.json")
                        with open(save_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print(f"⚡ [AUTO-SYNC] Đã đồng bộ API response về: {os.path.basename(save_path)}")
                    except Exception:
                        pass
            except Exception:
                pass

        page.on("response", handle_response)

        try:
            page.goto("https://app.trendtrack.io", timeout=45000)
            page.wait_for_timeout(3000)

            print("\n" + "=" * 65)
            print("👉 CỬA SỔ CHROME ĐÃ ĐƯỢC MỞ TRÊN MÀN HÌNH.")
            print("1. Nếu bạn chưa đăng nhập, vui lòng đăng nhập tài khoản TrendTrack.")
            print("2. Phiên đăng nhập sẽ được lưu tự động cho các lần sau.")
            print("3. Bất kỳ trang nào bạn duyệt qua, dữ liệu API sẽ tự động được cào về cache!")
            print("=" * 65)

            # Giữ phiên chạy và kiểm tra định kỳ trạng thái URL
            print("\n⏳ Trình duyệt đang chạy... Nhấn Ctrl+C trong terminal khi muốn dừng.")
            while True:
                time.sleep(2)
                # Kiểm tra xem cửa sổ có bị đóng không
                if page.is_closed():
                    print("\n🛑 Người dùng đã đóng cửa sổ trình duyệt.")
                    break

        except KeyboardInterrupt:
            print("\n🛑 Đã dừng kết nối theo yêu cầu.")
        except Exception as e:
            print(f"\n⚠️ Lỗi kết nối: {e}")
        finally:
            context.close()

if __name__ == "__main__":
    connect_trendtrack()
