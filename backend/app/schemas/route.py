from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field

class LocationInput(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class VehiclePreset(BaseModel):
    id: str
    name: str
    make: str
    model: str
    year: int
    battery_capacity_kwh: float
    efficiency_wh_per_km: float
    max_charge_rate_kw: float
    supported_connectors: List[str]
    description: Optional[str] = None

class RouteRequest(BaseModel):
    # Support string input ("San Francisco, CA") or structured LocationInput
    start_location: Union[str, LocationInput] = Field(..., description="Start city name, address, or coordinate object")
    destination: Union[str, LocationInput] = Field(..., description="Destination city name, address, or coordinate object")
    
    current_battery_pct: float = Field(80.0, ge=5.0, le=100.0, description="Current battery percentage (5 - 100%)")
    battery_capacity_kwh: float = Field(75.0, ge=15.0, le=250.0, description="Total usable battery capacity in kWh")
    vehicle_efficiency_wh_per_km: float = Field(160.0, ge=80.0, le=450.0, description="Vehicle consumption in Wh/km")
    
    vehicle_model: Optional[str] = Field(None, description="Optional EV model name for preset charging curve calculations")
    min_stop_soc_pct: float = Field(10.0, ge=2.0, le=30.0, description="Minimum battery safety buffer when arriving at a charger (%)")
    target_dest_soc_pct: float = Field(15.0, ge=5.0, le=50.0, description="Target minimum battery level at final destination (%)")
    max_charge_soc_pct: float = Field(80.0, ge=50.0, le=100.0, description="Target charge level at stops (80% recommended for fastest trip)")
    preferred_connectors: Optional[List[str]] = Field(default=None, description="e.g. ['NACS', 'CCS', 'Type 2']")
    min_charger_power_kw: Optional[float] = Field(default=50.0, description="Minimum power rating for candidate chargers")

class StationResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "US"
    operator: str
    power_kw: float
    total_ports: int
    available_ports: int
    connector_types: List[str]
    price_per_kwh: float
    amenities: List[str]
    is_operational: bool
    detour_km: Optional[float] = None

class ChargingStop(BaseModel):
    stop_index: int
    station: StationResponse
    arrival_soc_pct: float
    departure_soc_pct: float
    energy_added_kwh: float
    charge_duration_min: float
    estimated_cost_usd: float
    distance_from_start_km: float
    distance_from_prev_stop_km: float

class RouteLeg(BaseModel):
    leg_index: int
    from_name: str
    to_name: str
    distance_km: float
    duration_min: float
    energy_used_kwh: float
    start_soc_pct: float
    end_soc_pct: float
    polyline: Optional[List[List[float]]] = None # List of [lat, lon]

class BatteryProfilePoint(BaseModel):
    distance_km: float
    soc_pct: float
    location_name: str
    event: str # "start", "driving", "arrival_at_charger", "charged_at_charger", "destination"

class TripSummary(BaseModel):
    total_distance_km: float
    total_distance_miles: float
    total_drive_time_min: float
    total_charge_time_min: float
    total_trip_time_min: float
    initial_battery_pct: float
    final_battery_pct: float
    total_energy_consumed_kwh: float
    total_energy_charged_kwh: float
    total_charging_cost_usd: float
    co2_saved_kg: float
    num_stops: int
    is_feasible: bool
    status_message: str

class ResolvedLocation(BaseModel):
    name: str
    latitude: float
    longitude: float
    formatted_address: Optional[str] = None

class RouteResponse(BaseModel):
    summary: TripSummary
    origin: ResolvedLocation
    destination: ResolvedLocation
    legs: List[RouteLeg]
    stops: List[ChargingStop]
    battery_profile: List[BatteryProfilePoint]
    route_geometry: List[List[float]] # Full path polyline [[lat, lon], ...]
    candidate_stations: List[StationResponse]
