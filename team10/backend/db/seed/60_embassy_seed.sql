BEGIN;
TRUNCATE embassy.embassies RESTART IDENTITY;

INSERT INTO embassy.embassies
(represented_iso,type,name_en,name_ja,city,address_en,address_ja,phone,website,geom)
VALUES
('US','embassy','Embassy of the United States of America','在日米国大使館','Tokyo',
 '1-10-5 Akasaka, Minato-ku','東京都港区赤坂1-10-5','+81-3-3224-5000','https://jp.usembassy.gov',
 ST_SetSRID(ST_MakePoint(139.7429,35.6704),4326));
COMMIT;