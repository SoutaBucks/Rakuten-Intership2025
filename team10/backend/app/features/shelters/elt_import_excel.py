from typing import Any, Dict

import pandas as pd
import psycopg2
import logging


def import_excel_to_db(csv_path: str, db_config: Dict[str, Any]) -> None:
  try:
    df = pd.read_csv(csv_path, encoding='utf-8')

    # Select required columns and rename
    df = df[['共通ID', '施設・場所名', '住所', '緯度', '経度']]
    df.columns = ['id', 'name', 'address', 'latitude', 'longitude']

    # DB connect
    conn = psycopg2.connect(
      host=db_config['host'],
      port=db_config['port'],
      user=db_config['user'],
      password=db_config['password'],
      dbname=db_config['dbname']
    )
    cursor = conn.cursor()

    # Before add data, we need to delete existing data
    cursor.execute("DELETE FROM shelters")
    logging.info("Delete existing data")

    # insert query
    insert_query = """
                   INSERT INTO shelters (id, name, address, latitude, longitude)
                   VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET
                       name = EXCLUDED.name,
                       address = EXCLUDED.address,
                       latitude = EXCLUDED.latitude,
                       longitude = EXCLUDED.longitude
                   """

    # add Data in DB
    for index, row in df.iterrows():
      try:
        cursor.execute(insert_query, (
          row['id'],
          row['name'],
          row['address'],
          row['latitude'],
          row['longitude']
        ))
      except Exception as e:
        logging.error(f"We got an error when Inserting row {index + 1}: {e}")
        raise

    conn.commit()
    cursor.close()
    conn.close()

    logging.info("Csv to DB is Complete!!")
  except Exception as e:
    logging.error(f"We got an error when csv import: {e}")
    raise
