#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meta Facebook Page ID Resolver Engine
======================================
Giải quyết triệt để vấn đề sai lệch dữ liệu bằng cách chuyển đổi từ:
Cào theo Từ khóa (Keyword Search) -> Cào theo Page ID chính thức (view_all_page_id).

Hệ thống hoạt động theo 3 cấp độ (3-Tier Resolution):
1. Level 1: Registry Cache (0ms) - Tra cứu tức thì trong data_cache/facebook_page_ids.json.
2. Level 2: Website Footer Extraction - Bóc tách link Fanpage ở chân trang website.
3. Level 3: Meta Live Typeahead & Search Prober - Khám phá và trích xuất Page ID tự động.
"""

import os
import re
import json
import urllib.parse
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "data_cache", "facebook_page_ids.json")
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

# Pre-seeded Verified Authoritative Page IDs (Verified against Meta Ad Library)
SEEDED_PAGE_REGISTRY = {
    "ridge": {"page_id": "176366735873065", "page_name": "The Ridge", "canonical_domain": "ridge.com"},
    "the ridge": {"page_id": "176366735873065", "page_name": "The Ridge", "canonical_domain": "ridge.com"},
    "ridge.com": {"page_id": "176366735873065", "page_name": "The Ridge", "canonical_domain": "ridge.com"},
    "ridgewallet": {"page_id": "176366735873065", "page_name": "The Ridge", "canonical_domain": "ridge.com"},
    "ridgewallet.com": {"page_id": "176366735873065", "page_name": "The Ridge", "canonical_domain": "ridge.com"},
    
    "the oodie": {"page_id": "601495866852901", "page_name": "The Oodie", "canonical_domain": "theoodie.com"},
    "theoodie": {"page_id": "601495866852901", "page_name": "The Oodie", "canonical_domain": "theoodie.com"},
    "theoodie.com": {"page_id": "601495866852901", "page_name": "The Oodie", "canonical_domain": "theoodie.com"},
    "oodie": {"page_id": "601495866852901", "page_name": "The Oodie", "canonical_domain": "theoodie.com"},
    
    "true sea moss": {"page_id": "101371852670671", "page_name": "True Sea Moss Health", "canonical_domain": "trueseamoss.com"},
    "trueseamoss": {"page_id": "101371852670671", "page_name": "True Sea Moss Health", "canonical_domain": "trueseamoss.com"},
    "trueseamoss.com": {"page_id": "101371852670671", "page_name": "True Sea Moss Health", "canonical_domain": "trueseamoss.com"},
    
    "crz yoga": {"page_id": "144001845461758", "page_name": "CRZ YOGA UK", "canonical_domain": "crzyoga.com"},
    "crzyoga": {"page_id": "144001845461758", "page_name": "CRZ YOGA UK", "canonical_domain": "crzyoga.com"},
    "crzyoga.com": {"page_id": "144001845461758", "page_name": "CRZ YOGA UK", "canonical_domain": "crzyoga.com"},
    
    "dr. squatch": {"page_id": "118075261668462", "page_name": "Dr. Squatch", "canonical_domain": "drsquatch.com"},
    "dr squatch": {"page_id": "118075261668462", "page_name": "Dr. Squatch", "canonical_domain": "drsquatch.com"},
    "drsquatch": {"page_id": "118075261668462", "page_name": "Dr. Squatch", "canonical_domain": "drsquatch.com"},
    "drsquatch.com": {"page_id": "118075261668462", "page_name": "Dr. Squatch", "canonical_domain": "drsquatch.com"},
    
    "momcozy": {"page_id": "706775379186676", "page_name": "Momcozy", "canonical_domain": "momcozy.com"},
    "momcozy.com": {"page_id": "706775379186676", "page_name": "Momcozy", "canonical_domain": "momcozy.com"},
    
    "loop earplugs": {"page_id": "517850318391712", "page_name": "Loop", "canonical_domain": "loopearplugs.com"},
    "loopearplugs": {"page_id": "517850318391712", "page_name": "Loop", "canonical_domain": "loopearplugs.com"},
    "loopearplugs.com": {"page_id": "517850318391712", "page_name": "Loop", "canonical_domain": "loopearplugs.com"},
    
    "blissy": {"page_id": "1940989022646271", "page_name": "Blissy", "canonical_domain": "blissy.com"},
    "blissy.com": {"page_id": "1940989022646271", "page_name": "Blissy", "canonical_domain": "blissy.com"}
}


def load_page_registry() -> Dict[str, Any]:
    """Loads active Page ID registry from disk, merging with seeded values."""
    registry = dict(SEEDED_PAGE_REGISTRY)
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                disk_data = json.load(f)
                registry.update(disk_data)
        except Exception:
            pass
    return registry


def save_page_id(identifier: str, page_id: str, page_name: str, canonical_domain: Optional[str] = None):
    """Saves newly discovered Page ID to disk."""
    reg = load_page_registry()
    entry = {
        "page_id": str(page_id),
        "page_name": page_name,
        "canonical_domain": canonical_domain or ""
    }
    clean_k = identifier.strip().lower()
    reg[clean_k] = entry
    if canonical_domain:
        reg[canonical_domain.strip().lower()] = entry
    
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(reg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ [PAGE RESOLVER] Could not save registry: {e}")


def clean_slug(text: str) -> str:
    """Normalizes query or domain for lookup."""
    clean = (text or "").lower().strip()
    clean = re.sub(r'^https?://', '', clean)
    clean = re.sub(r'^(www|us|uk|au|shop|store)\.', '', clean)
    return clean.split('/')[0].split('?')[0].strip()


def resolve_facebook_page_id(query: str, domain: Optional[str] = None, allow_live_probe: bool = True) -> Optional[Dict[str, Any]]:
    """
    Main entry point: Resolves a brand query or domain to an exact Facebook Page ID.
    Returns: {"page_id": "176366735873065", "page_name": "The Ridge", "canonical_domain": "..."} or None.
    """
    registry = load_page_registry()
    
    clean_q = clean_slug(query)
    clean_d = clean_slug(domain) if domain else ""
    
    # ── Level 1: Instant Registry Lookup (0ms) ─────────────────────────────────
    for cand in [clean_q, clean_d, query.lower().strip()]:
        if cand and cand in registry:
            return registry[cand]
            
    # Check domain stem
    if clean_d:
        stem = re.sub(r'\.(com|co|vn|io|org|net|us|uk|de|fr|ca|au)$', '', clean_d)
        if stem in registry:
            return registry[stem]

    # ── Level 2: Website Ground Truth Footer Probe ────────────────────────────
    target_site = clean_d or (clean_q if '.' in clean_q else None)
    if target_site:
        try:
            import store_intelligence as _si
            gt = _si.extract_website_ground_truth(target_site)
            fb_handle = gt.get("facebook_handle")
            if fb_handle and fb_handle in registry:
                return registry[fb_handle]
        except Exception:
            pass

    if not allow_live_probe:
        return None

    # ── Level 3: Meta Live Typeahead & Search Prober ───────────────────────────
    try:
        from playwright.sync_api import sync_playwright
        search_target = query if len(query) >= 3 else (clean_d or query)
        q_enc = urllib.parse.quote(search_target)
        probe_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={q_enc}&search_type=keyword_unordered&media_type=all"
        
        print(f"🕵️ [PAGE RESOLVER] Probing Meta Ad Library for '{search_target}' Page ID...")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            page = browser.new_page(locale="en-US")
            page.goto(probe_url, wait_until="domcontentloaded", timeout=12000)
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()

            # Extract (page_name, page_id) pairs from JSON payload inside HTML
            pairs = re.findall(r'\"page_name\":\s*\"([^\"]+)\"[^\{\}\[\]]*?\"page_id\":\s*\"?(\d+)\"?', content)
            if not pairs:
                pairs = re.findall(r'\"page_id\":\s*\"?(\d+)\"?[^\{\}\[\]]*?\"page_name\":\s*\"([^\"]+)\"', content)
                pairs = [(p[1], p[0]) for p in pairs]

            # Find best matching page_name
            target_words = [w.lower() for w in re.findall(r'[a-zA-Z0-9]+', search_target) if len(w) >= 2]
            for pn, pid in pairs:
                pn_low = pn.lower()
                if any(w in pn_low for w in target_words) or clean_q in pn_low.replace(" ", ""):
                    print(f"🎯 [PAGE RESOLVER] Auto-discovered: '{pn}' -> Page ID: {pid}")
                    save_page_id(search_target, pid, pn, clean_d)
                    return {"page_id": pid, "page_name": pn, "canonical_domain": clean_d}
    except Exception as e:
        print(f"⚠️ [PAGE RESOLVER PROBE ERROR] {e}")

    return None


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 TESTING META FACEBOOK PAGE ID RESOLVER")
    print("=" * 60)
    for q, d in [("ridge.com", "ridge.com"), ("The Oodie", "theoodie.com"), ("True Sea Moss", "trueseamoss.com"), ("CRZ Yoga", "crzyoga.com")]:
        res = resolve_facebook_page_id(q, domain=d, allow_live_probe=False)
        print(f"Query '{q}' -> Page ID: {res['page_id'] if res else 'None'} ({res['page_name'] if res else 'N/A'})")
    print("=" * 60)
