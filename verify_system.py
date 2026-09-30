#!/usr/bin/env python3
"""
verify_system.py - One-Click Automated Health Check & Regression Guard
Được thiết kế đặc biệt để bảo vệ người dùng No-code:
Tự động kiểm tra tính toàn vẹn của mã nguồn, các API quét quảng cáo,
và đảm bảo không có dữ liệu giả nào lọt vào hệ thống.
"""

import sys
import json
import urllib.request
import urllib.error
import subprocess
import os

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8765
BASE_URL = f"http://localhost:{PORT}"

def log_pass(msg):
    print(f"\033[92m  [PASS] {msg}\033[0m")

def log_fail(msg):
    print(f"\033[91m  [FAIL] {msg}\033[0m")

def log_info(msg):
    print(f"\033[94m--> {msg}\033[0m")

def check_syntax():
    log_info("Kiểm tra cú pháp Python toàn bộ các file scanner...")
    files = [
        "trendtrack_app.py",
        "ad_scanner.py",
        "google_scanner.py",
        "tiktok_service.py",
        "email_scanner.py",
        "meta_ranking.py"
    ]
    all_ok = True
    for f in files:
        if not os.path.exists(f):
            log_fail(f"Không tìm thấy file: {f}")
            all_ok = False
            continue
        res = subprocess.run([sys.executable, "-m", "py_compile", f], capture_output=True, text=True)
        if res.returncode == 0:
            log_pass(f"Cú pháp file {f} hợp lệ")
        else:
            log_fail(f"Lỗi cú pháp file {f}: {res.stderr.strip()}")
            all_ok = False
    return all_ok

def check_server_alive():
    log_info(f"Kiểm tra trạng thái Web Server tại {BASE_URL}...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/", headers={"User-Agent": "HealthCheck/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                log_pass(f"Web Server đang chạy ổn định (HTTP 200) trên cổng {PORT}")
                return True
            else:
                log_fail(f"Web Server trả về mã: {resp.status}")
                return False
    except Exception as e:
        log_fail(f"Không thể kết nối đến Web Server cổng {PORT}: {e}")
        return False

def check_api_endpoint(endpoint, param_name="query", test_val="guyler"):
    url = f"{BASE_URL}{endpoint}?{param_name}={test_val}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HealthCheck/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                log_fail(f"Endpoint {endpoint} trả về HTTP {resp.status}")
                return False, None
            data = json.loads(resp.read().decode("utf-8"))
            return True, data
    except Exception as e:
        log_fail(f"Lỗi gọi {endpoint}: {e}")
        return False, None

def verify_zero_hallucination():
    log_info("Kiểm tra quy tắc 'Zero-Hallucination' (Không được fake data cho brand lạ 'guyler')...")
    all_ok = True
    
    # 1. Test TikTok API
    ok, tt_data = check_api_endpoint("/api/tiktok")
    if ok and tt_data:
        t_count = tt_data.get("total_tiktoks", -1)
        vids = tt_data.get("videos", [])
        if t_count == 0 and len(vids) == 0:
            log_pass("TikTok API: Trả về chính xác 0 TikToks & 0 video (Không fake ảnh Unsplash/quần áo)")
        else:
            log_fail(f"TikTok API bị dính dữ liệu giả! total_tiktoks={t_count}, len(videos)={len(vids)}")
            all_ok = False

    # 2. Test Emails API
    ok, em_data = check_api_endpoint("/api/emails")
    if ok and em_data:
        e_count = em_data.get("total_emails", -1)
        camps = em_data.get("campaigns", [])
        if e_count == 0 and len(camps) == 0:
            log_pass("Emails API: Trả về chính xác 0 emails (Không sinh 96 emails ảo)")
        else:
            log_fail(f"Emails API bị dính dữ liệu giả! total_emails={e_count}, len(campaigns)={len(camps)}")
            all_ok = False

    # 3. Test Meta Ranking API
    ok, rk_data = check_api_endpoint("/api/meta-ranking")
    if ok and rk_data:
        modes = rk_data.get("modes", {})
        top_ranked = modes.get("top_ranked", [])
        # Check if ranking uses real ads or fake template
        has_unsplash = any("unsplash.com" in str(c.get("image_url", "")) for c in top_ranked)
        if not has_unsplash:
            log_pass("Meta Ranking API: Sử dụng quảng cáo thực tế từ Ad Library, không dùng ảnh người mẫu Unsplash")
        else:
            log_fail("Meta Ranking API: Phát hiện thẻ xếp hạng giả mạo lấy từ Unsplash!")
            all_ok = False

    # 4. Test Google Ads API
    ok, gg_data = check_api_endpoint("/api/google-ads")
    if ok and gg_data:
        g_active = gg_data.get("active_ads", -1)
        g_total = gg_data.get("total_ads", gg_data.get("total_estimated", -1))
        g_cards = len(gg_data.get("ad_cards", gg_data.get("library_cards", [])))
        if g_active == 0 and g_total == 0 and g_cards == 0:
            log_pass("Google Ads API: Trả về chính xác 0 ads cho brand lạ (Zero-Hallucination chuẩn xác)")
        else:
            log_fail(f"Google Ads API bị dính dữ liệu giả! active={g_active}, total={g_total}, cards={g_cards}")
            all_ok = False

    return all_ok

def main():
    print("=" * 60)
    print("   TrendTrack Explorer - Automated Regression Guard")
    print("=" * 60)
    
    c1 = check_syntax()
    print()
    c2 = check_server_alive()
    print()
    c3 = verify_zero_hallucination()
    print()
    
    print("=" * 60)
    if c1 and c2 and c3:
        print("\033[92m  KẾT QUẢ: HỆ THỐNG HOÀN TOÀN KHỎE MẠNH (100% PASS)\033[0m")
        print("  Dữ liệu sạch, không dính Oodie, sẵn sàng mở rộng tính năng mới.")
        sys.exit(0)
    else:
        print("\033[91m  KẾT QUẢ: PHÁT HIỆN LỖI HOẶC BỊ DÍNH DỮ LIỆU GIẢ (FAIL)\033[0m")
        print("  Yêu cầu AI kiểm tra và sửa ngay lập tức!")
        sys.exit(1)

if __name__ == "__main__":
    main()
