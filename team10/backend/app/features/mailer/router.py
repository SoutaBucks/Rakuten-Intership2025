from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .service import send_mail, build_reservation_email

import urllib.parse
import os

router = APIRouter(prefix="/api/mailer", tags=["mailer"])

class SendReservationMail(BaseModel):
    to: EmailStr = Field(..., description="宛先メールアドレス")
    address: str = Field(..., description="ユーザーが入力した現在地の住所")
    nationality: str = Field(..., description="国籍（英語名: United States, France など）")
    link: Optional[str] = Field(None, description="フロントのディープリンク（未指定なら自動生成）")
    subject: Optional[str] = Field(None, description="件名（未指定ならデフォルト）")

@router.post("/send-reservation")
async def send_reservation_mail(payload: SendReservationMail):
    # link 未指定なら、環境変数 PUBLIC_BASE_URL を使って作る
    base_url = os.getenv("PUBLIC_BASE_URL", "http://localhost:5173")
    link = payload.link
    if not link:
        qs = urllib.parse.urlencode({
            "address": payload.address,
            "nationality": payload.nationality,
        })
        link = f"{base_url}/?{qs}"

    subject = payload.subject or "Your SafeTravel Link"

    text_body, html_body = build_reservation_email(
        address=payload.address,
        nationality=payload.nationality,
        link=link,
    )

    try:
        send_mail(
            to=payload.to,
            subject=subject,
            text_body=text_body,
            html_body=html_body,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    return {"ok": True, "sent_to": payload.to, "link": link}