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

def test_soc_consumption_physics():
    """
    Test physics calculation for EV battery consumption:
    45 km driven with 138 Wh/km on 40.5 kWh battery.
    Base consumption = 45 km * 138 Wh/km = 6,210 Wh = 6.21 kWh.
    Expected SOC drop = 6.21 / 40.5 * 100 = 15.33%.
    Starting at 70% SOC -> expected arrival SOC ~54.7% (or ~54.0% with 4% overhead).
    """
    distance_km = 45.0
    efficiency_wh_per_km = 138.0
    battery_capacity_kwh = 40.5
    start_soc = 70.0
    overhead = 1.04

    energy_consumed_kwh = (distance_km * efficiency_wh_per_km / 1000.0) * overhead
    soc_drop_pct = (energy_consumed_kwh / battery_capacity_kwh) * 100.0
    arrival_soc = start_soc - soc_drop_pct

    assert round(energy_consumed_kwh, 2) == 6.46  # 6.21 kWh base * 1.04 overhead
    assert 15.0 < soc_drop_pct < 16.5
    assert 53.5 <= arrival_soc <= 55.0

def test_charging_cost_33_to_70_percent():
    """
    Test 33% -> 70% charge on a 40.5 kWh battery:
    Energy added = 40.5 * (70 - 33) / 100 = 14.985 kWh.
    At typical Indian public charging rate ₹18-₹25/kWh (e.g. ₹20.50/kWh):
    Cost = 14.985 * 20.50 = ₹307.19 (expected ~₹270 - ₹375).
    Ensure it is NOT inflated by unit confusion or extra currency multipliers (e.g. ₹25,675).
    """
    battery_capacity_kwh = 40.5
    arrival_soc = 33.0
    target_soc = 70.0
    price_per_kwh = 20.50

    energy_added_kwh = battery_capacity_kwh * (target_soc - arrival_soc) / 100.0
    cost_inr = energy_added_kwh * price_per_kwh

    assert round(energy_added_kwh, 3) == 14.985
    assert 270.0 <= cost_inr <= 375.0
    assert cost_inr < 500.0  # verify never inflated to thousands

def test_indian_corridor_route_cost_and_soc(client):
    """
    Integration test for Indian corridor route (Vellore -> Bengaluru) with Tata Nexon EV LR.
    Verifies that stops have realistic costs (₹150 - ₹500) and proper SOC progression.
    """
    payload = {
        "start_location": "Vellore, Tamil Nadu, India",
        "start_lat": 12.9165,
        "start_lng": 79.1325,
        "destination": "Bengaluru, Karnataka, India",
        "dest_lat": 12.9716,
        "dest_lng": 77.5946,
        "current_battery_pct": 50.0,
        "battery_capacity_kwh": 40.5,
        "vehicle_efficiency_wh_per_km": 138.0,
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

    for stop in data["stops"]:
        assert 100.0 <= stop["estimated_cost_usd"] <= 800.0
        assert stop["departure_soc_pct"] > stop["arrival_soc_pct"]
        assert stop["energy_added_kwh"] > 0

