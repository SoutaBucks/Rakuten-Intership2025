from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query

from app.config import settings
import app.features.shelters.repo
from app.features.shelters.repo import ShelterRepository
from app.features.shelters.schemas import ShelterListResponse, ShelterResponse, ShelterCreate, ShelterSearchParams
from app.features.shelters.service import ShelterService

import logging

from app.features.shelters.schemas import ShelterWithDistanceListResponse

router = APIRouter()


# DI
def get_shelter_repo():
  db_config = {
    'host': settings.DB_HOST,
    'port': settings.DB_PORT,
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'dbname': settings.DB_NAME
  }
  return ShelterRepository(db_config)


def get_shelter_service():
  repository = get_shelter_repo()
  return ShelterService(repository)


@router.get("/", response_model=ShelterListResponse, summary="Get all shelters")
async def get_all_shelters(
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Get_all_shelters")
  try:
    shelters = service.get_all_shelters()
    return {
      "shelters": shelters,
      "total_count": len(shelters)
    }
  except Exception as e:
    logging.error(f"We got an API error when getting all shelters: {e}")
    raise HTTPException(status_code=500, detail="Error retrieving shelter")


@router.post("/", response_model=ShelterResponse, summary="Create new shelter")
async def create_shelter(
  shelter_data: ShelterCreate,
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Create_shelter")
  try:
    shelter = service.create_shelter(shelter_data)
    return shelter
  except Exception as e:
    logging.error(f"We got an API error when creating new shelter: {e}")
    raise HTTPException(status_code=500, detail="Error creating new shelter")


@router.get("/idsearch", response_model=ShelterResponse, summary="Get shelter by ID")
async def get_shelter_by_id(
  shelter_id: str = Query(..., description="Shelter ID"),
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Get_shelter_by_id")
  try:
    shelter = service.get_shelter_by_id(shelter_id)
    if not shelter:
      raise HTTPException(status_code=404, detail="Shelter not found")
    return shelter
  except HTTPException:
    raise
  except Exception as e:
    logging.error(f"We got an API error when getting shelter: {e}")
    raise HTTPException(status_code=500, detail="Error retrieving shelter")


@router.get("/search", response_model=ShelterListResponse, summary="Search shelters by name")
async def search_shelters_by_name(
  name: str = Query(..., description="Search shelter name"),
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Get_shelter_by_name")
  try:
    shelters = service.search_shelter_by_name(name)
    return {
      "shelters": shelters,
      "total_count": len(shelters)
    }
  except Exception as e:
    logging.error(f"We got an API error when searching shelters by name: {e}")
    raise HTTPException(status_code=500, detail="Error searching shelters by name")


@router.get("/search/location", response_model=ShelterWithDistanceListResponse, summary="Search shelters by location")
async def search_shelters_by_location(
  latitude: float = Query(..., description="Search center latitude"),
  longitude: float = Query(..., description="Search center longitude"),
  radius_km: float = Query(5.0, description="Search center radius"),
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Get_shelter_by_location")
  try:
    params = ShelterSearchParams(
      latitude=latitude,
      longitude=longitude,
      radius_km=radius_km
    )
    shelters = service.search_shelter_by_location(params)
    return {
      "shelters": shelters,
      "total_count": len(shelters)
    }
  except Exception as e:
    logging.error(f"We got an API error when searching shelters by location: {e}")
    raise HTTPException(status_code=500, detail="Error searching shelters by location")


@router.get("/map/data", summary="Get map data")
async def get_map_data(
  center_lat: float = Query(35.6762, description="Map center latitude"),
  center_lng: float = Query(139.6503, description="Map center longitude"),
  zoom_level: int = Query(10, ge=1, le=20, description="Map zoom level"),
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Get_map_data")
  try:
    return service.get_map_data(center_lat, center_lng, zoom_level)
  except Exception as e:
    logging.error(f"Error getting map data: {e}")
    raise HTTPException(status_code=500, detail="Error retrieving map data")


@router.put("/{shelter_id}", response_model=ShelterResponse, summary="Update shelter")
async def update_shelter(
  shelter_id: str, shelter_data: ShelterCreate,
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Update_shelter")
  try:
    shelter = service.update_shelter(shelter_id, shelter_data)
    if not shelter:
      raise HTTPException(status_code=404, detail="Shelter not found")
    return shelter
  except HTTPException as e:
    raise
  except Exception as e:
    logging.error(f"We got an API error when updating shelter: {e}")
    raise HTTPException(status_code=500, detail="Error updating shelter")


@router.delete("/{shelter_id}", summary="Delete shelter")
async def delete_shelter(
  shelter_id: str,
  service: ShelterService = Depends(get_shelter_service)
):
  logging.info("You called Delete_shelter")
  try:
    success = service.delete_shelter(shelter_id)
    if not success:
      raise HTTPException(status_code=404, detail="Shelter not found")
    return {"message": "Shelter deleted successfully"}
  except HTTPException:
    raise
  except Exception as e:
    logging.error(f"We got an API error when deleting shelter: {e}")
    raise HTTPException(status_code=500, detail="Error deleting shelter")
