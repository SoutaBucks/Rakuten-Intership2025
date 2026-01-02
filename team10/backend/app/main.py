import logging

# 로깅 설정을 맨 위로 이동
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.features.embassy.router import router as embassy_router
from app.features.area.router import router as area_router
from app.features.mailer.router import router as mailer_router
from app.features.hazards.router import router as hazards_router
from app.features.shelters.router import router as shelter_router
from app.features.shelters.elt_import_excel import import_excel_to_db
from app.config import settings
from app.features.reservation.router import router as reservation_router

app = FastAPI(title="SafeTravel API")

# フロント（別ポート）から叩くなら適当にCORS許可
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], allow_credentials=True,
  allow_methods=["*"], allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
  try:
    db_config = {
      'host': settings.DB_HOST,
      'port': settings.DB_PORT,
      'user': settings.DB_USER,
      'password': settings.DB_PASSWORD,
      'dbname': settings.DB_NAME
    }

    csv_path = "data/shelter.csv"

    if os.path.exists(csv_path):
      logging.info("🚀 Starting shelter data import on server startup...")
      import_excel_to_db(csv_path, db_config)
      logging.info("✅ Shelter data import completed on startup!")
    else:
      logging.warning(f"⚠️ CSV file not found: {csv_path}")

  except Exception as e:
    logging.error(f"❌ Error importing shelter data on startup: {e}")


app.include_router(embassy_router)
app.include_router(area_router)
app.include_router(mailer_router)


app.include_router(hazards_router, prefix="/api/hazards", tags=["hazards"])
app.include_router(shelter_router, prefix="/api/shelters", tags=["shelters"])
app.include_router(reservation_router)


@app.get("/health")
async def health():
  return {"ok": True}
