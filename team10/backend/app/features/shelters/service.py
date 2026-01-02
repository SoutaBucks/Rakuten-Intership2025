import logging
from typing import Optional, List

from app.features.shelters.repo import ShelterRepository
from app.features.shelters.schemas import ShelterCreate, ShelterResponse, ShelterSearchParams

from app.features.shelters.schemas import ShelterWithDistanceResponse


class ShelterService:
  def __init__(self, shelter_repo: ShelterRepository):
    self.shelter_repo = shelter_repo

  # make new Shelter
  def create_shelter(self, shelter_data: ShelterCreate) -> ShelterResponse:
    try:
      return self.shelter_repo.create_shelter(shelter_data)
    except Exception as e:
      logging.error(f"We get an error in create_shelter Service: {e}")
      raise

  # get all shelters
  def get_all_shelters(self) -> List[ShelterResponse]:
    try:
      return self.shelter_repo.get_all_shelters()
    except Exception as e:
      logging.error(f"We get an error in get_all_shelters Service: {e}")
      raise

  # get shelter by id
  def get_shelter_by_id(self, shelter_id: str) -> Optional[ShelterResponse]:
    try:
      return self.shelter_repo.get_shelter_by_id(shelter_id)
    except Exception as e:
      logging.error(f"We get an error in get_shelter_by_id Service: {e}")
      raise

  # update shelter
  def update_shelter(self, shelter_id: str, shelter_data: ShelterCreate) -> Optional[ShelterResponse]:
    try:
      return self.shelter_repo.update_shelter(shelter_id, shelter_data)
    except Exception as e:
      logging.error(f"We get an error in update_shelter Service: {e}")
      raise

  # delete Shelter
  def delete_shelter(self, shelter_id: str) -> bool:
    try:
      return self.shelter_repo.delete_shelter(shelter_id)
    except Exception as e:
      logging.error(f"We get an error in delete_shelter Service: {e}")
      raise

  # get shelters by location
  def search_shelter_by_location(self, params: ShelterSearchParams) -> List[ShelterWithDistanceResponse]:
    try:
      return self.shelter_repo.find_shelters_by_location(
        lat=params.latitude,
        lng=params.longitude,
        radius_km=params.radius_km
      )
    except Exception as e:
      logging.error(f"We get an error in search_shelter_by_location Service: {e}")
      raise

  def search_shelter_by_name(self, name: str) -> List[ShelterResponse]:
    try:
      return self.shelter_repo.find_shelters_by_name(name)
    except Exception as e:
      logging.error(f"We get an error in search_shelter_by_name Service: {e}")
      raise

  def get_map_data(self, center_lat: float = 35.6762, center_lng: float = 139.6503, zoom_level: int = 10) -> dict:
    try:
      all_shelters = self.shelter_repo.get_all_shelters()

      shelters_data = []
      for shelter in all_shelters:
        shelters_data.append({
          "id": shelter.id,
          "name": shelter.name,
          "latitude": shelter.latitude,
          "longitude": shelter.longitude,
          "address": shelter.address,
        })

      return {
        "shelters": shelters_data,
        "center_lat": center_lat,
        "center_lng": center_lng,
        "zoom_level": zoom_level,
        "total_count": len(shelters_data)
      }
    except Exception as e:
      logging.error(f"We get an error in get_map_data Service: {e}")
      raise
