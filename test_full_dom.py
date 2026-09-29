from playwright.sync_api import sync_playwright
import json

url = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=True%20sea%20moss&search_type=keyword_unordered&media_type=all"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(url, timeout=30000)
    page.wait_for_timeout(6000)
    
    # Extract total count text
    count_text = page.locator("text=kết quả").first.text_content() or ""
    print("Results header:", count_text)
    
    js = """() => {
        const cards = [];
        const spans = Array.from(document.querySelectorAll("span, div"));
        const idElements = spans.filter(el => el.children.length === 0 && (el.textContent.includes("ID thư viện:") || el.textContent.includes("Library ID:")));
        
        idElements.forEach((idEl, index) => {
            let container = idEl.parentElement;
            for (let i = 0; i < 7; i++) {
                if (container && container.innerText && (container.innerText.includes("Xem chi tiết") || container.innerText.includes("See ad details"))) break;
                if (container && container.parentElement) container = container.parentElement;
            }
            if (!container) return;
            
            const raw = container.innerText || "";
            const lines = raw.split("\\n").map(s => s.trim()).filter(Boolean);
            
            // ID
            const idMatch = (idEl.textContent || "").match(/\\d+/);
            const adId = idMatch ? idMatch[0] : ("ad_" + index);
            
            // Start date
            let startDateStr = "";
            const dateLine = lines.find(l => l.includes("Ngày bắt đầu chạy:") || l.includes("Started running on"));
            if (dateLine) {
                startDateStr = dateLine.replace(/Ngày bắt đầu chạy:|Started running on:/i, "").trim();
            }
            
            // Page Name
            let pageName = "Advertiser";
            const sponsoredIdx = lines.findIndex(l => l.includes("Được tài trợ") || l.includes("Sponsored"));
            if (sponsoredIdx > 0) {
                pageName = lines[sponsoredIdx - 1];
            }
            
            // Copy / Description
            let copyText = "";
            if (sponsoredIdx >= 0 && sponsoredIdx + 1 < lines.length) {
                const candidates = lines.slice(sponsoredIdx + 1).filter(l => !l.includes("Xem chi tiết") && !l.includes("ID thư viện") && !l.includes("Hoạt động") && !l.includes("quảng cáo"));
                copyText = candidates.slice(0, 3).join(" ");
            }
            
            // Media
            let mediaType = "image";
            let mediaUrl = "";
            let posterUrl = "";
            
            const video = container.querySelector("video");
            const img = container.querySelector("img[src*='fbcdn.net']") || container.querySelector("img");
            
            if (video && (video.src || video.querySelector("source"))) {
                mediaType = "video";
                mediaUrl = video.src || (video.querySelector("source") ? video.querySelector("source").src : "");
                posterUrl = video.poster || "";
            } else if (img && img.src) {
                mediaType = "image";
                mediaUrl = img.src;
            }
            
            // Outbound Link / CTA
            const ctaBtn = container.querySelector("a[href*='http'], div[role='button']");
            const ctaText = ctaBtn ? ctaBtn.innerText : "Shop Now";
            
            cards.push({
                id: adId,
                pageName: pageName,
                startDate: startDateStr,
                description: copyText,
                mediaType: mediaType,
                mediaUrl: mediaUrl,
                posterUrl: posterUrl,
                ctaText: ctaText
            });
        });
        return cards;
    }"""
    
    extracted = page.evaluate(js)
    print("Successfully extracted cards count:", len(extracted))
    for i, c in enumerate(extracted[:3]):
        p_name = c["pageName"]
        s_date = c["startDate"]
        m_type = c["mediaType"]
        print(f"[{i+1}] {p_name} | Date: {s_date} | Type: {m_type}")
        print("    Copy:", c["description"][:80])
        print("    Media:", c["mediaUrl"][:70])
    browser.close()
