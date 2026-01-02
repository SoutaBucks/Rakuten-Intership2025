-- まずPostGISだけ有効化（距離検索やPoint格納に使う）
CREATE EXTENSION IF NOT EXISTS postgis;