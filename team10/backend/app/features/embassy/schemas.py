from pydantic import BaseModel
from typing import Optional

class Embassy(BaseModel):
    name_en: str
    name_ja: Optional[str] = None
    represented_iso: str
    phone: Optional[str] = None
    website: Optional[str] = None
    lat: float
    lng: float
    dist_m: float