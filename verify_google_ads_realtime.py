import json
import urllib.request
import urllib.parse
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://adstransparency.google.com/?region=anywhere",
}

def rpc_call(endpoint, payload):
    url = f"https://adstransparency.google.com/anji/_/rpc/{endpoint}?authuser="
    post_data = urllib.parse.urlencode({"f.req": json.dumps(payload)}).encode("utf-8")
    req = urllib.request.Request(url, data=post_data, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))

test_cases = [
    {"name": "Ridge Wallet", "query": "ridge.com"},
    {"name": "Gymshark", "query": "Gymshark"},
    {"name": "Casetify", "query": "casetify.com"},
    {"name": "Anker", "query": "Anker"},
    {"name": "Manscaped", "query": "Manscaped"}
]

print("=== BẮT ĐẦU KIỂM CHỨNG TRỰC TIẾP TRÊN MÁY CHỦ GOOGLE ADS TRANSPARENCY ===\n")

for tc in test_cases:
    brand = tc["name"]
    query = tc["query"]
    print(f"--------------------------------------------------")
    print(f"[*] Đang kiểm tra thương hiệu: {brand} (Query: '{query}')")
    
    # 1. Search suggestion
    sugg_res = rpc_call("SearchService/SearchSuggestions", {"1": query, "2": 5, "3": 5, "5": {"1": 1}})
    items = sugg_res.get("1", [])
    
    adv_id = None
    adv_name = None
    country = None
    domain = None
    
    for it in items:
        if "1" in it:
            adv = it["1"]
            adv_name = adv.get("1")
            adv_id = adv.get("2")
            country = adv.get("3")
            break
        elif "2" in it and not domain:
            domain = it["2"].get("1")
            
    print(f"  -> Kết quả gợi ý từ Google:")
    if adv_id:
        print(f"     + Pháp nhân được xác minh bởi Google: {adv_name}")
        print(f"     + Google Advertiser ID: {adv_id}")
        print(f"     + Quốc gia đăng ký: {country}")
    elif domain:
        print(f"     + Tên miền khớp: {domain}")
    else:
        print(f"     + Không tìm thấy gợi ý trực tiếp.")
        
    # 2. Fetch Creatives
    if adv_id:
        filter_obj = {"12": {"1": "", "2": True}, "13": {"1": [adv_id]}}
    elif domain:
        filter_obj = {"12": {"1": domain, "2": True}}
    else:
        filter_obj = {"12": {"1": query, "2": True}}
        
    payload_creatives = {
        "2": 10,
        "3": filter_obj,
        "7": {"1": 1, "2": 0, "3": 2704}
    }
    
    creative_res = rpc_call("SearchService/SearchCreatives", payload_creatives)
    creatives = creative_res.get("1", [])
    est_range = (creative_res.get("4"), creative_res.get("5"))
    
    print(f"  -> Dữ liệu Ads thật từ máy chủ Google:")
    print(f"     + Tổng số Ads Google ước tính: {est_range[0]} - {est_range[1]}")
    print(f"     + Số Ads mẫu tải về thành công: {len(creatives)}")
    
    if creatives:
        sample = creatives[0]
        c_id = sample.get("2")
        fmt = sample.get("4")
        fmt_name = "Image" if fmt == 1 else ("Text" if fmt == 2 else "Video")
        first_shown_ts = int(sample.get("6", {}).get("1", 0))
        last_shown_ts = int(sample.get("7", {}).get("1", 0))
        
        first_date = datetime.fromtimestamp(first_shown_ts).strftime("%Y-%m-%d") if first_shown_ts else "N/A"
        last_date = datetime.fromtimestamp(last_shown_ts).strftime("%Y-%m-%d") if last_shown_ts else "N/A"
        days = (last_shown_ts - first_shown_ts) // 86400 if (last_shown_ts and first_shown_ts) else 0
        
        print(f"     + Mẫu Ad Creative ID: {c_id}")
        print(f"     + Định dạng: {fmt_name} (Code: {fmt})")
        print(f"     + Bắt đầu chạy: {first_date} -> Lần cuối thấy: {last_date} ({days} ngày)")
        
        # Link asset image nếu có
        content = sample.get("3", {})
        if "3" in content and "2" in content["3"]:
            import re
            m = re.search(r'src="([^"]+)"', content["3"]["2"])
            if m:
                print(f"     + Link ảnh banner gốc trên Google CDN: {m.group(1)[:75]}...")
        elif "1" in content and "4" in content["1"]:
            print(f"     + Link Rich Media Google: {content['1']['4'][:75]}...")
            
    print()
