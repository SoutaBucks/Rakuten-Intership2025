import logging
from typing import List, Optional

import psycopg2
import psycopg2.extras
from math import *
from app.features.shelters.schemas import ShelterCreate, ShelterResponse

from app.features.shelters.schemas import ShelterWithDistanceResponse


class ShelterRepository:
  def __init__(self, db_config: dict):
    self.db_config = db_config

  def _get_connection(self):
    return psycopg2.connect(
      host=self.db_config['host'],
      port=self.db_config['port'],
      user=self.db_config['user'],
      password=self.db_config['password'],
      dbname=self.db_config['dbname']
    )

  def create_shelter(self, shelter: ShelterCreate) -> ShelterResponse:
    conn = self._get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
      query = """
              INSERT INTO shelters (id, name, address, latitude, longitude)
              VALUES (%s, %s, %s, %s, %s) RETURNING id, name, address, latitude, longitude \
              """

      cursor.execute(query, (
        shelter.id, shelter.name, shelter.address, shelter.latitude, shelter.longitude
      ))

      result = cursor.fetchone()
      conn.commit()

      return ShelterResponse(**dict(result))
    except Exception as e:
      conn.rollback()
      logging.error(f"We got an error when create shelter: {e}")
      raise
    finally:
      cursor.close()
      conn.close()

  def get_all_shelters(self) -> List[ShelterResponse]:
    conn = self._get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
      query = """
              SELECT id, name, address, latitude, longitude
              FROM shelters
              ORDER BY name \
              """
      cursor.execute(query)
      results = cursor.fetchall()

      return [ShelterResponse(**dict(row)) for row in results]

    except Exception as e:
      logging.error(f"We got an error when get all shelters: {e}")
      raise
    finally:
      cursor.close()
      conn.close()

  def get_shelter_by_id(self, shelter_id: str) -> Optional[ShelterResponse]:
    conn = self._get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
      query = """
        SELECT id, name, address, latitude, longitude
        FROM shelters 
            WHERE id = %s
      """
      cursor.execute(query, (shelter_id,))
      result = cursor.fetchone()

      if result:
        return ShelterResponse(**dict(result))
      return None

    except Exception as e:
      logging.error(f"We got an error when get shelter by id: {e}")
      raise
    finally:
      cursor.close()
      conn.close()


  def update_shelter(self, shelter_id: str, shelter: ShelterCreate) -> Optional[ShelterResponse]:
    conn = self._get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
      query = """
              UPDATE shelters
              SET name      = %s,
                  address   = %s,
                  latitude  = %s,
                  longitude = %s
              WHERE id = %s RETURNING id, name, address, latitude, longitude 
              """
      cursor.execute(query, (
        shelter.name, shelter.address, shelter.latitude, shelter.longitude, shelter_id
      ))

      result = cursor.fetchone()
      conn.commit()

      if result:
        return ShelterResponse(**dict(result))
      return None
    except Exception as e:
      conn.rollback()
      logging.error(f"We got an error when update: {e}")
      raise
    finally:
      cursor.close()
      conn.close()

  def delete_shelter(self, shelter_id: str) -> bool:
    conn = self._get_connection()
    cursor = conn.cursor()

    try:
      query = """DELETE
                 FROM shelters
                 WHERE id = %s"""
      cursor.execute(query, (shelter_id,))

      deleted_count = cursor.rowcount
      conn.commit()

      return deleted_count > 0
    except Exception as e:
      conn.rollback()
      logging.error(f"We got an error when delete: {e}")
      raise
    finally:
      cursor.close()
      conn.close()

  def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    return (6371 * acos(cos(radians(lat1)) * cos(radians(lat2)) *
                        cos(radians(lng1) - radians(lng2)) +
                        sin(radians(lat1)) * sin(radians(lat2))))

  def find_shelters_by_location(self, lat: float, lng: float, radius_km: float = 5.0) -> List[ShelterWithDistanceResponse]:
    conn = self._get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
      # 모든 대피소를 가져옴
      query = """
              SELECT id, name, address, latitude, longitude
              FROM shelters 
              """
      cursor.execute(query)
      results = cursor.fetchall()

      # 거리 계산 및 필터링
      shelters_with_distance = []
      for row in results:
        distance = self._calculate_distance(lat, lng, row['latitude'], row['longitude'])
        if distance <= radius_km:
          shelter_data = dict(row)
          shelter_data['distance_km'] = round(distance, 2)
          shelters_with_distance.append(shelter_data)
          # shelters_with_distance.append({
          #   'shelter': ShelterResponse(**dict(row)),
          #   'distance': distance
          # })

      # 거리순으로 정렬
      shelters_with_distance.sort(key=lambda x: x['distance_km'])

      #return [item['shelter'] for item in shelters_with_distance]
      return [ShelterWithDistanceResponse(**row) for row in shelters_with_distance]


    except Exception as e:
      logging.error(f"We got an error when find  by location: {e}")
      raise
    finally:
      cursor.close()
      conn.close()


  def find_shelters_by_name(self, name: str) -> List[ShelterResponse]:
    conn = self._get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
      query = """
              SELECT id, name, address, latitude, longitude
              FROM shelters
              WHERE name ILIKE %s
              ORDER BY name 
              """
      search_pattern = f'%{name}%'
      cursor.execute(query, (search_pattern,))
      results = cursor.fetchall()

      shelters = [ShelterResponse(**dict(row)) for row in results]
      return shelters

    except Exception as e:
      logging.error(f"We got an error when find by name: {e}")
      raise
    finally:
      cursor.close()
      conn.close()
