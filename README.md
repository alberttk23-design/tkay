# TrendTrack Pro - Ad & Traffic Intelligence Platform

Hệ thống reverse-engineer dữ liệu quảng cáo đa kênh (Meta Ad Library, TikTok Creative Center, Google Ads), phân tích lưu lượng truy cập (SimilarWeb Engine) và dự đoán doanh thu thương mại điện tử.

---

## ⚡ Tính năng cốt lõi

1. **🌐 Traffic & Sales Intelligence**
   - Phân tích Visitors MoM, dự đoán doanh thu tháng (`Est. sales/mo`) và doanh thu ngày (`$X/day`).
   - Area spline chart 6 tháng gần nhất.
   - Bóc tách thị phần truy cập theo quốc gia (`Visitors by country`).

2. **📣 Meta Ads & Multi-Channel Switcher**
   - Theo dõi số lượng Ads đang chạy (`Active Ads / Total`), tốc độ vít camp mới (`Ads Launched 30D / 7D`), ước tính Reach & Spend.
   - Biểu đồ tăng trưởng chiến dịch theo thời gian.
   - Chuyển đổi 1-click giữa **Meta Ads** và **TikTok Content**.

3. **📹 TikTok 24-Month Keyword Intelligence**
   - Biểu đồ chu kỳ 24 tháng theo dõi độ tăng trưởng keyword theo mùa (Q4 Holiday Spike, New Year Detox Spike, Summer Spike...).
   - Bộ hashtag nhận diện chính xác theo thương hiệu (`#brand`, `#brandreview`, `#brandamazon`, `#brandproduct`, `#brandofficial`).
   - Tổng hợp Views, Likes và tháng bùng nổ viral đỉnh điểm.

4. **🎯 Brandtracker Radar**
   - Bảng theo dõi danh sách thương hiệu, số lượng ads đang chạy và tốc độ lên camp.

---

## 🚀 Khởi chạy nhanh

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Khởi chạy ứng dụng
```bash
python3 trendtrack_app.py
```

Truy cập Dashboard tại: **`http://localhost:8765`**

---

## 📂 Cấu trúc Repository

- `trendtrack_app.py`: Server HTTP đa luồng phục vụ Dashboard UI, API routing và cache handler.
- `ad_scanner.py`: Core scanner bóc tách Meta Ad Library ngầm, engine tính toán traffic & doanh thu, thuật toán chu kỳ keyword TikTok 24 tháng.
- `out/spy_cache/`: Dữ liệu cache chuẩn của các thương hiệu hàng đầu (The Oodie, Ridge, Momcozy, True Sea Moss...).
