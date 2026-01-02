# backend/app/features/mailer/service.py
from __future__ import annotations
import os, smtplib
from email.message import EmailMessage
from typing import Any, Dict, List, Optional

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS", SMTP_USER or "no-reply@example.com")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "SafeTravel")

def build_reservation_email(
    address: str,
    nationality: Optional[str],
    embassies: List[Dict[str, Any]],
) -> tuple[str, str]:
    """件名と本文を返す（routerが期待してる名前）"""
    subject = "Your Stay & Nearby Embassies"
    lines = []
    lines.append("Your reservation & nearby embassies")
    lines.append("")
    lines.append(f"Hotel address: {address}")
    if nationality:
        lines.append(f"Nationality: {nationality}")
    lines.append("")
    lines.append("Nearest embassies:")
    if not embassies:
        lines.append("- (No embassy found for the specified nationality)")
    else:
        for e in embassies[:3]:
            nm = f"{e.get('name_en','')}"
            if e.get("name_ja"):
                nm += f" / {e['name_ja']}"
            dist = e.get("dist_m")
            dist_km = f"{dist/1000:.2f} km" if isinstance(dist, (int, float)) else "n/a"
            lines.append(f"- {nm}  ({dist_km})")
            if e.get("phone"):   lines.append(f"  phone: {e['phone']}")
            if e.get("website"): lines.append(f"  site:  {e['website']}")
    lines.append("")
    lines.append("Japan Emergency: Police 110 / Ambulance & Fire 119")
    lines.append("You can find more information here: http://localhost:3000/info")
    body = "\n".join(lines)
    return subject, body

def send_mail(to: str, subject: str, body: str) -> Dict[str, Any]:
    """素のメール送信（routerが期待してる名前）"""
    if not to:
        raise ValueError("to is required")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM_ADDRESS}>"
    msg["To"] = to
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.ehlo(); s.starttls(); s.ehlo()
            if SMTP_USER and SMTP_PASS:
                s.login(SMTP_USER, SMTP_PASS)
            resp = s.send_message(msg)
        return {"status": "sent" if not resp else "partial", "provider": "smtp", "message_id": None}
    except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError(f"SMTP auth failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"SMTP send failed: {e}") from e

# 便利ラッパー（統合API側から使える）
def send_reservation_email(to: str, address: str, nationality: Optional[str], embassies: List[Dict[str, Any]]) -> Dict[str, Any]:
    subject, body = build_reservation_email(address, nationality, embassies)
    return send_mail(to, subject, body)