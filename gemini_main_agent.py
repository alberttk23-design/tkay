#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Main Agent: Query Disambiguation & Intelligent Dispatcher
================================================================
Trí tuệ nhân tạo điều phối trung tâm sử dụng Google Gemini API.
Nhiệm vụ:
1. Tiếp nhận bất kỳ câu truy vấn nào từ người dùng (tên sản phẩm, viết sai chính tả, tiếng Việt có dấu/không dấu, v.v.)
2. Suy luận có cấu trúc và chuẩn hóa thành:
   - Brand Name chính thức (ví dụ: 'The Oodie', 'Loop Earplugs')
   - Canonical Domain (ví dụ: 'theoodie.com', 'loopearplugs.com')
   - Facebook Search Term / Fanpage Name (cho Meta Subagent)
   - TikTok Clean Slug (cho TikTok Subagent)
   - Google Search Query (cho Google Subagent)
   - Industry Category
3. Phân phối chính xác xuống cho 4 Subagents chuyên trách.
4. Cơ chế Dual-Engine: Tự động fallback về Heuristic Normalizer nếu chưa có GEMINI_API_KEY.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read GEMINI_API_KEY from environment or .env file if available
def get_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    env_file = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return ""


# Pre-computed Knowledge Base for instant high-confidence matching
KNOWN_BRAND_REGISTRY = {
    "the oodie": {
        "brand_name": "The Oodie",
        "canonical_domain": "theoodie.com",
        "facebook_search_term": "The Oodie",
        "tiktok_slug": "theoodie",
        "google_search_term": "The Oodie",
        "industry": "Apparel & Loungewear",
        "confidence": 1.0
    },
    "loop earplugs": {
        "brand_name": "Loop Earplugs",
        "canonical_domain": "loopearplugs.com",
        "facebook_search_term": "Loop Earplugs",
        "tiktok_slug": "loopearplugs",
        "google_search_term": "Loop Earplugs",
        "industry": "Consumer Tech & Audio",
        "confidence": 1.0
    },
    "dr. squatch": {
        "brand_name": "Dr. Squatch",
        "canonical_domain": "drsquatch.com",
        "facebook_search_term": "Dr. Squatch",
        "tiktok_slug": "drsquatch",
        "google_search_term": "Dr. Squatch",
        "industry": "Personal Care & Grooming",
        "confidence": 1.0
    },
    "true sea moss": {
        "brand_name": "True Sea Moss",
        "canonical_domain": "trueseamoss.com",
        "facebook_search_term": "True Sea Moss",
        "tiktok_slug": "trueseamoss",
        "google_search_term": "True Sea Moss",
        "industry": "Health & Supplements",
        "confidence": 1.0
    },
    "momcozy": {
        "brand_name": "Momcozy",
        "canonical_domain": "momcozy.com",
        "facebook_search_term": "Momcozy",
        "tiktok_slug": "momcozy",
        "google_search_term": "Momcozy",
        "industry": "Baby & Mother Care",
        "confidence": 1.0
    },
    "ridge wallet": {
        "brand_name": "Ridge Wallet",
        "canonical_domain": "ridge.com",
        "facebook_search_term": "The Ridge",
        "tiktok_slug": "ridge",
        "google_search_term": "Ridge Wallet",
        "industry": "Accessories & Everyday Carry",
        "confidence": 1.0
    },
    "blissy": {
        "brand_name": "Blissy",
        "canonical_domain": "blissy.com",
        "facebook_search_term": "Blissy",
        "tiktok_slug": "blissy",
        "google_search_term": "Blissy",
        "industry": "Beauty & Silk Sleepwear",
        "confidence": 1.0
    },
    "glov beauty": {
        "brand_name": "Glov Beauty",
        "canonical_domain": "glov.co",
        "facebook_search_term": "GLOV",
        "tiktok_slug": "glov.co",
        "google_search_term": "Glov Beauty",
        "industry": "Skincare & Beauty",
        "confidence": 1.0
    }
}


def heuristic_normalize_query(raw_query: str) -> Dict[str, Any]:
    """
    Intelligent heuristic fallback normalizer when Gemini API is unavailable.
    """
    clean = raw_query.strip().lower()
    clean = re.sub(r'^https?://', '', clean)
    clean = re.sub(r'^(www|us|uk|au|shop|store)\.', '', clean)
    clean = clean.split('/')[0].split('?')[0]

    # Check exact known brand aliases
    for k, v in KNOWN_BRAND_REGISTRY.items():
        if k in clean or clean in k or v["canonical_domain"] in clean:
            return {**v, "_engine": "registry_heuristic"}

    # General domain or brand slug normalization
    domain_match = re.search(r'([a-z0-9\-]+)\.(com|co|vn|io|shop|store|org|net|app|us|uk|de|fr|ca|au)', clean)
    if domain_match:
        brand_slug = domain_match.group(1).replace('-', ' ')
        domain = domain_match.group(0)
    else:
        brand_slug = re.sub(r'[^a-z0-9]', ' ', clean).strip()
        domain = f"{re.sub(r'[^a-z0-9]', '', clean)}.com"

    formatted_name = brand_slug.title()
    clean_tiktok = re.sub(r'[^a-z0-9]', '', brand_slug)

    return {
        "brand_name": formatted_name,
        "canonical_domain": domain,
        "facebook_search_term": formatted_name,
        "tiktok_slug": clean_tiktok,
        "google_search_term": formatted_name,
        "industry": "General E-Commerce",
        "confidence": 0.85,
        "_engine": "smart_heuristic"
    }


def call_gemini_api(raw_query: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Calls Google Gemini API (gemini-2.5-flash / gemini-1.5-flash) to structure the query.
    """
    model_name = "gemini-2.5-flash"
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    system_prompt = (
        "You are the TrendTrack Main Orchestrator Agent. "
        "Analyze the user's input (which may be a brand name, messy product query, or misspelled shop name) "
        "and extract the canonical e-commerce brand identity. "
        "Respond ONLY with a valid JSON object matching this schema:\n"
        "{\n"
        '  "brand_name": "Official Brand Name",\n'
        '  "canonical_domain": "brand.com",\n'
        '  "facebook_search_term": "Official Facebook Page Name",\n'
        '  "tiktok_slug": "clean_alphanumeric_handle",\n'
        '  "google_search_term": "Official Brand Name",\n'
        '  "industry": "Industry Category",\n'
        '  "confidence": 0.95\n'
        "}\n"
        "Do not include markdown codeblocks, explanations, or any extra text."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nUser Search Query: \"{raw_query}\""}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }

    try:
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        raw_json_str = parts[0].get("text", "").strip()
                        parsed = json.loads(raw_json_str)
                        parsed["_engine"] = f"gemini_{model_name}"
                        return parsed
    except Exception as e:
        print(f"⚠️ [GEMINI MAIN AGENT] API call error ({e}), falling back to heuristic...")
    return None


def disambiguate_and_dispatch(raw_query: str) -> Dict[str, Any]:
    """
    Main entry point for Gemini Main Agent:
    Disambiguates query and prepares dispatch packets for all 4 subagents.
    """
    if not raw_query or not raw_query.strip():
        return heuristic_normalize_query("unknown")

    # Check instant registry first (0ms latency)
    clean_low = raw_query.strip().lower()
    for k, v in KNOWN_BRAND_REGISTRY.items():
        if clean_low == k or clean_low == v["canonical_domain"]:
            return {**v, "_engine": "registry_instant"}

    # Attempt Gemini API if key is available
    api_key = get_gemini_api_key()
    if api_key:
        ai_res = call_gemini_api(raw_query, api_key)
        if ai_res and ai_res.get("brand_name") and ai_res.get("canonical_domain"):
            return ai_res

    # Fallback to smart heuristic normalizer
    return heuristic_normalize_query(raw_query)


if __name__ == "__main__":
    test_queries = [
        "áo hoodie the oodie úc",
        "tai nghe loop bỉ",
        "trueseamoss.com",
        "mom cozy",
        "ví ridge wallet"
    ]
    print("=" * 65)
    print("🤖 GEMINI MAIN AGENT - TEST DISAMBIGUATION & DISPATCH")
    print("=" * 65)
    for q in test_queries:
        res = disambiguate_and_dispatch(q)
        print(f"\n🔍 Query: \"{q}\"")
        print(f"  ├─ Brand: {res.get('brand_name')} ({res.get('canonical_domain')})")
        print(f"  ├─ FB: {res.get('facebook_search_term')} | TikTok: #{res.get('tiktok_slug')}")
        print(f"  └─ Engine: {res.get('_engine')} (Confidence: {res.get('confidence')})")
    print("\n" + "=" * 65)
