from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any

from app.features.area.service import geocode_address
from app.features.embassy.service import find_nearest
from app.features.mailer.service import send_reservation_email

router = APIRouter(prefix="/api/reservation", tags=["reservation"])

class SubmitReq(BaseModel):
    to: EmailStr
    address: str
    nationality: Optional[str] = None
    limit: int = Field(default=3, ge=1, le=10)

class SubmitRes(BaseModel):
    hotel: Dict[str, Any]
    embassies: List[Dict[str, Any]]
    jp_emergency: List[Dict[str, str]]
    mail: Dict[str, Any]

@router.post("/submit", response_model=SubmitRes)
def submit(req: SubmitReq):
    # 1) 住所→座標
    try:
        lat, lng = geocode_address(req.address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"GEOCODE_FAILED: {e}")
    if lat is None or lng is None:
        raise HTTPException(status_code=400, detail="GEOCODE_FAILED")

    # 2) 最寄り公館（service.py の find_nearest をそのまま使用）
    emb_list = find_nearest(lat, lng, req.nationality or "", req.limit)

    # 3) メール送信
    try:
        mail_result = send_reservation_email(
            to=req.to,
            address=req.address,
            nationality=req.nationality,
            embassies=emb_list,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"SMTP_DOWNSTREAM_ERROR: {e}")

    return {
        "hotel": {"address": req.address, "lat": lat, "lng": lng},
        "embassies": emb_list,
        "jp_emergency": [
            {"number": "110", "desc_en": "Police", "desc_ja": "警察"},
            {"number": "119", "desc_en": "Ambulance/Fire", "desc_ja": "救急・消防"},
        ],
        "mail": mail_result,
    }