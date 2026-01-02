from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from app.db import get_conn
from app.features.area.service import geocode_address  # ★ 追加

router = APIRouter(prefix="/api/area", tags=["area"])

# 住所で受け取り、サーバ側でジオコーディングするモデル
class HotelUpsertByAddress(BaseModel):
    id: str
    name: Optional[str] = None
    address: str = Field(..., description="ホテルの住所（日本国内）")
    nationality_iso: Optional[str] = Field(None, description="例: US, KR, CN など2文字")

UPSERT_SQL = """
INSERT INTO public.hotels (id,name,address,lat,lng,nationality_iso)
VALUES ($1,$2,$3,$4,$5,UPPER($6))
ON CONFLICT (id) DO UPDATE
SET name=EXCLUDED.name, address=EXCLUDED.address,
    lat=EXCLUDED.lat, lng=EXCLUDED.lng,
    nationality_iso=EXCLUDED.nationality_iso;
"""

@router.post("/hotels")
async def register_hotel(h: HotelUpsertByAddress):
    # 住所 → 座標に変換
    lat, lng = geocode_address(h.address)
    if lat is None or lng is None:
        raise HTTPException(400, detail="Geocoding failed for the given address")

    # DB に upsert（既存 schema を踏襲）
    async with get_conn() as conn:
        await conn.execute(
            UPSERT_SQL,
            h.id,
            h.name,
            h.address,
            float(lat),
            float(lng),
            h.nationality_iso or "",
        )
    return {"ok": True, "hotel_id": h.id, "lat": lat, "lng": lng}