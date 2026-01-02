#!/usr/bin/env bash
set -euo pipefail
DB=${1:-safetravel}

# このスクリプトファイルの場所を基準にパス構成
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_DIR="$SCRIPT_DIR/../schema"
SEED_DIR="$SCRIPT_DIR/../seed"

echo "== Using:"
echo "  DB=$DB"
echo "  SCHEMA_DIR=$SCHEMA_DIR"
echo "  SEED_DIR=$SEED_DIR"

# 存在チェック
[ -d "$SCHEMA_DIR" ] || { echo "Schema dir not found: $SCHEMA_DIR"; exit 1; }
[ -d "$SEED_DIR" ]   || { echo "Seed dir not found: $SEED_DIR"; }

echo "== Apply schema to $DB"
# まず extensions（あれば）
if [ -f "$SCHEMA_DIR/00_extensions.sql" ]; then
  psql -v ON_ERROR_STOP=1 -d "$DB" -f "$SCHEMA_DIR/00_extensions.sql"
fi

# 他のスキーマを順に
for f in "$SCHEMA_DIR"/*.sql; do
  [[ "$(basename "$f")" == "00_extensions.sql" ]] && continue
  echo " >> $f"
  psql -v ON_ERROR_STOP=1 -d "$DB" -f "$f"
done

echo "== Seed data"
if [ -d "$SEED_DIR" ]; then
  for f in "$SEED_DIR"/*.sql; do
    [ -e "$f" ] || continue
    echo " >> $f"
    psql -v ON_ERROR_STOP=1 -d "$DB" -f "$f"
  done
fi
echo "Done."