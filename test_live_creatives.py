import asyncio
import json
import sys
from datetime import datetime
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

test_targets = [
    {"name": "The Ridge Wallet", "adv_id": "AR14056452383756517377"},
    {"name": "Gymshark Ltd", "adv_id": "AR05501100765344694273"},
    {"name": "Casetify", "domain": "casetify.com"}
]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("[*] Navigating to Google Ads Transparency...")
        await page.goto("https://adstransparency.google.com/?region=anywhere", wait_until="networkidle")

        for target in test_targets:
            name = target["name"]
            print(f"\n==========================================")
            print(f"[*] FETCHING LIVE ADS CHO: {name}")
            
            adv_id = target.get("adv_id")
            domain = target.get("domain")

            result = await page.evaluate("""async (args) => {
                const [advId, domain] = args;
                const url = 'https://adstransparency.google.com/anji/_/rpc/SearchService/SearchCreatives?authuser=';
                
                let filterObj = {};
                if (advId) {
                    filterObj = {
                        "12": {"1": "", "2": true},
                        "13": {"1": [advId]}
                    };
                } else {
                    filterObj = {
                        "12": {"1": domain, "2": true}
                    };
                }

                const payload = {
                    "2": 20,
                    "3": filterObj,
                    "7": {"1": 1, "2": 0, "3": 2704}
                };

                const resp = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
                    body: 'f.req=' + encodeURIComponent(JSON.stringify(payload))
                });

                if (!resp.ok) return { status: resp.status, error: resp.statusText };
                const data = await resp.json();
                return { status: resp.status, data: data };
            }""", [adv_id, domain])

            status = result.get("status")
            if status != 200:
                print(f"[-] Lỗi HTTP: {status} - {result.get('error')}")
                continue

            data = result.get("data", {})
            creatives = data.get("1", [])
            count_min = data.get("4", "N/A")
            count_max = data.get("5", "N/A")

            print(f"[+] HTTP Status: {status} (Thành công)")
            print(f"[+] Tổng số lượng Ads Google đang lưu trữ: {count_min} - {count_max} ads")
            print(f"[+] Số Ads tải về: {len(creatives)}")

            # Thống kê format thực tế
            formats = {"Image (Banner)": 0, "Text (Search)": 0, "Video (YouTube)": 0}
            for c in creatives:
                fmt = c.get("4")
                if fmt == 1: formats["Image (Banner)"] += 1
                elif fmt == 2: formats["Text (Search)"] += 1
                elif fmt == 3: formats["Video (YouTube)"] += 1

            print(f"[+] Cơ cấu định dạng thực tế (Format Mix): {formats}")

            if creatives:
                first = creatives[0]
                first_ts = int(first.get("6", {}).get("1", 0))
                last_ts = int(first.get("7", {}).get("1", 0))
                first_d = datetime.fromtimestamp(first_ts).strftime("%d/%m/%Y") if first_ts else "N/A"
                last_d = datetime.fromtimestamp(last_ts).strftime("%d/%m/%Y") if last_ts else "N/A"
                days_running = (last_ts - first_ts) // 86400 if (last_ts and first_ts) else 0

                print(f"[+] Mẫu Ad tiêu biểu ID: {first.get('2')}")
                print(f"    - Thời gian chạy: {first_d} -> {last_d} ({days_running} ngày)")

                # Bóc tách nội dung thật
                c_content = first.get("3", {})
                if "3" in c_content and "2" in c_content["3"]:
                    import re
                    m = re.search(r'src="([^"]+)"', c_content["3"]["2"])
                    if m:
                        print(f"    - URL ảnh CDN thật của Google: {m.group(1)[:80]}...")
                elif "1" in c_content and "4" in c_content["1"]:
                    print(f"    - URL Rich Media thật: {c_content['1']['4'][:80]}...")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
