BEGIN;

CREATE SCHEMA IF NOT EXISTS area;

-- Area Class（必要になったとき用。今は空でもOK）
CREATE TABLE IF NOT EXISTS area.area_class (
  id BIGSERIAL PRIMARY KEY,
  large_code TEXT NOT NULL,  large_name TEXT NOT NULL,
  middle_code TEXT NOT NULL, middle_name TEXT NOT NULL,
  small_code TEXT NOT NULL,  small_name TEXT NOT NULL,
  detail_code TEXT,          detail_name TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS area_class_codes_uk
  ON area.area_class (large_code, middle_code, small_code, COALESCE(detail_code,''));

-- フロントが返すホテル住所・座標を保持
CREATE TABLE IF NOT EXISTS area.hotels (
  id TEXT PRIMARY KEY,           -- 予約/QRの hotel_id をそのまま鍵に
  name TEXT,
  address TEXT,
  lat DOUBLE PRECISION,
  lng DOUBLE PRECISION,
  geom geometry(Point,4326) GENERATED ALWAYS AS
       (CASE WHEN lat IS NOT NULL AND lng IS NOT NULL
             THEN ST_SetSRID(ST_MakePoint(lng,lat),4326) END) STORED,

  -- あるならフロントから受け取るAreaコード（NULL可）
  large_code TEXT,
  middle_code TEXT,
  small_code TEXT,
  detail_code TEXT,

  nationality_iso CHAR(2)        -- “予約時に入力された国籍ISO2”（例: US, KR）
);

CREATE INDEX IF NOT EXISTS hotels_geom_gix ON area.hotels USING GIST (geom);

-- 公開ビュー（API側は public を読めばOK）
CREATE OR REPLACE VIEW public.hotels AS SELECT * FROM area.hotels;
CREATE OR REPLACE VIEW public.area_class AS SELECT * FROM area.area_class;

COMMIT;