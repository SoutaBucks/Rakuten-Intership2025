from __future__ import annotations
from fastapi import APIRouter, Body, HTTPException
from typing import Any, Dict, List

from app.features.area.service import geocode_address
from .service import find_nearest  # embassies.json から距離順に返す

router = APIRouter(prefix="/api/embassy", tags=["embassy"])

@router.post("/near")  # ← response_model をやめる
async def embassy_near(payload: Dict[str, Any] = Body(...)):
    """
    期待するJSON:
    {
      "address": "東京都新宿区西新宿2-8-1",
      "nationality": "United States",
      "limit": 3   // 省略可
    }
    """
    address = payload.get("address")
    nationality = payload.get("nationality")
    limit = payload.get("limit", 3)

    # 最低限の手動チェック
    if not isinstance(address, str) or not address.strip():
        raise HTTPException(400, "'address' is required (string).")
    if not isinstance(nationality, str) or not nationality.strip():
        raise HTTPException(400, "'nationality' is required (string).")
    try:
        limit = int(limit)
        if not (1 <= limit <= 10):
            raise ValueError()
    except Exception:
        raise HTTPException(400, "'limit' must be an integer between 1 and 10.")

    # 住所→座標
    lat, lng = geocode_address(address)
    if lat is None or lng is None:
        raise HTTPException(400, "Geocoding failed")

    # 国籍表示名→ISO2変換＆最寄り大使館
    embassies = find_nearest(lat=lat, lng=lng, nationality_display=nationality, limit=limit)

    # 素のdictで返却
    return {
        "point": {"address": address, "lat": lat, "lng": lng},
        "embassies": embassies,
        "jp_emergency": [
            {"number": "110", "desc_en": "Police", "desc_ja": "警察"},
            {"number": "119", "desc_en": "Ambulance/Fire", "desc_ja": "救急・消防"},
        ],
    }