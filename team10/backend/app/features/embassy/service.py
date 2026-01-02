# backend/app/features/embassy/service.py
from __future__ import annotations
from typing import List, Dict, Any, Optional
import json
import os
import math

import pycountry
from rapidfuzz import fuzz, process  # 多少のゆらぎ対応（例: "U.S.A." → "United States"）

# embassies.json のロード
BASE_DIR = os.path.dirname(__file__)
RES_PATH = os.path.join(BASE_DIR, "resources", "embassies.json")
with open(RES_PATH, "r", encoding="utf-8") as f:
    EMBASSIES: List[Dict[str, Any]] = json.load(f)

# 国名の別名 → 正式英語名の手当て
MANUAL_COUNTRY_ALIASES = {
    "USA": "United States",
    "U.S.A.": "United States",
    "United States of America": "United States",
    "Korea": "South Korea",
    "Republic of Korea": "South Korea",
    "UK": "United Kingdom",
    "Great Britain": "United Kingdom",
    "Britain": "United Kingdom",
    "Viet Nam": "Vietnam",
    "Russian Federation": "Russia",
    # 日本語の通称
    "中国": "China",
    "韓国": "South Korea",
    "米国": "United States",
    "英国": "United Kingdom",
    "豪州": "Australia",
    "UAE": "United Arab Emirates",
}

def _country_display_to_iso2(country_name: str) -> Optional[str]:
    """
    ユーザー入力の国名（英語または一部日本語通称）→ ISO2（US/FR/CN...）に変換。
    1) 手当て辞書で正規化
    2) RapidFuzz で正式名称に近似マッチ
    3) pycountry で ISO2 を取得
    """
    if not country_name:
        return None
    name = country_name.strip()
    name = MANUAL_COUNTRY_ALIASES.get(name, name)

    # 近似候補（正式英語名の集合へマッチ）
    all_names = [c.name for c in pycountry.countries]
    match = process.extractOne(name, all_names, scorer=fuzz.WRatio)
    if match and match[1] >= 90:
        name = match[0]

    try:
        c = pycountry.countries.lookup(name)
        return c.alpha_2.upper()
    except Exception:
        return None

def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """2点間のハバースイン距離（メートル）"""
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def find_nearest(lat: float, lng: float, nationality_display: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    embassies.json から nationality_display（例: "United States"）を ISO2 に変換し、
    represented_iso が一致する大使館をユーザー位置からの距離順に返す。
    """
    iso2 = _country_display_to_iso2(nationality_display)
    if not iso2:
        return []

    items: List[Dict[str, Any]] = []
    for e in EMBASSIES:
        if (e.get("represented_iso") or "").upper() != iso2:
            continue
        elat, elng = float(e["lat"]), float(e["lng"])
        dist = _haversine(lat, lng, elat, elng)
        items.append({
            "name_en": e.get("name_en"),
            "name_ja": e.get("name_ja"),
            "represented_iso": e.get("represented_iso"),
            "phone": e.get("phone"),
            "website": e.get("website"),
            "lat": elat,
            "lng": elng,
            "dist_m": dist,
        })

    items.sort(key=lambda x: x["dist_m"])
    # limit の最低1保障
    safe_limit = max(1, int(limit))
    return items[:safe_limit]