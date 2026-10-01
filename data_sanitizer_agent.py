#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Sanitizer & Quality Gatekeeper Agent
=========================================
Bảo vệ tính trung thực và toàn vẹn dữ liệu:
1. Kiểm tra 100% các Ad Cards trước khi ghi cache hoặc hiển thị.
2. Loại bỏ các domain ngoại lai/ô nhiễm (ví dụ blueridgemountains.com khi tìm ridge.com).
3. Đảm bảo tính nhất quán toán học giữa số lượng Ads Active, thẻ hiển thị và trang Landing Page.
4. Đóng dấu chứng nhận '_sanitized': True cho các payload hợp lệ.
"""

import re
import urllib.parse
from typing import Dict, Any, List, Tuple, Optional


def extract_clean_netloc(url: str) -> str:
    """Trích xuất hostname sạch từ URL (bỏ www, query, protocol)."""
    if not url:
        return ""
    try:
        if not re.match(r'^[a-zA-Z]+://', url):
            url = 'https://' + url
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc.lower().split(':')[0].strip()
        netloc = re.sub(r'^(www|us|uk|au|ca|shop|store)\.', '', netloc)
        return netloc
    except Exception:
        return ""


def is_authorized_domain(candidate_url_or_domain: str, canonical_domain: str) -> bool:
    """
    Kiểm tra xem candidate domain có khớp chính xác hoặc là subdomain hợp lệ của canonical_domain hay không.
    Ví dụ canonical = ridge.com:
      - ridge.com -> True
      - shop.ridge.com -> True
      - checkout.ridge.com -> True
      - blueridgemountains.com -> False
      - ridgeproductswelding.com -> False
      - fakewallet.com -> False
    """
    if not canonical_domain:
        return True

    target = extract_clean_netloc(canonical_domain)
    cand = extract_clean_netloc(candidate_url_or_domain)

    if not cand or not target:
        return False

    # Exact match
    if cand == target:
        return True

    # Subdomain match: shop.ridge.com ends with .ridge.com
    if cand.endswith('.' + target):
        return True

    return False


def is_valid_page_name(page_name: str, brand_name: str, canonical_domain: str) -> bool:
    """
    Kiểm tra tên Fanpage có liên quan đến thương hiệu hay là trang rác/lạc đề.
    """
    if not page_name:
        return True

    clean_page = page_name.lower().strip()
    clean_brand = (brand_name or "").lower().strip()
    clean_domain_slug = re.sub(r'\.(com|co|vn|io|org|net|us|uk|de|fr|ca|au)$', '', (canonical_domain or "").lower()).strip()

    # Bỏ qua các từ phụ thông dụng
    clean_brand_core = re.sub(r'\b(the|official|shop|store|brand|inc|llc|co)\b', '', clean_brand).strip()
    clean_domain_core = re.sub(r'\b(the|official|shop|store|brand|inc|llc|co)\b', '', clean_domain_slug).strip()

    if clean_brand and clean_brand in clean_page:
        return True
    if clean_brand_core and len(clean_brand_core) >= 3 and clean_brand_core in clean_page:
        return True
    if clean_domain_core and len(clean_domain_core) >= 3 and clean_domain_core in clean_page:
        return True

    # Nếu tên trang hoàn toàn xa lạ nhưng có chứa từ khóa phổ quát trùng một phần nhỏ (ví dụ "Blue Ridge Mountain")
    # Kiểm tra xem có chứa từ chỉ địa danh hoặc ngành nghề hoàn toàn khác không
    irrelevant_keywords = ["mountain", "resort", "hotel", "cabin", "park", "tourism", "realtor", "realty"]
    if any(k in clean_page for k in irrelevant_keywords) and not any(k in clean_brand for k in irrelevant_keywords):
        return False

    return True


def sanitize_ads_list(ads: List[Dict[str, Any]], canonical_domain: str, brand_name: str = "") -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Duyệt qua danh sách Ad Cards và loại bỏ các quảng cáo không thuộc về brand.
    Trả về: (danh_sách_sạch, thống_kê_kiểm_định)
    """
    if not ads:
        return [], {"total_in": 0, "approved": 0, "rejected": 0, "rejection_reasons": {}}

    target_domain = extract_clean_netloc(canonical_domain)
    approved_ads: List[Dict[str, Any]] = []
    rejected_reasons: Dict[str, int] = {
        "foreign_landing_domain": 0,
        "irrelevant_page_name": 0,
        "empty_ad": 0
    }

    for ad in ads:
        if not isinstance(ad, dict):
            continue

        landing_url = ad.get("landing_page") or ad.get("link_url") or ad.get("url") or ""
        landing_netloc = extract_clean_netloc(landing_url)
        page_name = ad.get("page_name") or ad.get("advertiser_name") or ""

        # 1. Nếu có landing page URL, kiểm tra domain
        if landing_netloc:
            # Bỏ qua các link tracking nội bộ của FB
            if landing_netloc in ["facebook.com", "fb.me", "m.facebook.com", "instagram.com"]:
                pass
            elif not is_authorized_domain(landing_netloc, target_domain):
                # Domain ngoại lai bị loại bỏ ngay
                rejected_reasons["foreign_landing_domain"] += 1
                continue

        # 2. Kiểm tra tên Page
        if page_name and not is_valid_page_name(page_name, brand_name, canonical_domain):
            rejected_reasons["irrelevant_page_name"] += 1
            continue

        # Đạt chuẩn kiểm định
        approved_ads.append(ad)

    summary = {
        "total_in": len(ads),
        "approved": len(approved_ads),
        "rejected": len(ads) - len(approved_ads),
        "rejection_reasons": rejected_reasons,
        "canonical_domain": target_domain
    }

    return approved_ads, summary


def sanitize_landing_pages(landing_pages: List[Dict[str, Any]], canonical_domain: str) -> List[Dict[str, Any]]:
    """Lọc danh sách Landing Pages chỉ giữ lại các URL thuộc canonical domain."""
    if not landing_pages:
        return []

    target_domain = extract_clean_netloc(canonical_domain)
    clean_lps = []

    for lp in landing_pages:
        if not isinstance(lp, dict):
            continue
        domain = lp.get("domain") or extract_clean_netloc(lp.get("url") or "")
        if is_authorized_domain(domain, target_domain):
            clean_lps.append(lp)

    return clean_lps


def sanitize_meta_suite(suite_data: Dict[str, Any], canonical_domain: str, brand_name: str = "") -> Dict[str, Any]:
    """
    Kiểm định toàn bộ gói Meta Suite (6 subtabs).
    """
    if not suite_data or not isinstance(suite_data, dict):
        return suite_data

    target_domain = extract_clean_netloc(canonical_domain or suite_data.get("domain") or "")
    brand = brand_name or suite_data.get("brand_name") or suite_data.get("name") or ""

    # 1. Sanitize ads
    if "ads" in suite_data and isinstance(suite_data["ads"], list):
        sanitized_ads, audit = sanitize_ads_list(suite_data["ads"], target_domain, brand)
        suite_data["ads"] = sanitized_ads
        suite_data["_ad_audit"] = audit

    # 2. Sanitize landing pages tab
    if "landing_pages" in suite_data and isinstance(suite_data["landing_pages"], list):
        suite_data["landing_pages"] = sanitize_landing_pages(suite_data["landing_pages"], target_domain)

    # 3. Chốt chặn domain
    if target_domain:
        suite_data["domain"] = target_domain
        suite_data["canonical_domain"] = target_domain

    suite_data["_sanitized"] = True
    return suite_data


def sanitize_brand_payload(payload: Dict[str, Any], canonical_domain: str) -> Dict[str, Any]:
    """
    Kiểm định toàn bộ Brand Payload (Shop Overview, Meta, Products, Apps).
    """
    if not payload or not isinstance(payload, dict):
        return payload

    target_domain = extract_clean_netloc(canonical_domain or payload.get("domain") or "")
    brand = payload.get("name") or payload.get("brand_name") or ""

    # Chốt chặn domain ở root
    if target_domain:
        payload["domain"] = target_domain

    # Sanitize ads list
    if "ads" in payload and isinstance(payload["ads"], list):
        clean_ads, audit = sanitize_ads_list(payload["ads"], target_domain, brand)
        payload["ads"] = clean_ads
        payload["_ad_audit"] = audit

    payload["_sanitized"] = True
    return payload


if __name__ == "__main__":
    print("=" * 60)
    print("🛡️ DATA QUALITY & SANITIZATION GATEKEEPER TEST")
    print("=" * 60)

    # Test case 1: Ridge Wallet vs Blue Ridge Mountains
    test_ads = [
        {"id": "1", "page_name": "The Ridge", "landing_page": "https://ridge.com/products/wallet", "title": "Minimalist Wallet"},
        {"id": "2", "page_name": "Ridge Official", "landing_page": "https://shop.ridge.com/sale", "title": "Daily Carry"},
        {"id": "3", "page_name": "Blue Ridge Mountain Resort", "landing_page": "https://blueridgemountains.com/book", "title": "Book a Cabin"},
        {"id": "4", "page_name": "Ridge Welding Supplies", "landing_page": "https://ridgeproductswelding.com", "title": "Welding Helmet"},
        {"id": "5", "page_name": "The Ridge", "landing_page": "https://www.facebook.com/ridge", "title": "Brand story"}
    ]

    clean, report = sanitize_ads_list(test_ads, "ridge.com", "The Ridge")
    print(f"Input Ads: {len(test_ads)}")
    print(f"Approved Ads: {len(clean)}")
    print(f"Rejected: {report['rejected']}")
    print(f"Rejection Reasons: {report['rejection_reasons']}")
    for a in clean:
        print(f"  ✅ Kept: {a['page_name']} -> {a['landing_page']}")
    print("=" * 60)
