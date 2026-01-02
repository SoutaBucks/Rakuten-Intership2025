BEGIN;

CREATE SCHEMA IF NOT EXISTS embassy;

CREATE TABLE IF NOT EXISTS embassy.embassies (
  id BIGSERIAL PRIMARY KEY,
  represented_iso CHAR(2) NOT NULL,   -- 国籍（ISO2）
  type TEXT,                          -- embassy / consulate
  name_en TEXT, name_ja TEXT,
  city TEXT,
  address_en TEXT, address_ja TEXT,
  phone TEXT, website TEXT,
  geom geometry(Point,4326) NOT NULL
);

CREATE INDEX IF NOT EXISTS embassies_gix     ON embassy.embassies USING GIST (geom);
CREATE INDEX IF NOT EXISTS embassies_iso_idx ON embassy.embassies (represented_iso);

-- 公開ビュー
CREATE OR REPLACE VIEW public.embassies AS SELECT * FROM embassy.embassies;

COMMIT;