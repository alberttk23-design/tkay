() => {
        const results = [];
        const allText = Array.from(document.querySelectorAll("span, div"));
        const idElements = allText.filter(el => el.children.length === 0 && (el.textContent.includes("ID thư viện") || el.textContent.includes("Library ID")));
        
        idElements.forEach(idEl => {
            let container = idEl.parentElement;
            for (let i = 0; i < 6; i++) {
                if (container && container.innerText && container.innerText.includes("Xem chi tiết")) break;
                if (container && container.parentElement) container = container.parentElement;
            }
            if (!container) return;
            
            const raw = container.innerText || "";
            const lines = raw.split("\n").map(s => s.trim()).filter(Boolean);
            const img = container.querySelector("img");
            const video = container.querySelector("video");
            
            results.push({
                idText: idEl.textContent,
                lines: lines.slice(0, 10),
                imgSrc: img ? img.src : "",
                videoSrc: video ? (video.src || (video.querySelector("source") ? video.querySelector("source").src : "")) : ""
            });
        });
        return results;
    }