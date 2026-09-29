import os
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = os.path.expanduser("~/.gemini/browser_profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

def run_gemini_automation(image_path, prompt_text, output_video_path):
    print(f"--- KHỞI ĐỘNG TRÌNH DUYỆT TỰ ĐỘNG HÓA GEMINI ULTRA ---")
    print(f"Profile lưu tại: {PROFILE_DIR}")
    
    with sync_playwright() as p:
        # Launch Chrome with persistent profile
        browser = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False, # Mở cửa sổ thật để người dùng thấy và duyệt
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 900})
        
        print("Đang điều hướng đến https://gemini.google.com ...")
        page.goto("https://gemini.google.com/app", timeout=30000)
        page.wait_for_timeout(3000)
        
        # Check login status
        content = page.content()
        if "Sign in" in content or "Đăng nhập" in content:
            print("\n[CHÚ Ý] Bạn cần đăng nhập tài khoản Google Gemini Ultra lần đầu tiên trên cửa sổ Chrome vừa mở ra.")
            print("Vui lòng click đăng nhập tài khoản của bạn trên cửa sổ Chrome.")
            print("Đang chờ bạn đăng nhập (tối đa 60 giây)...")
            
            # Chờ người dùng đăng nhập thành công
            for i in range(12):
                page.wait_for_timeout(5000)
                if "Sign in" not in page.content() and "Đăng nhập" not in page.content():
                    print("ĐÃ PHÁT HIỆN ĐĂNG NHẬP THÀNH CÔNG!")
                    break
        else:
            print("ĐÃ ĐĂNG NHẬP SẴN BẰNG TÀI KHOẢN CỦA BẠN!")
            
        print("Đang chuẩn bị gửi ảnh và prompt...")
        page.wait_for_timeout(2000)
        
        # Tự động tìm khung chat
        chat_box = page.locator("div[contenteditable='true'], textarea, rich-textarea").first
        if chat_box.is_visible():
            chat_box.click()
            chat_box.fill(prompt_text)
            print("Đã điền prompt vào khung chat thành công!")
        else:
            print("Không tìm thấy khung chat tự động.")
            
        # Lưu phiên
        page.wait_for_timeout(5000)
        browser.close()
        print("Hoàn tất phiên kiểm tra!")

if __name__ == "__main__":
    test_img = os.path.expanduser("~/.gemini/antigravity/scratch/ai-video-studio/public/assets/scene1_hook.jpg")
    run_gemini_automation(
        image_path=test_img,
        prompt_text="Tạo video chuyển động 9:16 bằng Veo: Cô gái bấm remote, cây thông sáng đèn lung linh",
        output_video_path="/tmp/output_veo.mp4"
    )
