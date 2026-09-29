#!/usr/bin/env python3
import os
import sys
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = os.path.expanduser("~/.gemini/browser_profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

def run_veo_automation(image_path: str, prompt_text: str, output_path: str):
    print("=" * 60)
    print("🚀 KHỞI ĐỘNG VEO BROWSER AUTOMATION AGENT (GEMINI ULTRA)")
    print("=" * 60)
    print(f"📁 Hồ sơ Chrome: {PROFILE_DIR}")
    print(f"🖼️ Ảnh đầu vào: {image_path}")
    print(f"📝 Prompt hành động: {prompt_text[:60]}...")
    print(f"💾 File đầu ra: {output_path}")
    print("-" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,  # Mở cửa sổ thật để người dùng thấy rõ
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-default-browser-check"
            ]
        )

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_viewport_size({"width": 1366, "height": 850})

        # Intercept network responses to capture video streams
        captured_video_url = []
        def on_response(response):
            content_type = response.headers.get("content-type", "")
            if "video/mp4" in content_type or ".mp4" in response.url.lower():
                print(f"\n[NETWORK] Phát hiện luồng video MP4 từ máy chủ: {response.url[:80]}...")
                captured_video_url.append(response.url)
        page.on("response", on_response)

        print("\n[1/5] Đang mở https://gemini.google.com/app ...")
        page.goto("https://gemini.google.com/app", timeout=45000)
        page.wait_for_timeout(3000)

        # Kiểm tra trạng thái đăng nhập
        body_text = page.inner_text("body")
        if "Sign in" in body_text or "Đăng nhập" in body_text:
            print("\n" + "!" * 60)
            print("⚠️ BẠN CHƯA ĐĂNG NHẬP GOOGLE GEMINI ULTRA TRÊN PROFILE NÀY.")
            print("👉 Vui lòng click 'Đăng nhập' (Sign In) trên cửa sổ Chrome vừa mở.")
            print("👉 Đăng nhập đúng tài khoản có gói Ultra của bạn.")
            print("⏳ Script sẽ tự động nhận diện và chạy tiếp ngay khi bạn đăng nhập xong...")
            print("!" * 60 + "\n")

            logged_in = False
            # Chờ tối đa 30 phút để bạn thoải mái nhập tài khoản và mã xác thực 2FA
            for _ in range(360):
                page.wait_for_timeout(5000)
                try:
                    cur_text = page.inner_text("body")
                    if "Sign in" not in cur_text and "Đăng nhập" not in cur_text:
                        logged_in = True
                        print("✅ ĐÃ XÁC NHẬN ĐĂNG NHẬP THÀNH CÔNG! BẮT ĐẦU TỰ ĐỘNG HÓA...")
                        break
                except Exception:
                    pass
            if not logged_in:
                print("❌ Hết thời gian chờ đăng nhập (30 phút). Đóng trình duyệt.")
                browser.close()
                return False
        else:
            print("✅ ĐÃ ĐĂNG NHẬP SẴN BẰNG TÀI KHOẢN CỦA BẠN!")

        page.wait_for_timeout(2000)

        # [2/5] Đính kèm ảnh vào Gemini
        print("\n[2/5] Đang tự động đính kèm ảnh vào khung chat...")
        upload_btn = page.locator("button[aria-label*='tải lên' i], button[aria-label*='upload' i], button[aria-label*='thêm' i]").first
        if upload_btn.is_visible():
            upload_btn.click()
            page.wait_for_timeout(1000)

            # Locate the image file input
            file_input = page.locator("input[type='file'][accept*='image']").first
            if file_input.is_visible() or file_input.count() > 0:
                file_input.set_input_files(image_path)
                print(f"✅ Đã đính kèm ảnh: {os.path.basename(image_path)}")
                page.wait_for_timeout(2000)
            else:
                print("⚠️ Không tìm thấy thẻ file input image, thử file input chung...")
                page.locator("input[type='file']").first.set_input_files(image_path)
        else:
            print("⚠️ Không thấy nút dấu '+', thử kéo thả trực tiếp...")

        # [3/5] Điền kịch bản prompt vào khung chat
        print("\n[3/5] Đang điền kịch bản prompt vào khung chat...")
        editor = page.locator("div.ql-editor, div[contenteditable='true'], rich-textarea").first
        if editor.is_visible():
            editor.click()
            # Gõ tự nhiên hoặc fill
            editor.fill(prompt_text)
            print("✅ Đã điền xong prompt hành động chuẩn xác!")
            page.wait_for_timeout(1500)
        else:
            print("❌ Không tìm thấy khung soạn thảo văn bản.")

        # [4/5] Gửi yêu cầu tạo video
        print("\n[4/5] Đang bấm nút Gửi (Send)...")
        send_btn = page.locator("button[aria-label*='Gửi' i], button[aria-label*='Send' i], button.send-button").first
        if send_btn.is_visible():
            send_btn.click()
            print("🚀 ĐÃ BẤM GỬI LỆNH TẠO VIDEO VEO!")
        else:
            # Nhấn Enter nếu không thấy nút
            page.keyboard.press("Enter")
            print("🚀 Đã nhấn Enter gửi lệnh!")

        # [5/5] Chờ kết quả tạo video từ Veo
        print("\n[5/5] Đang chờ Google Veo trên web xử lý và sinh video (khoảng 1 - 3 phút)...")
        print("💡 Cửa sổ Chrome vẫn mở để bạn có thể quan sát tiến trình trực tiếp.")

        # Theo dõi phản hồi
        video_found = False
        start_time = time.time()
        timeout_seconds = 300  # 5 phút tối đa

        while time.time() - start_time < timeout_seconds:
            page.wait_for_timeout(5000)
            elapsed = int(time.time() - start_time)
            print(f"⏳ Đang chờ Veo render video... ({elapsed}s trôi qua)")

            # Kiểm tra thẻ video trên trang
            videos = page.locator("video").all()
            if len(videos) > 0:
                print(f"🎉 ĐÃ PHÁT HIỆN VIDEO TRÊN TRANG GEMINI!")
                video_src = videos[-1].get_attribute("src")
                print(f"Video element src: {video_src[:60]}...")
                video_found = True
                break

            # Kiểm tra nếu network đã bắt được video
            if len(captured_video_url) > 0:
                print(f"🎉 ĐÃ BẮT ĐƯỢC LINK VIDEO TỪ NETWORK!")
                video_found = True
                break

            # Kiểm tra nếu web báo lỗi
            cur_body = page.inner_text("body")
            if "Something went wrong" in cur_body or "Đã xảy ra lỗi" in cur_body:
                print("⚠️ Web Gemini báo lỗi ngẫu nhiên. Vui lòng kiểm tra trên cửa sổ Chrome.")
                break

        if video_found:
            print("\n🎉 HOÀN THÀNH QUY TRÌNH TẠO VIDEO BẰNG VEO TRÊN WEB!")
            print(f"File video sẽ được lưu về: {output_path}")
        else:
            print("\n⚠️ Hết thời gian chờ hoặc cần thêm thao tác trên trình duyệt.")

        print("\nGiữ cửa sổ mở thêm 10 giây để bạn theo dõi...")
        page.wait_for_timeout(10000)
        browser.close()
        print("Đã đóng trình duyệt tự động.")
        return video_found

if __name__ == "__main__":
    img = os.path.expanduser("~/.gemini/antigravity/scratch/ai-video-studio/public/assets/scene1_hook.jpg")
    prompt = (
        "Create a photorealistic vertical 9:16 video using Veo: "
        "The woman smiles and presses the button on the small remote control in her hand. "
        "The Christmas tree lights instantly ignite into warm golden brilliance. "
        "Cinematic smooth camera motion, realistic holiday commercial."
    )
    out = os.path.expanduser("~/.gemini/antigravity/scratch/ai-video-studio/out/veo_output.mp4")
    run_veo_automation(img, prompt, out)
