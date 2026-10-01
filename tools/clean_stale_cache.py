#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cache Auto-Heal Script — clean_stale_cache.py
=============================================
Scans out/spy_cache/*.json for stale/incorrect entries:
  - logo_url = ui-avatars.com  (fake initials avatar — must be healed)
  - brand_name missing or wrong
  - tiktok_slug missing

Re-fetches real data using store_intelligence.extract_website_ground_truth()
and patches the cache files in place.

Usage:
    python tools/clean_stale_cache.py          # dry run (show what would change)
    python tools/clean_stale_cache.py --apply  # actually overwrite cache files
"""

import os
import sys
import json
import re
import argparse
import time

# Make sure parent dir is in path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import store_intelligence as si

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", "spy_cache")

STALE_PATTERNS = [
    "ui-avatars.com",
    "https://ui-avatars",
]

def is_stale(data: dict) -> bool:
    """Returns True if this cache entry has known bad logo or is missing ground truth."""
    logo = data.get("logo_url") or data.get("brand_logo") or ""
    if any(p in logo for p in STALE_PATTERNS):
        return True
    if not data.get("ground_truth"):
        return True
    return False

def extract_domain_from_cache(data: dict, filename: str) -> str:
    """Best-effort: get the domain from the cached data or filename."""
    domain = (
        data.get("domain") or
        data.get("verified_domain") or
        data.get("brand_domain") or
        ""
    ).strip().lower()
    if domain:
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^(www)\\.', '', domain)
        domain = domain.split('/')[0]
    if not domain or '.' not in domain:
        # Derive from filename: "the_oodie.json" → "theoodie.com"
        base = os.path.splitext(os.path.basename(filename))[0]
        base = base.replace('_', '').replace('-', '')
        domain = base + ".com"
    return domain

def heal_cache_file(filepath: str, apply: bool) -> bool:
    """
    Reads a cache JSON, checks if stale, and heals it.
    Returns True if a change was (or would be) made.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ⚠️  SKIP (invalid JSON): {os.path.basename(filepath)} — {e}")
            return False

    if not isinstance(data, dict):
        print(f"  ⚠️  SKIP (not a dict): {os.path.basename(filepath)} — root type: {type(data).__name__}")
        return False

    if not is_stale(data):
        print(f"  ✅ OK   : {os.path.basename(filepath)}")
        return False


    domain = extract_domain_from_cache(data, filepath)
    print(f"  🔧 STALE: {os.path.basename(filepath)} (domain={domain})")
    print(f"           old logo: {(data.get('logo_url') or '')[:80]}")

    # Fetch ground truth
    gt = si.extract_website_ground_truth(domain)
    new_logo  = gt.get("logo_url") or ""
    new_name  = gt.get("brand_name") or data.get("name") or data.get("brand_name") or ""
    new_slug  = gt.get("tiktok_slug") or ""
    new_domain = gt.get("canonical_domain") or domain

    print(f"           new logo: {new_logo[:80]}")
    print(f"           brand   : {new_name}")
    print(f"           tiktok  : #{new_slug}")

    if not apply:
        print(f"           [DRY RUN] Would patch — use --apply to save")
        return True

    # Patch data
    if new_logo and "ui-avatars" not in new_logo:
        data["logo_url"]   = new_logo
        data["brand_logo"] = new_logo
    if new_name:
        data["brand_name"] = new_name
        if not data.get("name"):
            data["name"] = new_name
    if new_slug:
        data["tiktok_slug"]    = new_slug
        data["tiktok_handle"]  = f"@{new_slug}"
        data["tiktok_hashtag"] = f"#{new_slug}"
    data["verified_domain"] = new_domain
    data["ground_truth"] = {
        "brand_name": new_name,
        "logo_url":   new_logo,
        "tiktok_slug": new_slug,
        "canonical_domain": new_domain,
        "_source": gt.get("_source", "website_crawl"),
        "_healed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"           ✅ HEALED and saved.")
    return True


def main():
    parser = argparse.ArgumentParser(description="TrendTrack Cache Auto-Heal Tool")
    parser.add_argument("--apply", action="store_true", help="Actually write changes (default: dry run)")
    parser.add_argument("--dir",   default=CACHE_DIR,   help="Cache directory path")
    args = parser.parse_args()

    cache_dir = args.dir
    if not os.path.isdir(cache_dir):
        print(f"❌ Cache directory not found: {cache_dir}")
        sys.exit(1)

    json_files = sorted([
        os.path.join(cache_dir, f)
        for f in os.listdir(cache_dir)
        if f.endswith(".json")
    ])

    print(f"\n{'='*60}")
    print(f"TrendTrack Cache Auto-Heal — {'APPLY MODE' if args.apply else 'DRY RUN'}")
    print(f"Cache dir : {cache_dir}")
    print(f"Files     : {len(json_files)}")
    print(f"{'='*60}\n")

    healed = 0
    ok = 0
    for fp in json_files:
        changed = heal_cache_file(fp, args.apply)
        if changed:
            healed += 1
            time.sleep(0.5)  # be polite to websites when fetching
        else:
            ok += 1

    print(f"\n{'='*60}")
    print(f"✅ Clean  : {ok}")
    print(f"🔧 {'Healed' if args.apply else 'Would heal'} : {healed}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
