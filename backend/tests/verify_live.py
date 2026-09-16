import urllib.request
import json

def test_live():
    print("=== LIVE INTEGRATION & ENDPOINTS VERIFICATION ===")
    
    # 1. Health check
    try:
        r1 = urllib.request.urlopen("http://127.0.0.1:8000/health")
        h_data = json.loads(r1.read())
        print(f"✅ 1. Backend /health: HTTP {r1.status} | {h_data}")
    except Exception as e:
        print(f"❌ 1. Backend /health failed: {e}")

    # 2. Vehicles presets
    try:
        r2 = urllib.request.urlopen("http://127.0.0.1:8000/api/vehicles/presets")
        v_data = json.loads(r2.read())
        print(f"✅ 2. Backend /api/vehicles/presets: HTTP {r2.status} | {len(v_data)} vehicle models loaded")
    except Exception as e:
        print(f"❌ 2. Vehicles failed: {e}")

    # 3. Charging stations
    try:
        r3 = urllib.request.urlopen("http://127.0.0.1:8000/api/stations?limit=150")
        s_data = json.loads(r3.read())
        print(f"✅ 3. Backend /api/stations: HTTP {r3.status} | {len(s_data)} stations available")
    except Exception as e:
        print(f"❌ 3. Stations failed: {e}")

    # 4. Route calculation (Vellore -> Chennai)
    try:
        payload = json.dumps({
            "start_location": "Vellore, Tamil Nadu, India",
            "start_lat": 12.9165,
            "start_lng": 79.1325,
            "destination": "Chennai, Tamil Nadu, India",
            "dest_lat": 13.0827,
            "dest_lng": 80.2707,
            "current_battery_pct": 70,
            "battery_capacity_kwh": 40.5,
            "vehicle_efficiency_wh_per_km": 138,
            "vehicle_model": "Tata Nexon EV Long Range",
            "optimization_mode": "fastest"
        }).encode()
        req = urllib.request.Request("http://127.0.0.1:8000/api/route", data=payload, headers={"Content-Type": "application/json"})
        r4 = urllib.request.urlopen(req)
        route_data = json.loads(r4.read())
        summary = route_data.get("summary", {})
        print(f"✅ 4. Backend /api/route (Vellore -> Chennai): HTTP {r4.status} | Distance: {summary.get('total_distance_km')} km | Stops: {summary.get('num_stops')} | Feasible: {summary.get('is_feasible')}")
    except Exception as e:
        print(f"❌ 4. Route calculation failed: {e}")

    # 5. Frontend index check
    try:
        r5 = urllib.request.urlopen("http://localhost:3000")
        html = r5.read().decode("utf-8")
        print(f"✅ 5. Frontend http://localhost:3000: HTTP {r5.status} | {len(html)} bytes HTML received")
        print(f"   - App title present: {'VoltRoute' in html}")
        print(f"   - Next.js hydration chunks present: {'_next' in html}")
    except Exception as e:
        print(f"❌ 5. Frontend connection failed: {e}")

if __name__ == "__main__":
    test_live()
