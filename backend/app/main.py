import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db, SessionLocal
from app.models.station import ChargingStation
from app.data.seed_stations import seed_database_if_empty
from app.routes.route_api import router as route_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("voltroute")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and auto-seed database
    logger.info("Initializing VoltRoute database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        count = seed_database_if_empty(db)
        logger.info(f"Database ready with {count} verified EV charging stations.")
    finally:
        db.close()
    
    yield
    logger.info("VoltRoute API shutting down.")

app = FastAPI(
    title="VoltRoute — Intelligent EV Route Planner API",
    description="Production-quality REST API for EV route planning, battery consumption modeling, and fast-charging stop optimization.",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(route_router)

@app.get("/health", summary="Service Health Check")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint verifying database connectivity and station count.
    """
    station_count = db.query(ChargingStation).count()
    return {
        "status": "ok",
        "app": "VoltRoute — Intelligent EV Route Planner",
        "version": settings.VERSION,
        "database": "connected",
        "charging_stations_loaded": station_count
    }

@app.get("/", summary="Root Overview")
def root_overview():
    return {
        "name": "VoltRoute — Intelligent EV Route Planner API",
        "version": settings.VERSION,
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "plan_route": "POST /route or POST /api/route",
            "vehicle_presets": "GET /api/vehicles/presets",
            "stations": "GET /api/stations"
        }
    }

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
