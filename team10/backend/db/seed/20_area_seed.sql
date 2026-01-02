BEGIN;
INSERT INTO area.hotels (id,name,address,lat,lng,nationality_iso)
VALUES ('HTL_DEMO_001','Sample Hotel','Chiyoda-ku, Tokyo',35.6812,139.7671,'US')
ON CONFLICT (id) DO NOTHING;
COMMIT;