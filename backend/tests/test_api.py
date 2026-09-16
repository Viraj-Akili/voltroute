import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.data.seed_stations import seed_database_if_empty

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database_if_empty(db)
    db.close()
    yield

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert data["charging_stations_loaded"] > 50

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data

def test_vehicle_presets(client):
    response = client.get("/api/vehicles/presets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    first = data[0]
    assert "battery_capacity_kwh" in first
    assert "efficiency_wh_per_km" in first
    assert "max_charge_rate_kw" in first

def test_get_stations(client):
    response = client.get("/api/stations?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 10
    assert len(data) > 0
    station = data[0]
    assert "name" in station
    assert "power_kw" in station
    assert "latitude" in station
    assert "longitude" in station

def test_short_route_no_stops_needed(client):
    # San Francisco to San Jose (~75km) with 90% battery on 75kWh Tesla Model 3
    payload = {
        "start_location": "San Francisco, CA",
        "destination": "San Jose, CA",
        "current_battery_pct": 90.0,
        "battery_capacity_kwh": 75.0,
        "vehicle_efficiency_wh_per_km": 150.0,
        "min_stop_soc_pct": 10.0,
        "target_dest_soc_pct": 15.0
    }
    response = client.post("/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["is_feasible"] is True
    assert data["summary"]["num_stops"] == 0
    assert data["summary"]["total_distance_km"] > 40.0
    assert len(data["legs"]) == 1
    assert len(data["battery_profile"]) > 0

def test_long_route_charging_stops_optimized(client):
    # Los Angeles to San Francisco (~610km) with 70% initial battery on Tesla Model 3
    payload = {
        "start_location": "Los Angeles, CA",
        "destination": "San Francisco, CA",
        "current_battery_pct": 70.0,
        "battery_capacity_kwh": 75.0,
        "vehicle_efficiency_wh_per_km": 160.0,
        "min_stop_soc_pct": 10.0,
        "target_dest_soc_pct": 15.0,
        "max_charge_soc_pct": 80.0
    }
    response = client.post("/api/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    summary = data["summary"]
    assert summary["is_feasible"] is True
    assert summary["num_stops"] >= 1
    assert summary["total_charge_time_min"] > 0
    assert summary["total_distance_km"] > 400.0
    assert len(data["stops"]) >= 1
    assert len(data["legs"]) >= 2
    assert len(data["battery_profile"]) >= 5

    # Check that charging stop details are filled properly
    first_stop = data["stops"][0]
    assert first_stop["arrival_soc_pct"] >= 5.0
    assert first_stop["departure_soc_pct"] > first_stop["arrival_soc_pct"]
    assert first_stop["charge_duration_min"] > 0
    assert first_stop["station"]["power_kw"] >= 50.0

def test_route_with_coordinates(client):
    payload = {
        "start_location": {"name": "Seattle Space Needle", "lat": 47.6205, "lon": -122.3493},
        "destination": {"name": "Portland Pioneer Square", "lat": 45.5189, "lon": -122.6796},
        "current_battery_pct": 85.0,
        "battery_capacity_kwh": 77.4,
        "vehicle_efficiency_wh_per_km": 180.0
    }
    response = client.post("/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["is_feasible"] is True
    assert data["origin"]["name"] == "Seattle Space Needle"
    assert data["destination"]["name"] == "Portland Pioneer Square"
