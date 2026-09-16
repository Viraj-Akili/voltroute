import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.station import ChargingStation
from app.schemas.route import (
    RouteRequest, RouteResponse, StationResponse, VehiclePreset
)
from app.services.geocoding import geocode_location
from app.services.optimizer import optimize_ev_route
from app.services.routing import haversine_distance_km
from app.data.seed_stations import VEHICLE_PRESETS
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["EV Route Planner"])

@router.post("/route", response_model=RouteResponse, summary="Calculate Optimal EV Route & Charging Plan")
@router.post("/api/route", response_model=RouteResponse, summary="Calculate Optimal EV Route & Charging Plan (API prefix)")
async def plan_ev_route(request: RouteRequest, db: Session = Depends(get_db)):
    """
    Plan an intelligent EV route between two locations.
    Simulates real-world EV battery depletion, analyzes charging speeds,
    and recommends optimal charging stops along the travel corridor to minimize total travel time.
    """
    try:
        # Geocode start and destination
        origin = await geocode_location(request.start_location)
        destination = await geocode_location(request.destination)

        # Ensure start and destination are distinct
        dist_direct = haversine_distance_km(
            origin.latitude, origin.longitude,
            destination.latitude, destination.longitude
        )
        if dist_direct < 0.5:
            raise HTTPException(
                status_code=400,
                detail="Start location and Destination are too close to each other. Please provide different locations."
            )

        # Run optimization
        response = await optimize_ev_route(
            request=request,
            origin=origin,
            destination=destination,
            db=db,
            osrm_base_url=settings.OSRM_BASE_URL
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error calculating EV route: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while calculating the route: {str(e)}"
        )

@router.get("/api/vehicles/presets", response_model=List[VehiclePreset], summary="Get Popular EV Vehicle Presets")
def get_vehicle_presets():
    """
    Returns popular electric vehicle presets with battery capacity, efficiency, and max charging speeds.
    """
    return VEHICLE_PRESETS

@router.get("/api/stations", response_model=List[StationResponse], summary="List & Search Charging Stations")
def get_stations(
    lat: Optional[float] = Query(None, description="Center latitude for spatial radius search"),
    lon: Optional[float] = Query(None, description="Center longitude for spatial radius search"),
    radius_km: Optional[float] = Query(100.0, ge=1.0, le=2000.0, description="Radius in km"),
    operator: Optional[str] = Query(None, description="Filter by operator/network name"),
    min_power: Optional[float] = Query(None, description="Filter by minimum power rating in kW"),
    limit: int = Query(250, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Query charging stations from the database with optional spatial radius filtering.
    """
    query = db.query(ChargingStation).filter(ChargingStation.is_operational == True)

    if operator:
        query = query.filter(ChargingStation.operator.ilike(f"%{operator}%"))
    if min_power:
        query = query.filter(ChargingStation.power_kw >= min_power)

    stations = query.all()

    # Spatial radius filtering if lat/lon provided
    if lat is not None and lon is not None:
        filtered = []
        for s in stations:
            d = haversine_distance_km(lat, lon, s.latitude, s.longitude)
            if d <= radius_km:
                s_dict = s.to_dict()
                s_dict["detour_km"] = round(d, 1)
                filtered.append(s_dict)
        filtered.sort(key=lambda x: x.get("detour_km", 0))
        return filtered[:limit]

    return [s.to_dict() for s in stations[:limit]]
