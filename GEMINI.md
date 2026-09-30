# AI Video Studio / TrendTrack Explorer - Project Guidelines & Rules

> **MỤC TIÊU DỰ ÁN**: Xây dựng nền tảng tình báo quảng cáo đa kênh (Meta Ad Library, Google Ads Transparency Center, TikTok Ad Library & Profile, Email Marketing Flows) hoạt động chính xác cho **BẤT KỲ THƯƠNG HIỆU / DOMAIN NÀO** do người dùng tìm kiếm.

---

## 1. NGUYÊN TẮC CỐT LÕI (CORE PRINCIPLES - BẮT BUỘC TUÂN THỦ)

### 1.1. Zero Hallucination & Zero Fake Data (Tuyệt đối không chế dữ liệu ảo)
- **Không sinh dữ liệu giả (No synthetic mock data)**: Tuyệt đối không tự động tạo ra video/ảnh giả lập (ví dụ: ảnh người mẫu thời trang, giá treo quần áo lấy từ Unsplash) khi quét thương hiệu mới.
- **Trạng thái 0 trung thực (Honest Zero-State)**: Nếu một thương hiệu có `0` quảng cáo hoặc `0` video trên bất kỳ nền tảng nào (Meta, Google, TikTok, Emails), hệ thống PHẢI giữ nguyên số `0` và hiển thị giao diện **Empty State** thông báo rõ ràng cho người dùng.
- **Xóa bỏ triệt để Hardcode & Fallback**: Tuyệt đối không hardcode dữ liệu của "The Oodie", "Guyker" hoặc bất kỳ thương hiệu nào làm giá trị mặc định cho các thương hiệu khác. Cấm các toán tử fallback dạng `|| 703`, `|| 31`, `|| 69`, `|| '1.8K'`.

### 1.2. Universal Brand Search (Công cụ tìm kiếm phổ quát)
- Mọi logic quét dữ liệu phải độc lập, chấp nhận mọi input: tên thương hiệu (vd: `crzyoga`, `momcozy`, `ridge`, `trueseamoss`), domain (`guyker.com`, `gymshark.com`), hoặc URL.
- Không ép người dùng chỉ được xem một số thương hiệu có sẵn.

---

## 2. QUY TẮC AN TOÀN GIT & VERSION CONTROL

- **Remote Push Constraint**:
  - **CHỈ ĐƯỢC PHÉP PUSH** lên remote `alt` trên nhánh `main`:
    ```bash
    git push alt main
    ```
    *(Remote: `https://github.com/ankhang041074-alt/tkay.git`)*
  - **TUYỆT ĐỐI CẤM** push lên remote `origin`.

---

## 3. KIẾN TRÚC HỆ THỐNG & BẢN ĐỒ CODEBASE

### 3.1. Server & API Handlers
- **File chạy chính**: `trendtrack_app.py`
  - Cổng dịch vụ (Port): **`8765`** (truy cập tại `http://localhost:8765`).
  - Giao diện người dùng: Single-page application tích hợp trực tiếp, hỗ trợ sub-tabs: Overview, Meta, Google, TikTok, Contents, Emails.
  - Các API chính:
    - `/api/scan?query=...`: Quét tổng hợp Meta Ad Library & KPIs.
    - `/api/google-ads?query=...`: Quét Google Transparency Center.
    - `/api/tiktok?query=...`: Lấy thông tin TikTok Ads & Organic profile.
    - `/api/emails?query=...`: Lấy dữ liệu Email Marketing & flows.
    - `/api/meta-ranking?query=...`: Lấy xếp hạng quảng cáo Meta theo longevity, views, velocity.

### 3.2. Scanner Modules
- `ad_scanner.py`: Trích xuất dữ liệu từ Meta Ad Library API/web scraping.
- `google_scanner.py`: Trích xuất quảng cáo từ Google Ads Transparency Center.
- `tiktok_service.py`: Phân tích TikTok Ads Library, Spark Ads, tỷ lệ Ads vs Organic.
- `email_scanner.py`: Trích xuất các chiến dịch email và luồng tự động (flows).
- `meta_ranking.py`: Thuật toán phân loại và xếp hạng quảng cáo theo thời gian chạy và hiệu suất.

### 3.3. Cache Management
- Thư mục lưu cache: `out/spy_cache/`.
- Khi cập nhật thuật toán hoặc khi người dùng yêu cầu quét sạch dữ liệu, cần xóa các file cache tương ứng trong thư mục này để tránh đọc lại dữ liệu lỗi/cũ.

---

## 4. QUY TRÌNH PHÁT TRIỂN & KIỂM THỬ (VERIFICATION WORKFLOW)

Mỗi khi chỉnh sửa mã nguồn backend hoặc frontend:
1. **Khởi động lại Server**:
   ```bash
   lsof -ti :8765 | xargs kill -9 2>/dev/null || true
   python3 trendtrack_app.py
   ```
2. **Kiểm tra tự động bằng Playwright (Headless)**:
   - Viết hoặc chạy script Playwright để truy cập `http://localhost:8765`, click vào tab cần kiểm tra, chờ nạp dữ liệu và chụp ảnh màn hình lưu vào thư mục artifacts.
   - Dùng `view_file` xem lại ảnh chụp thực tế để kiểm tra giao diện, số liệu hiển thị trước khi báo cáo kết quả cho người dùng.
3. **Commit & Push**:
   - Luôn commit với commit message rõ ràng, theo chuẩn Conventional Commits.
   - Luôn push bằng lệnh: `git push alt main`.

---

## 5. NGUYÊN TẮC BẢO VỆ NGƯỜI DÙNG NO-CODE (NO-CODE USER PROTECTION PROTOCOL)

- **Người dùng không chuyên về lập trình (No-Code)**: 
  - Tuyệt đối không yêu cầu người dùng tự đọc code, tự debug lỗi terminal hay sửa cấu hình phức tạp.
  - Mọi lỗi phát sinh trong quá trình phát triển, AI phải tự động bắt lỗi và tự động sửa chữa 100%.
- **Lá chắn kiểm thử tự động bắt buộc (`verify_system.py`)**:
  - Sau mỗi lần sửa code hoặc thêm tính năng mới, AI **BẮT BUỘC** phải chạy lệnh:
    ```bash
    python3 verify_system.py
    ```
  - Nếu kết quả trả về có bất kỳ mục nào **FAIL** (lỗi cú pháp, server bị treo, hoặc lọt dữ liệu giả/Oodie), AI phải tự động sửa cho đến khi đạt **100% PASS** trước khi thông báo cho người dùng.
- **Bảo toàn tính năng cũ (No Regressions)**:
  - Khi dự án phình to, cấm sửa đổi ồ ạt hoặc xóa nhầm các hàm đang chạy ổn định.
  - Luôn kiểm tra đối chiếu kỹ lưỡng trước khi lưu file.
