from fastapi import FastAPI
from app.features.area.router import router as area_router
from app.features.mailer.router import router as mailer_router
from app.features.shelters.router import router as shelters_router
from app.features.hazards.router import router as hazards_router
from app.features.embassy.router import router as embassy_router

def include_feature_routers(app: FastAPI):
    app.include_router(area_router,     prefix="/api/area",     tags=["area"])
    app.include_router(mailer_router,   prefix="/api/mailer",   tags=["mailer"])
    app.include_router(shelters_router, prefix="/api/shelters", tags=["shelters"])
    app.include_router(hazards_router,  prefix="/api/hazards",  tags=["hazards"])
    app.include_router(embassy_router,  prefix="/api/embassy",  tags=["embassy"])



from fastapi import APIRouter, FastAPI
from .features.hazards.router import router as hazards_router

def include_feature_routers(app: FastAPI):
    api = APIRouter(prefix="/api")
    api.include_router(hazards_router, prefix="/hazards", tags=["hazards"])
    app.include_router(api)
