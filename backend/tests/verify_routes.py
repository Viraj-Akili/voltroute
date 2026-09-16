import httpx

routes = [
    {
        "title": "Test A: Vellore to Chennai (Tata Nexon EV, 70% SOC)",
        "payload": {
            "start_location": "Vellore, Tamil Nadu",
            "destination": "Chennai, Tamil Nadu",
            "current_battery_pct": 70.0,
            "battery_capacity_kwh": 40.5,
            "vehicle_efficiency_wh_per_km": 138.0,
            "vehicle_model": "Tata Nexon EV Long Range",
            "min_stop_soc_pct": 10.0,
            "target_dest_soc_pct": 15.0
        }
    },
    {
        "title": "Test B: Vellore to Bengaluru (Tata Nexon EV, 50% SOC)",
        "payload": {
            "start_location": "Vellore, Tamil Nadu",
            "destination": "Bengaluru, Karnataka",
            "current_battery_pct": 50.0,
            "battery_capacity_kwh": 40.5,
            "vehicle_efficiency_wh_per_km": 138.0,
            "vehicle_model": "Tata Nexon EV Long Range",
            "min_stop_soc_pct": 10.0,
            "target_dest_soc_pct": 15.0
        }
    },
    {
        "title": "Test C: Vellore to Tirupati (MG ZS EV, 80% SOC)",
        "payload": {
            "start_location": "Vellore, Tamil Nadu",
            "destination": "Tirupati, Andhra Pradesh",
            "current_battery_pct": 80.0,
            "battery_capacity_kwh": 50.3,
            "vehicle_efficiency_wh_per_km": 150.0,
            "vehicle_model": "MG ZS EV",
            "min_stop_soc_pct": 10.0,
            "target_dest_soc_pct": 15.0
        }
    }
]

client = httpx.Client(timeout=20.0)
for r in routes:
    resp = client.post("http://127.0.0.1:8000/api/route", json=r["payload"])
    assert resp.status_code == 200, f"Route failed: {resp.status_code} {resp.text}"
    data = resp.json()
    s = data["summary"]
    print(f"=== {r['title']} ===")
    print(f"  Distance: {s['total_distance_km']} km ({s['total_distance_miles']} mi)")
    print(f"  Stops Count: {s['num_stops']} | Feasible: {s['is_feasible']}")
    print(f"  Drive Time: {s['total_drive_time_min']}m | Charge Time: {s['total_charge_time_min']}m | Total: {s['total_trip_time_min']}m")
    print(f"  Energy Consumed: {s['total_energy_consumed_kwh']} kWh | Estimated Cost: Rs. {s['total_charging_cost_usd']:.2f}")
    print(f"  Arrival Battery: {s['final_battery_pct']}%")
    if data["stops"]:
        for st in data["stops"]:
            print(f"    - Stop #{st['stop_index']}: {st['station']['name']} ({st['station']['operator']} {st['station']['power_kw']}kW) -> Charge {st['charge_duration_min']}m ({st['arrival_soc_pct']}% to {st['departure_soc_pct']}%)")
    print()
