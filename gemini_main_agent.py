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
4. Quản lý cấu hình API Key & Model động (hỗ trợ chuyển đổi model từ giao diện).
"""

import os
import re
import sys
import time
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "data_cache", "ai_config.json")

DEFAULT_MODELS = [
    {"id": "models/gemini-3.1-flash-lite", "name": "Gemini 3.1 Flash Lite (Khuyến nghị - Siêu tốc)", "recommended": True},
    {"id": "models/gemini-3.8-flash", "name": "Gemini 3.8 Flash (Mạnh mẽ)", "recommended": False},
    {"id": "models/gemini-3.5-flash", "name": "Gemini 3.5 Flash", "recommended": False},
    {"id": "models/gemini-pro-latest", "name": "Gemini Pro Latest (Chuyên sâu)", "recommended": False}
]


def load_ai_config() -> Dict[str, Any]:
    """Loads active AI configuration from disk."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Fallback to .env or environment variable
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    env_file = os.path.join(BASE_DIR, ".env")
    if not key and os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass

    return {
        "api_key": key or "",
        "active_model": "models/gemini-3.1-flash-lite",
        "available_models": DEFAULT_MODELS,
        "temperature": 0.1
    }


def save_ai_config(api_key: str, model_id: str = "models/gemini-3.1-flash-lite") -> Dict[str, Any]:
    """Saves updated AI configuration to disk and .env."""
    cfg = load_ai_config()
    if api_key:
        cfg["api_key"] = api_key.strip()
    if model_id:
        cfg["active_model"] = model_id.strip()
    cfg["updated_at"] = str(time.time())

    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    # Sync with .env
    env_file = os.path.join(BASE_DIR, ".env")
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(f"GEMINI_API_KEY={cfg['api_key']}\n")
            f.write(f"GEMINI_MODEL={cfg['active_model']}\n")
    except Exception:
        pass

    return cfg


def test_ai_connection(api_key: Optional[str] = None, model_id: Optional[str] = None) -> Dict[str, Any]:
    """Tests the connection to Gemini API with the given key and model."""
    cfg = load_ai_config()
    key = (api_key if api_key is not None else cfg.get("api_key", "")).strip()
    model = (model_id if model_id is not None else cfg.get("active_model", "models/gemini-3.1-flash-lite")).strip()

    if not key:
        return {"success": False, "error": "API Key is empty", "model": model}

    clean_m = model.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_m}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": "Hello, respond with JSON: {\"status\": \"ok\", \"model\": \"" + clean_m + "\"}"}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                res_data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "model": clean_m, "response": res_data}
    except Exception as e:
        return {"success": False, "error": str(e), "model": clean_m}
    return {"success": False, "error": "Unknown error", "model": clean_m}


# Pre-computed Knowledge Base for instant high-confidence matching (0ms)
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
    "ridge": {
        "brand_name": "The Ridge",
        "canonical_domain": "ridge.com",
        "facebook_search_term": "Ridge Wallet",
        "tiktok_slug": "ridge",
        "google_search_term": "Ridge Wallet",
        "industry": "Accessories & Everyday Carry",
        "confidence": 1.0
    },
    "ridge.com": {
        "brand_name": "The Ridge",
        "canonical_domain": "ridge.com",
        "facebook_search_term": "Ridge Wallet",
        "tiktok_slug": "ridge",
        "google_search_term": "Ridge Wallet",
        "industry": "Accessories & Everyday Carry",
        "confidence": 1.0
    },
    "the ridge": {
        "brand_name": "The Ridge",
        "canonical_domain": "ridge.com",
        "facebook_search_term": "Ridge Wallet",
        "tiktok_slug": "ridge",
        "google_search_term": "Ridge Wallet",
        "industry": "Accessories & Everyday Carry",
        "confidence": 1.0
    },
    "ridge wallet": {
        "brand_name": "The Ridge",
        "canonical_domain": "ridge.com",
        "facebook_search_term": "Ridge Wallet",
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
    """Intelligent heuristic fallback normalizer when Gemini API is unavailable."""
    clean = raw_query.strip().lower()
    clean = re.sub(r'^https?://', '', clean)
    clean = re.sub(r'^(www|us|uk|au|shop|store)\.', '', clean)
    clean = clean.split('/')[0].split('?')[0]

    for k, v in KNOWN_BRAND_REGISTRY.items():
        if k in clean or clean in k or v["canonical_domain"] in clean:
            return {**v, "_engine": "registry_heuristic"}

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


def call_gemini_api_with_fallback(raw_query: str, api_key: str, primary_model: str) -> Optional[Dict[str, Any]]:
    """Calls Gemini API with an automatic fallback chain across available models."""
    model_chain = [primary_model]
    for alt in ["models/gemini-3.1-flash-lite", "models/gemini-3.8-flash", "models/gemini-3.5-flash", "models/gemini-pro-latest"]:
        if alt not in model_chain:
            model_chain.append(alt)

    system_prompt = (
        "You are the TrendTrack Main Orchestrator Agent. "
        "Analyze the user's input (which may be a brand name, messy product query, or misspelled shop name in English or Vietnamese) "
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

    for m in model_chain:
        clean_m = m.replace("models/", "")
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_m}:generateContent?key={api_key}"
        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=6) as response:
                if response.status == 200:
                    res_data = json.loads(response.read().decode("utf-8"))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            raw_json_str = parts[0].get("text", "").strip()
                            parsed = json.loads(raw_json_str)
                            parsed["_engine"] = f"gemini_{clean_m}"
                            return parsed
        except Exception as e:
            # Try next model in chain if 503 or 404
            continue

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

    # Attempt Gemini API using active configuration
    cfg = load_ai_config()
    api_key = cfg.get("api_key", "").strip()
    active_model = cfg.get("active_model", "models/gemini-3.1-flash-lite")

    if api_key:
        ai_res = call_gemini_api_with_fallback(raw_query, api_key, active_model)
        if ai_res and ai_res.get("brand_name") and ai_res.get("canonical_domain"):
            return ai_res

    # Fallback to smart heuristic normalizer
    return heuristic_normalize_query(raw_query)


if __name__ == "__main__":
    cfg = load_ai_config()
    print("=" * 65)
    print(f"🤖 GEMINI MAIN AGENT (Active Model: {cfg.get('active_model')})")
    print(f"🔑 API Key: {cfg.get('api_key')[:8]}...{cfg.get('api_key')[-6:]}")
    print("=" * 65)

    test_queries = [
        "tai nghe loop của bỉ",
        "áo hoodie the oodie",
        "trueseamoss.com",
        "ví kim loại ridge",
        "xà bông dr squatch cho nam"
    ]
    for q in test_queries:
        res = disambiguate_and_dispatch(q)
        print(f"\n🔍 Query: \"{q}\"")
        print(f"  ├─ Brand: {res.get('brand_name')} ({res.get('canonical_domain')})")
        print(f"  ├─ FB: {res.get('facebook_search_term')} | TikTok: #{res.get('tiktok_slug')}")
        print(f"  └─ Engine: {res.get('_engine')} (Confidence: {res.get('confidence')})")
    print("\n" + "=" * 65)
