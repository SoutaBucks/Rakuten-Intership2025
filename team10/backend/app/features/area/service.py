# backend/app/features/area/service.py
from __future__ import annotations
from typing import Optional, Tuple, List
import logging
import re

from geopy.geocoders import ArcGIS, Nominatim
from geopy.extra.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

# ---- 住所正規化（軽め） ----
def normalize_address(addr: str) -> str:
    if not addr:
        return ""
    s = addr.strip()
    s = s.replace("　", " ")              # 全角スペース → 半角
    s = re.sub(r"\s+", " ", s)            # 連続スペースを1つに
    return s

# ---- ジオコーダ（APIキー不要）----
def _arcgis_geocode(query: str, timeout: int = 8):
    g = ArcGIS(timeout=timeout)
    rl = RateLimiter(g.geocode, min_delay_seconds=0.0)
    # ArcGIS は exactly_one オプション不要（内部で1件返す）
    return rl(query)

def _nominatim_geocode(query: str, timeout: int = 10):
    g = Nominatim(user_agent="safetravel/1.0 (+hackathon)", timeout=timeout)
    rl = RateLimiter(g.geocode, min_delay_seconds=1.0)
    # 日本を優先（country_codes）、日本語レスポンス（language）
    return rl(query, exactly_one=True, country_codes="jp", language="ja")

# ---- 昨日の候補生成ロジック ----
def _build_variants_yesterday(addr: str) -> List[str]:
    """
    - 生/「, Japan」/「, 日本」
    - 東京/新宿/渋谷/品川/港区 を含むなら 「, 東京都, 日本」を追加
    - 大阪/梅田/難波/天王寺 を含むなら 「, 大阪府, 日本」を追加
    - 2-8-1 を 2丁目8-1 に置換した候補も追加
    """
    v: List[str] = [
        addr,
        f"{addr}, Japan",
        f"{addr}, 日本",
    ]
    if any(tok in addr for tok in ("東京", "新宿", "渋谷", "品川", "港区")):
        v.append(f"{addr}, 東京都, 日本")
    if any(tok in addr for tok in ("大阪", "梅田", "難波", "天王寺")):
        v.append(f"{addr}, 大阪府, 日本")

    m = re.search(r'(\d+)-(\d+)-(\d+)', addr)
    if m:
        chome = f"{m.group(1)}丁目{m.group(2)}-{m.group(3)}"
        replaced = addr.replace(m.group(0), chome)
        v.append(replaced)
        v.append(f"{replaced}, 日本")

    # 重複除去（順序保持）
    seen, out = set(), []
    for q in v:
        if q not in seen:
            seen.add(q)
            out.append(q)
    return out

# ---- 住所 → (lat, lng) ----
def geocode_address(address: str) -> Tuple[Optional[float], Optional[float]]:
    """
    住所を ArcGIS → Nominatim の順でジオコーディング。
    上のバリアント候補を順に当てて、最初にヒットした座標を返す。
    """
    addr = normalize_address(address)
    if not addr:
        return None, None

    candidates = _build_variants_yesterday(addr)

    # 1) ArcGIS
    for q in candidates:
        try:
            loc = _arcgis_geocode(q)
            if loc and getattr(loc, "latitude", None) and getattr(loc, "longitude", None):
                logger.info("[ArcGIS] %s -> (%s,%s)", q, loc.latitude, loc.longitude)
                return float(loc.latitude), float(loc.longitude)
        except Exception as e:
            logger.warning("[ArcGIS] failed for '%s': %s", q, e)

    # 2) Nominatim
    for q in candidates:
        try:
            loc = _nominatim_geocode(q)
            if loc and getattr(loc, "latitude", None) and getattr(loc, "longitude", None):
                logger.info("[Nominatim] %s -> (%s,%s)", q, loc.latitude, loc.longitude)
                return float(loc.latitude), float(loc.longitude)
        except Exception as e:
            logger.warning("[Nominatim] failed for '%s': %s", q, e)

    logger.error("Geocoding failed: %s", addr)
    return None, None

# ---- デバッグ用（候補と試行ログを返す）----
def geocode_candidates(address: str) -> dict:
    addr = normalize_address(address)
    tried: List[str] = []
    hits: List[str] = []
    seen = set()
    variants = _build_variants_yesterday(addr)

    # ArcGIS 候補
    for q in variants:
        tried.append(f"ArcGIS: {q}")
        try:
            loc = _arcgis_geocode(q)
            if loc and getattr(loc, "address", None):
                line = f"[ArcGIS] {loc.address}"
                if line not in seen:
                    seen.add(line)
                    hits.append(line)
        except Exception:
            pass

    # Nominatim 候補
    for q in variants:
        tried.append(f"Nominatim: {q}")
        try:
            loc = _nominatim_geocode(q)
            if loc and getattr(loc, "address", None):
                line = f"[Nominatim] {loc.address}"
                if line not in seen:
                    seen.add(line)
                    hits.append(line)
        except Exception:
            pass

    lat, lng = geocode_address(addr)
    return {
        "input": addr,
        "tried": tried,
        "candidates": hits[:10],
        "lat": lat,
        "lng": lng,
    }