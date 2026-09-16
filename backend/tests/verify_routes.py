import httpx

routes_to_test = [
    {
        "name": "Trip 1: LA to SF (Model 3, 70% Battery)",
        "payload": {
            "start_location": "Los Angeles, CA",
            "destination": "San Francisco, CA",
            "current_battery_pct": 70.0,
            "battery_capacity_kwh": 75.0,
            "vehicle_efficiency_wh_per_km": 150.0,
            "vehicle_model": "Tesla Model 3 Long Range",
            "min_stop_soc_pct": 10.0,
            "target_dest_soc_pct": 15.0
        }
    },
    {
        "name": "Trip 2: Seattle to Portland (Ioniq 5, 85% Battery - Direct)",
        "payload": {
            "start_location": "Seattle, WA",
            "destination": "Portland, OR",
            "current_battery_pct": 85.0,
            "battery_capacity_kwh": 77.4,
            "vehicle_efficiency_wh_per_km": 180.0,
            "vehicle_model": "Hyundai Ioniq 5 AWD"
        }
    },
    {
        "name": "Trip 3: NYC to Boston (Model Y, 35% Low Battery)",
        "payload": {
            "start_location": "New York, NY",
            "destination": "Boston, MA",
            "current_battery_pct": 35.0,
            "battery_capacity_kwh": 75.0,
            "vehicle_efficiency_wh_per_km": 168.0,
            "vehicle_model": "Tesla Model Y Long Range"
        }
    },
    {
        "name": "Trip 4: LA to Las Vegas (Mustang Mach-E, 50% Battery)",
        "payload": {
            "start_location": "Los Angeles, CA",
            "destination": "Las Vegas, NV",
            "current_battery_pct": 50.0,
            "battery_capacity_kwh": 91.0,
            "vehicle_efficiency_wh_per_km": 195.0,
            "vehicle_model": "Ford Mustang Mach-E ER"
        }
    },
    {
        "name": "Trip 5: Austin to Houston (Porsche Taycan, 60% Battery)",
        "payload": {
            "start_location": "Austin, TX",
            "destination": "Houston, TX",
            "current_battery_pct": 60.0,
            "battery_capacity_kwh": 93.4,
            "vehicle_efficiency_wh_per_km": 210.0,
            "vehicle_model": "Porsche Taycan Plus"
        }
    }
]

client = httpx.Client(timeout=20.0)

for item in routes_to_test:
    res = client.post("http://127.0.0.1:8000/api/route", json=item["payload"])
    assert res.status_code == 200, f"Failed: {res.status_code} {res.text}"
    data = res.json()
    s = data["summary"]
    print(f"=== {item['name']} ===")
    print(f"  Distance: {s['total_distance_km']} km ({s['total_distance_miles']} mi)")
    print(f"  Drive Time: {s['total_drive_time_min']}m | Charge Time: {s['total_charge_time_min']}m | Total: {s['total_trip_time_min']}m")
    print(f"  Stops Count: {s['num_stops']} | Feasible: {s['is_feasible']}")
    print(f"  Energy: {s['total_energy_consumed_kwh']} kWh | Cost: ${s['total_charging_cost_usd']:.2f} | CO2 Avoided: {s['co2_saved_kg']} kg")
    print(f"  Arrival Battery: {s['final_battery_pct']}%")
    if data["stops"]:
        for st in data["stops"]:
            print(f"    - Stop #{st['stop_index']}: {st['station']['name']} ({st['station']['operator']} {st['station']['power_kw']}kW) -> Charge {st['charge_duration_min']}m ({st['arrival_soc_pct']}% to {st['departure_soc_pct']}%)")
    print()
