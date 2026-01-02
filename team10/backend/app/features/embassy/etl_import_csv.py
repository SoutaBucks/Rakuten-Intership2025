# app/features/embassy/etl_import_csv.py
import csv
from pathlib import Path
from sqlalchemy import text
from app.db import Session

CSV_PATH = Path(__file__).parent / "data" / "embassies.csv"

SQL = text("""
INSERT INTO public.embassies (id, name_en, name_ja, represented_iso, phone, website, geom)
VALUES (:id, :name_en, :name_ja, :iso, :phone, :website,
        ST_SetSRID(ST_MakePoint(:lng, :lat),4326))
ON CONFLICT (id) DO UPDATE
SET name_en = EXCLUDED.name_en,
    name_ja = EXCLUDED.name_ja,
    represented_iso = EXCLUDED.represented_iso,
    phone = EXCLUDED.phone,
    website = EXCLUDED.website,
    geom = EXCLUDED.geom;
""")

async def import_embassies():
    async with Session() as s:
        with CSV_PATH.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                await s.execute(SQL, {
                    "id": row["id"],
                    "name_en": row["name_en"],
                    "name_ja": row.get("name_ja"),
                    "iso": row["represented_iso"].upper(),
                    "phone": row.get("phone"),
                    "website": row.get("website"),
                    "lat": float(row["lat"]),
                    "lng": float(row["lng"]),
                })
        await s.commit()