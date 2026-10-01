"""
Smart Cache Manager with Time-To-Live (TTL) & Incremental Delta Merge
Enterprise-grade caching for TrendTrack SaaS
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "spy_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Default TTLs (in seconds)
DEFAULT_TTL = {
    "meta_ads": 12 * 3600,     # 12 hours
    "google_ads": 24 * 3600,   # 24 hours
    "tiktok": 12 * 3600,       # 12 hours
    "emails": 24 * 3600,       # 24 hours
    "meta_ranking": 12 * 3600  # 12 hours
}

class SmartCacheManager:
    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = cache_dir

    def _get_path(self, key: str) -> str:
        clean_key = key.replace("/", "_").replace("\\", "_")
        if not clean_key.endswith(".json"):
            clean_key += ".json"
        return os.path.join(self.cache_dir, clean_key)

    def get(self, key: str, max_age_seconds: Optional[int] = None) -> Tuple[Optional[Dict[str, Any]], bool]:
        """
        Retrieves cache entry.
        Returns: (data, is_stale)
        If not found: (None, True)
        """
        path = self._get_path(key)
        if not os.path.exists(path):
            return None, True

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check metadata or fallback to file modification time
            meta = data.get("_cache_meta", {})
            crawled_at = meta.get("crawled_at", 0)
            if crawled_at <= 0:
                try:
                    crawled_at = os.path.getmtime(path)
                except Exception:
                    crawled_at = 0
            
            ttl = max_age_seconds or meta.get("ttl", 12 * 3600)
            now = time.time()
            is_stale = (now - crawled_at) > ttl if crawled_at > 0 else True
            return data, is_stale
        except Exception as e:
            print(f"⚠️ [CACHE MANAGER] Error reading cache {key}: {e}")
            return None, True

    def set(self, key: str, data: Dict[str, Any], ttl_seconds: int = 12 * 3600) -> bool:
        """Saves data with TTL metadata."""
        path = self._get_path(key)
        now = time.time()
        
        # Inject cache metadata without polluting business logic
        data_to_store = dict(data)
        data_to_store["_cache_meta"] = {
            "crawled_at": now,
            "crawled_at_iso": datetime.utcnow().isoformat() + "Z",
            "ttl": ttl_seconds,
            "expires_at": now + ttl_seconds,
            "version": "2.0"
        }

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data_to_store, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ [CACHE MANAGER] Error writing cache {key}: {e}")
            return False

    def merge_delta(
        self,
        key: str,
        new_items: List[Dict[str, Any]],
        id_field: str = "id",
        items_field: str = "ads",
        ttl_seconds: int = 12 * 3600
    ) -> Dict[str, Any]:
        """
        Incremental Delta Merge:
        - Detects truly new items by ID
        - Prepends new items to the front
        - Updates metrics on existing items
        - Preserves historical records
        """
        existing_data, _ = self.get(key)
        if not existing_data or items_field not in existing_data:
            # First time save
            container = {items_field: new_items, "total_items": len(new_items)}
            self.set(key, container, ttl_seconds)
            return container

        existing_list = existing_data.get(items_field, [])
        existing_map = {item.get(id_field): idx for idx, item in enumerate(existing_list) if item.get(id_field)}

        brand_new_items = []
        updated_count = 0

        for item in new_items:
            item_id = item.get(id_field)
            if not item_id or item_id not in existing_map:
                brand_new_items.append(item)
            else:
                # Update metrics on existing item
                idx = existing_map[item_id]
                existing_list[idx].update(item)
                updated_count += 1

        # Combine: New items in front, followed by preserved existing items
        merged_list = brand_new_items + existing_list
        existing_data[items_field] = merged_list
        existing_data["total_items"] = len(merged_list)
        existing_data["new_items_delta"] = len(brand_new_items)
        existing_data["updated_items_delta"] = updated_count

        print(f"🔄 [CACHE DELTA] Key '{key}': Found {len(brand_new_items)} new items, updated {updated_count} existing items.")
        self.set(key, existing_data, ttl_seconds)
        return existing_data

    def purge_brand(self, brand: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Atomically discovers and deletes ALL cache files related to a brand/domain across:
        - out/spy_cache/
        - data_cache/store_history/
        """
        import re
        deleted_files = []
        clean_brand = re.sub(r'[^a-z0-9]', '', (brand or "").lower())
        clean_domain = re.sub(r'[^a-z0-9]', '', (domain or "").lower())
        
        domain_stem = ""
        if domain:
            d_clean = re.sub(r'^https?://', '', domain.lower()).split('/')[0].strip()
            domain_stem = re.sub(r'\.(com|co|vn|io|shop|store|org|net|us|uk|de|fr|ca|au)$', '', d_clean)
            domain_stem = re.sub(r'[^a-z0-9]', '', domain_stem)

        stems = set(filter(None, [clean_brand, clean_domain, domain_stem]))
        # Remove overly generic stems
        stems = {s for s in stems if len(s) >= 3 and s not in ["com", "shop", "store", "the", "official"]}

        if not stems:
            return {"success": False, "error": "No valid brand stems found to purge", "deleted_files": []}

        # 1. Purge matching files in out/spy_cache
        if os.path.exists(self.cache_dir):
            for fname in os.listdir(self.cache_dir):
                if not fname.endswith(".json"):
                    continue
                fname_clean = re.sub(r'[^a-z0-9]', '', fname.lower().replace(".json", ""))
                
                # Check if any stem is part of filename with separator awareness
                matched = False
                for stem in stems:
                    # Match exact stem or stem delimited by separators or as a major component
                    pattern = rf'(^|_|-|\.){re.escape(stem)}(_|-|\.|\d|$)'
                    if re.search(pattern, fname.lower()) or fname_clean == stem or fname_clean.startswith(stem) or fname_clean.endswith(stem):
                        matched = True
                        break

                if matched:
                    fpath = os.path.join(self.cache_dir, fname)
                    try:
                        os.remove(fpath)
                        deleted_files.append(f"spy_cache/{fname}")
                    except Exception as e:
                        print(f"⚠️ [PURGE] Error deleting {fpath}: {e}")

        # 2. Purge in data_cache/store_history
        hist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cache", "store_history")
        if os.path.exists(hist_dir):
            for fname in os.listdir(hist_dir):
                if not fname.endswith(".json"):
                    continue
                fname_clean = re.sub(r'[^a-z0-9]', '', fname.lower().replace(".json", ""))
                matched = any(stem in fname_clean for stem in stems)
                if matched:
                    fpath = os.path.join(hist_dir, fname)
                    try:
                        os.remove(fpath)
                        deleted_files.append(f"store_history/{fname}")
                    except Exception as e:
                        print(f"⚠️ [PURGE] Error deleting {fpath}: {e}")

        # 3. Clear in-memory caches
        try:
            import store_intelligence as _si
            if hasattr(_si, "_GROUND_TRUTH_CACHE"):
                _si._GROUND_TRUTH_CACHE.clear()
        except Exception:
            pass

        try:
            import meta_ads_agent as _maa
            if hasattr(_maa, "_SUITE_CACHE"):
                _maa._SUITE_CACHE.clear()
        except Exception:
            pass

        print(f"🗑️ [CACHE PURGED] Brand: '{brand}' Domain: '{domain}' -> Deleted {len(deleted_files)} files: {deleted_files}")
        return {
            "success": True,
            "brand": brand,
            "domain": domain,
            "deleted_count": len(deleted_files),
            "deleted_files": deleted_files
        }


def purge_brand_cache(brand: str, domain: Optional[str] = None) -> Dict[str, Any]:
    """Top-level helper to purge brand cache."""
    return smart_cache.purge_brand(brand, domain)


# Global instance
smart_cache = SmartCacheManager()
