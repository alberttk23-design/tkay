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

# Global instance
smart_cache = SmartCacheManager()
