# app/features/area/repo.py
from sqlalchemy import text
from app.db import Session

UPSERT_SQL = text("""
INSERT INTO area.hotels (id,name,address,lat,lng,nationality_iso)
VALUES (:id,:name,:address,:lat,:lng,:iso)
ON CONFLICT (id) DO UPDATE
SET name=EXCLUDED.name,
    address=EXCLUDED.address,
    lat=EXCLUDED.lat,
    lng=EXCLUDED.lng,
    nationality_iso=EXCLUDED.nationality_iso;
""")

async def upsert_hotel(hotel):
    async with Session() as s:
        await s.execute(UPSERT_SQL, hotel)
        await s.commit()