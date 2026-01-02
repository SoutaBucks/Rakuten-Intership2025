from app.db import get_conn

SQL_NEAR = """
WITH h AS (SELECT lat, lng, nationality_iso FROM public.hotels WHERE id = $1),
     q AS (SELECT ST_SetSRID(ST_MakePoint(h.lng,h.lat),4326)::geography g, h.nationality_iso iso FROM h)
SELECT e.name_en, e.name_ja, e.represented_iso, e.phone, e.website,
       ST_Y(e.geom) AS lat, ST_X(e.geom) AS lng,
       ST_DistanceSphere(e.geom, (SELECT g::geometry FROM q)) AS dist_m
FROM public.embassies e
WHERE e.represented_iso = (SELECT iso FROM q)
ORDER BY dist_m
LIMIT $2;
"""

async def find_nearest_embassy(hotel_id: str, limit: int = 3):
    async with get_conn() as conn:
        rows = await conn.fetch(SQL_NEAR, hotel_id, limit)
    return [dict(r) for r in rows]