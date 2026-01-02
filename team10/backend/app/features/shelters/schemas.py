from pydantic import BaseModel, Field
from typing import Optional, List


class ShelterCreate(BaseModel):
  id: str = Field(..., example='E1322800002111')
  name: str = Field(..., example="東京駅避難所")
  address: str = Field(..., example="東京港区")
  latitude: float = Field(..., ge=-90, le=90, example=35.6349)
  longitude: float = Field(..., ge=-180, le=180, example=139.6836)

class ShelterResponse(BaseModel):
  id: str
  name: str
  address: str
  latitude: float
  longitude: float

  class Config:
    from_attributes = True

class ShelterSearchParams(BaseModel):
  latitude: float = Field(..., ge=-90, le=90)
  longitude: float = Field(..., ge=-180, le=180)
  radius_km: Optional[float] = Field(default=5.0, gt=0, example=10.0)

class ShelterListResponse(BaseModel):
  shelters: List[ShelterResponse]
  total_count: int

class ShelterWithDistanceResponse(BaseModel):
  id: str
  name: str
  address: str
  latitude: float
  longitude: float
  distance_km: float

  class Config:
    from_attributes = True

class ShelterWithDistanceListResponse(BaseModel):
   shelters: List[ShelterWithDistanceResponse]
   total_count: int