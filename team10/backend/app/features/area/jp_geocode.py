# -*- coding: utf-8 -*-
# 日本住所向けのジオコーディング（ArcGIS → Nominatim の順）
# 命中した座標が日本国内で、かつ住所に「東京都／◯◯区」など
# 入力に含まれる主要キーワードが含まれている場合のみ採用する。
import re
from typing import Optional, Tuple
from geopy.geocoders import ArcGIS, Nominatim
from geopy.extra.rate_limiter import RateLimiter

_arc = ArcGIS(timeout=10)
_nom = Nominatim(user_agent="team10-safestay", timeout=10)
_nom_geocode = RateLimiter(_nom.geocode, min_delay_seconds=1.0)

# 日本のざっくりバウンディングボックス（緯度経度）
JP_BBOX = (20.0, 122.0, 46.5, 154.0)  # (S, W, N, E)

def _in_japan(lat: float, lng: float) -> bool:
    s, w, n, e = JP_BBOX
    return s <= lat <= n and w <= lng <= e

def _variants(addr: str):
    """候補文字列を複数生成：'丁目' 付与や '日本' 付加など"""
    a = (addr or "").strip().replace("　", " ")
    cands = [a, f"{a}, 日本"]
    if "東京" in a or "東京都" in a:
        cands.append(f"{a}, 東京都, 日本")
    # 2-8-1 → 2丁目8-1（すでに丁目があれば触らない）
    if "丁目" not in a:
        m = re.search(r"(\d+)-(\d+)-(\d+)", a)
        if m:
            cands.append(re.sub(r"(\d+)-(\d+)-(\d+)", r"\1丁目\2-\3", a))
    # 重複除去（順序維持）
    seen, out = set(), []
    for q in cands:
        if q not in seen:
            out.append(q); seen.add(q)
    return out

def _required_match(input_addr: str, resolved_addr: str) -> bool:
    """入力に含まれる主要キーワード（例：東京都、新宿区）が解決先にも含まれるか"""
    r = resolved_addr or ""
    if "東京都" in input_addr and "東京都" not in r:
        return False
    m = re.search(r"([^\d\s,、]+区)", input_addr)  # 例: 新宿区, 渋谷区
    if m and m.group(1) not in r:
        return False
    return True

def geocode_address_jp(address: str) -> Optional[Tuple[float, float]]:
    # 1) ArcGIS を優先
    for q in _variants(address):
        try:
            loc = _arc.geocode(q)
        except Exception:
            loc = None
        if loc and _in_japan(loc.latitude, loc.longitude) and _required_match(address, loc.address or ""):
            return (loc.latitude, loc.longitude)

    # 2) ダメなら Nominatim（日本限定・日本語優先）
    for q in _variants(address):
        try:
            loc = _nom_geocode(q, country_codes="jp", language="ja",
                               addressdetails=False, exactly_one=True)
        except Exception:
            loc = None
        # Nominatim の住所文字列は raw.display_name に入ることが多い
        resolved = ""
        if getattr(loc, "address", None):
            resolved = str(loc.address)
        elif getattr(loc, "raw", None):
            resolved = loc.raw.get("display_name", "")
        if loc and _in_japan(loc.latitude, loc.longitude) and _required_match(address, resolved):
            return (loc.latitude, loc.longitude)

    return None  # ここまで来たら「命中なし」
