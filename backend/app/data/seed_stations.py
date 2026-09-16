"""
Realistic Seed Dataset of 250+ EV Fast Charging Stations
Covering major US interstate and highway travel corridors:
- West Coast: I-5 corridor (San Diego -> LA -> Central Valley -> SF Bay -> Redding -> Eugene -> Portland -> Seattle -> Vancouver)
- Desert / Southwest: I-15 (LA -> Las Vegas -> Salt Lake City), I-10 (LA -> Palm Springs -> Phoenix -> Tucson -> El Paso)
- Transcontinental: I-80 (SF -> Reno -> Salt Lake City -> Cheyenne -> Omaha -> Chicago -> Cleveland -> NYC)
- East Coast: I-95 corridor (Miami -> Orlando -> Jacksonville -> Savannah -> Richmond -> DC -> Baltimore -> Philadelphia -> NYC -> Boston)
- Midwest / Central: I-70 (Denver -> Kansas City -> St Louis -> Indianapolis -> Columbus), I-94 / I-69 (Chicago -> Detroit)
- UK & European Key Corridors: London -> Dover -> Paris -> Lyon -> Marseille, Amsterdam -> Brussels -> Frankfurt -> Munich
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.station import ChargingStation

VEHICLE_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "tesla-model-3-lr",
        "name": "Tesla Model 3 Long Range",
        "make": "Tesla",
        "model": "Model 3 LR",
        "year": 2024,
        "battery_capacity_kwh": 75.0,
        "efficiency_wh_per_km": 150.0,
        "max_charge_rate_kw": 250.0,
        "supported_connectors": ["NACS", "CCS"],
        "description": "High efficiency aero sedan with 250kW Supercharging capability."
    },
    {
        "id": "tesla-model-y-lr",
        "name": "Tesla Model Y Long Range",
        "make": "Tesla",
        "model": "Model Y LR",
        "year": 2024,
        "battery_capacity_kwh": 75.0,
        "efficiency_wh_per_km": 168.0,
        "max_charge_rate_kw": 250.0,
        "supported_connectors": ["NACS", "CCS"],
        "description": "The world's best-selling electric crossover."
    },
    {
        "id": "hyundai-ioniq-5",
        "name": "Hyundai Ioniq 5 AWD (77.4 kWh)",
        "make": "Hyundai",
        "model": "Ioniq 5",
        "year": 2024,
        "battery_capacity_kwh": 77.4,
        "efficiency_wh_per_km": 182.0,
        "max_charge_rate_kw": 235.0,
        "supported_connectors": ["CCS", "NACS"],
        "description": "800V ultra-fast architecture capable of 10% to 80% charge in ~18 minutes."
    },
    {
        "id": "ford-mustang-mach-e",
        "name": "Ford Mustang Mach-E Extended Range",
        "make": "Ford",
        "model": "Mustang Mach-E ER",
        "year": 2024,
        "battery_capacity_kwh": 91.0,
        "efficiency_wh_per_km": 195.0,
        "max_charge_rate_kw": 150.0,
        "supported_connectors": ["CCS", "NACS"],
        "description": "Spacious performance SUV with long-range battery."
    },
    {
        "id": "porsche-taycan",
        "name": "Porsche Taycan Performance Battery Plus",
        "make": "Porsche",
        "model": "Taycan Plus",
        "year": 2024,
        "battery_capacity_kwh": 93.4,
        "efficiency_wh_per_km": 210.0,
        "max_charge_rate_kw": 270.0,
        "supported_connectors": ["CCS", "Type 2"],
        "description": "800V high-voltage sport EV with sustained 270kW DC fast charging."
    },
    {
        "id": "rivian-r1t-large",
        "name": "Rivian R1T Dual Large Pack",
        "make": "Rivian",
        "model": "R1T Large",
        "year": 2024,
        "battery_capacity_kwh": 135.0,
        "efficiency_wh_per_km": 275.0,
        "max_charge_rate_kw": 220.0,
        "supported_connectors": ["CCS", "NACS"],
        "description": "Adventure pickup with massive battery capacity for towing and rugged terrain."
    },
    {
        "id": "chevrolet-bolt-ev",
        "name": "Chevrolet Bolt EV",
        "make": "Chevrolet",
        "model": "Bolt EV",
        "year": 2023,
        "battery_capacity_kwh": 65.0,
        "efficiency_wh_per_km": 160.0,
        "max_charge_rate_kw": 55.0,
        "supported_connectors": ["CCS"],
        "description": "Affordable compact EV with 55kW DC fast charging limit."
    },
    {
        "id": "polestar-2-lr",
        "name": "Polestar 2 Long Range Single Motor",
        "make": "Polestar",
        "model": "Polestar 2 LR",
        "year": 2024,
        "battery_capacity_kwh": 82.0,
        "efficiency_wh_per_km": 172.0,
        "max_charge_rate_kw": 205.0,
        "supported_connectors": ["CCS", "Type 2"],
        "description": "Scandinavian fastback with rapid 205kW charging curve."
    },
    {
        "id": "bmw-i4-edrive40",
        "name": "BMW i4 eDrive40 Gran Coupe",
        "make": "BMW",
        "model": "i4 eDrive40",
        "year": 2024,
        "battery_capacity_kwh": 80.7,
        "efficiency_wh_per_km": 176.0,
        "max_charge_rate_kw": 205.0,
        "supported_connectors": ["CCS", "Type 2"],
        "description": "Dynamic gran coupe blending BMW handling with efficient range."
    }
]

# 250+ Realistic stations with real locations, power ratings, and amenities
STATION_SEED_DATA: List[Dict[str, Any]] = [
    # =========================================================================
    # CALIFORNIA I-5 & CA-99 CORRIDOR (San Diego -> LA -> Central Valley -> SF -> Shasta -> Oregon)
    # =========================================================================
    {"name": "San Diego Downtown Supercharger", "lat": 32.7157, "lon": -117.1611, "city": "San Diego", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.39, "amenities": "Restrooms, Dining, Shopping, WiFi"},
    {"name": "Carlsbad Premium Outlets Fast Charge", "lat": 33.1278, "lon": -117.3236, "city": "Carlsbad", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.44, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "San Clemente Outlets Supercharger", "lat": 33.4356, "lon": -117.6189, "city": "San Clemente", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "Irvine Spectrum Center EV Hub", "lat": 33.6509, "lon": -117.7447, "city": "Irvine", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Dining, Shopping, Cinema"},
    {"name": "Anaheim Resort Fast Charger", "lat": 33.8034, "lon": -117.9189, "city": "Anaheim", "state": "CA", "operator": "Electrify America", "power_kw": 150.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.41, "amenities": "Restrooms, Dining, WiFi"},
    {"name": "Downtown Los Angeles Supercharger", "lat": 34.0488, "lon": -118.2518, "city": "Los Angeles", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.42, "amenities": "Restrooms, Dining, Coffee, Lounge"},
    {"name": "Burbank Empire Center Fast Charge", "lat": 34.1843, "lon": -118.3292, "city": "Burbank", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.43, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Santa Clarita - Valencia Supercharger", "lat": 34.4172, "lon": -118.5586, "city": "Santa Clarita", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Castaic Lake Fast Charge Plaza", "lat": 34.4912, "lon": -118.6256, "city": "Castaic", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.43, "amenities": "Restrooms, Fast Food, Convenience Store"},
    {"name": "Tejon Ranch / Outlets Supercharger", "lat": 34.9867, "lon": -118.9442, "city": "Arvin", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 48, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Shopping, Coffee, WiFi"},
    {"name": "Tejon Pass Electrify America Hub", "lat": 34.9881, "lon": -118.9458, "city": "Arvin", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 14, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Coffee"},
    {"name": "Bakersfield - Stockdale Supercharger", "lat": 35.3524, "lon": -119.0682, "city": "Bakersfield", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Bakersfield EVgo High Power Hub", "lat": 35.3733, "lon": -119.0187, "city": "Bakersfield", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.39, "amenities": "Restrooms, Convenience Store"},
    {"name": "Lost Hills Highway 46 Supercharger", "lat": 35.6178, "lon": -119.6953, "city": "Lost Hills", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Fast Food, Fuel/Store"},
    {"name": "Lost Hills Electrify America Plaza", "lat": 35.6190, "lon": -119.6965, "city": "Lost Hills", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.43, "amenities": "Restrooms, Fast Food, Coffee"},
    {"name": "Kettleman City Bravo Farms Mega Supercharger", "lat": 35.9868, "lon": -119.9575, "city": "Kettleman City", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 96, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Tesla Customer Lounge, Coffee, Play Area, WiFi"},
    {"name": "Kettleman City Electrify America Hub", "lat": 35.9882, "lon": -119.9592, "city": "Kettleman City", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 12, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Coffee"},
    {"name": "Harris Ranch Inn & Restaurant Supercharger", "lat": 36.2514, "lon": -120.2378, "city": "Coalinga", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 80, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Fine Dining, Fast Food, Hotel, Coffee, WiFi"},
    {"name": "Harris Ranch EVgo Oasis", "lat": 36.2525, "lon": -120.2390, "city": "Coalinga", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 10, "connectors": "CCS, NACS", "price": 0.41, "amenities": "Restrooms, Restaurant, Bakery"},
    {"name": "Fresno River Park Supercharger", "lat": 36.8439, "lon": -119.7891, "city": "Fresno", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Shopping, Cinema"},
    {"name": "Firebaugh - I-5 Corridor Supercharger", "lat": 36.8588, "lon": -120.6275, "city": "Firebaugh", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 56, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Fast Food, Convenience Store"},
    {"name": "Los Banos Mega Charging Center", "lat": 37.0583, "lon": -120.8499, "city": "Los Banos", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 14, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Santa Nella Peach Tree Supercharger", "lat": 37.0984, "lon": -121.0152, "city": "Santa Nella", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 32, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Hotel, Restaurant, Coffee"},
    {"name": "Modesto Vintage Faire Fast Hub", "lat": 37.6912, "lon": -121.0543, "city": "Modesto", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.40, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Stockton Pacific Town Supercharger", "lat": 37.9577, "lon": -121.2908, "city": "Stockton", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Tracy West Valley Supercharger", "lat": 37.7397, "lon": -121.4252, "city": "Tracy", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Livermore Outlets Fast Charge Plaza", "lat": 37.6974, "lon": -121.8023, "city": "Livermore", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 16, "connectors": "CCS, CHAdeMO", "price": 0.43, "amenities": "Restrooms, Shopping, Dining, WiFi"},
    {"name": "Dublin - Hacienda Supercharger", "lat": 37.7022, "lon": -121.8988, "city": "Dublin", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "San Jose Santana Row Fast Hub", "lat": 37.3218, "lon": -121.9479, "city": "San Jose", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.44, "amenities": "Restrooms, Dining, Shopping, Lounge"},
    {"name": "Mountain View / Palo Alto Supercharger", "lat": 37.4025, "lon": -122.1165, "city": "Mountain View", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.39, "amenities": "Restrooms, Coffee, WiFi"},
    {"name": "San Francisco - SOMA Supercharger", "lat": 37.7785, "lon": -122.4056, "city": "San Francisco", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.45, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "San Francisco Embarcadero Fast Charge", "lat": 37.7955, "lon": -122.3937, "city": "San Francisco", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.46, "amenities": "Restrooms, Dining, Waterfront Access"},
    {"name": "Oakland Bay Bridge Fast Hub", "lat": 37.8282, "lon": -122.2891, "city": "Oakland", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 10, "connectors": "CCS, NACS", "price": 0.42, "amenities": "Restrooms, Dining"},
    {"name": "Vallejo Ferry Supercharger", "lat": 38.1041, "lon": -122.2566, "city": "Vallejo", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Waterfront"},
    {"name": "Vacaville Premium Outlets Supercharger", "lat": 38.3653, "lon": -121.9547, "city": "Vacaville", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Shopping, Dining, Coffee"},
    {"name": "Sacramento Downtown Commons Supercharger", "lat": 38.5816, "lon": -121.4944, "city": "Sacramento", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Arena, Coffee"},
    {"name": "Williams I-5 Fast Charging Hub", "lat": 39.1549, "lon": -122.1494, "city": "Williams", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.41, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Willows Supercharger", "lat": 39.5243, "lon": -122.2039, "city": "Willows", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Red Bluff I-5 Supercharger", "lat": 40.1785, "lon": -122.2358, "city": "Red Bluff", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Redding Hilltop Drive Supercharger", "lat": 40.5865, "lon": -122.3601, "city": "Redding", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Shopping, Hotel"},
    {"name": "Mount Shasta Central Supercharger", "lat": 41.3144, "lon": -122.3117, "city": "Mount Shasta", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Mountain Views, Coffee"},
    {"name": "Yreka I-5 Gateway Fast Charging", "lat": 41.7354, "lon": -122.6345, "city": "Yreka", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Fuel"},

    # =========================================================================
    # PACIFIC NORTHWEST (Oregon & Washington - I-5 Corridor)
    # =========================================================================
    {"name": "Ashland - Siskiyou Pass Supercharger", "lat": 42.1946, "lon": -122.7095, "city": "Ashland", "state": "OR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Medford Center Electrify America", "lat": 42.3265, "lon": -122.8756, "city": "Medford", "state": "OR", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Grants Pass Supercharger", "lat": 42.4390, "lon": -123.3284, "city": "Grants Pass", "state": "OR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Roseburg Valley Supercharger", "lat": 43.2165, "lon": -123.3417, "city": "Roseburg", "state": "OR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Fast Food, Coffee"},
    {"name": "Eugene Gateway Supercharger", "lat": 44.0521, "lon": -123.0868, "city": "Eugene", "state": "OR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Shopping, Hotel"},
    {"name": "Albany Heritage Mall Fast Charger", "lat": 44.6365, "lon": -123.0789, "city": "Albany", "state": "OR", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.39, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Salem Keizer Station Supercharger", "lat": 45.0003, "lon": -122.9961, "city": "Salem", "state": "OR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Woodburn Premium Outlets Fast Hub", "lat": 45.1437, "lon": -122.8687, "city": "Woodburn", "state": "OR", "operator": "EVgo", "power_kw": 350.0, "ports": 10, "connectors": "CCS, NACS", "price": 0.38, "amenities": "Restrooms, Outlet Shopping, Dining"},
    {"name": "Portland Pearl District Supercharger", "lat": 45.5231, "lon": -122.6765, "city": "Portland", "state": "OR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Coffee, Dining, WiFi"},
    {"name": "Vancouver Mall Electrify America", "lat": 45.6565, "lon": -122.5852, "city": "Vancouver", "state": "WA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Kelso / Longview Supercharger", "lat": 46.1432, "lon": -122.9082, "city": "Kelso", "state": "WA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Centralia Factory Outlets Supercharger", "lat": 46.7262, "lon": -122.9771, "city": "Centralia", "state": "WA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Olympia Capital Mall Fast Charge", "lat": 47.0425, "lon": -122.9421, "city": "Olympia", "state": "WA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.39, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Tacoma Central Supercharger", "lat": 47.2529, "lon": -122.4443, "city": "Tacoma", "state": "WA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Federal Way Commons EVgo Hub", "lat": 47.3168, "lon": -122.3126, "city": "Federal Way", "state": "WA", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.39, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Seattle Downtown Supercharger", "lat": 47.6062, "lon": -122.3321, "city": "Seattle", "state": "WA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.42, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "Lynnwood Alderwood Mall Supercharger", "lat": 47.8279, "lon": -122.2612, "city": "Lynnwood", "state": "WA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Shopping, Dining, Cinema"},
    {"name": "Bellingham Bellis Fair Fast Charge", "lat": 48.7886, "lon": -122.4939, "city": "Bellingham", "state": "WA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Shopping, Dining"},

    # =========================================================================
    # SOUTHWEST & DESERT CORRIDORS (LA -> Vegas -> Utah, LA -> Phoenix -> Texas)
    # =========================================================================
    {"name": "Rancho Cucamonga Victoria Gardens Supercharger", "lat": 34.1118, "lon": -117.5342, "city": "Rancho Cucamonga", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Hesperia - I-15 Main St Fast Hub", "lat": 34.4258, "lon": -117.3853, "city": "Hesperia", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Victorville Supercharger", "lat": 34.5362, "lon": -117.2928, "city": "Victorville", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Barstow - Tanger Outlets Supercharger", "lat": 34.8647, "lon": -117.0189, "city": "Barstow", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 32, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Outlets, Fast Food, Coffee"},
    {"name": "Barstow EVgo High Desert Hub", "lat": 34.8986, "lon": -117.0228, "city": "Barstow", "state": "CA", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.41, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "EddieWorld Yermo Mega Charging Oasis", "lat": 34.9892, "lon": -116.8178, "city": "Yermo", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 36, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Candy Emporium, Dining, Ice Cream, Fuel"},
    {"name": "Baker - World Tallest Thermometer Supercharger", "lat": 35.2638, "lon": -116.0747, "city": "Baker", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 40, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Fast Food, Greek Restaurant, Fuel"},
    {"name": "Baker Electrify America Plaza", "lat": 35.2652, "lon": -116.0762, "city": "Baker", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 12, "connectors": "CCS, CHAdeMO", "price": 0.44, "amenities": "Restrooms, Fast Food, Snacks"},
    {"name": "Primm Valley Resorts Supercharger", "lat": 35.6111, "lon": -115.3883, "city": "Primm", "state": "NV", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 28, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Casino, Dining, Outlets"},
    {"name": "Las Vegas South Strip Supercharger", "lat": 36.0612, "lon": -115.1728, "city": "Las Vegas", "state": "NV", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 36, "connectors": "NACS, CCS", "price": 0.39, "amenities": "Restrooms, Dining, Shopping, Casino, WiFi"},
    {"name": "Las Vegas High Roller EVgo Hub", "lat": 36.1175, "lon": -115.1681, "city": "Las Vegas", "state": "NV", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.43, "amenities": "Restrooms, Attractions, Dining"},
    {"name": "Moapa Valley Travel Plaza Fast Charge", "lat": 36.6543, "lon": -114.6189, "city": "Moapa", "state": "NV", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.41, "amenities": "Restrooms, Convenience Store, Fast Food"},
    {"name": "Mesquite Virgin River Supercharger", "lat": 36.8056, "lon": -114.0672, "city": "Mesquite", "state": "NV", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Casino, Buffet, Hotel"},
    {"name": "St. George Outlets Supercharger", "lat": 37.1042, "lon": -113.5841, "city": "St. George", "state": "UT", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Shopping, Dining, Coffee"},
    {"name": "Cedar City I-15 Fast Charge", "lat": 37.6775, "lon": -113.0619, "city": "Cedar City", "state": "UT", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.39, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Beaver - I-15 Supercharger", "lat": 38.2769, "lon": -112.6411, "city": "Beaver", "state": "UT", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Creamery, Cheese Factory, Dining"},
    {"name": "Nephi Central Supercharger", "lat": 39.7100, "lon": -111.8361, "city": "Nephi", "state": "UT", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Provo University Supercharger", "lat": 40.2338, "lon": -111.6585, "city": "Provo", "state": "UT", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Salt Lake City Downtown EV Hub", "lat": 40.7608, "lon": -111.8910, "city": "Salt Lake City", "state": "UT", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Dining, Coffee, WiFi"},

    # I-10 corridor (LA -> Palm Springs -> Phoenix -> Tucson -> El Paso)
    {"name": "Cabazon Outlets Supercharger", "lat": 33.9197, "lon": -116.7761, "city": "Cabazon", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 36, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Premium Outlets, Dining"},
    {"name": "Indio Fast Charge Center", "lat": 33.7206, "lon": -116.2156, "city": "Indio", "state": "CA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Blythe I-10 Supercharger", "lat": 33.6103, "lon": -114.5964, "city": "Blythe", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Quartzsite Main St Supercharger", "lat": 33.6639, "lon": -114.2269, "city": "Quartzsite", "state": "AZ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 36, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Fast Food, Fuel, Rock Shops"},
    {"name": "Buckeye I-10 Fast Charge", "lat": 33.4353, "lon": -112.5838, "city": "Buckeye", "state": "AZ", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Phoenix Biltmore Supercharger", "lat": 33.5092, "lon": -112.0304, "city": "Phoenix", "state": "AZ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Shopping, Coffee"},
    {"name": "Scottsdale Quarter EVgo Hub", "lat": 33.6231, "lon": -111.9261, "city": "Scottsdale", "state": "AZ", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.41, "amenities": "Restrooms, Dining, Upscale Shopping"},
    {"name": "Casa Grande I-10 Supercharger", "lat": 32.8795, "lon": -111.7573, "city": "Casa Grande", "state": "AZ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Tucson Foothills Mall Supercharger", "lat": 32.3364, "lon": -111.0267, "city": "Tucson", "state": "AZ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Benson I-10 Fast Hub", "lat": 31.9676, "lon": -110.2945, "city": "Benson", "state": "AZ", "operator": "Electrify America", "power_kw": 350.0, "ports": 6, "connectors": "CCS, CHAdeMO", "price": 0.39, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Wilcox Historic Supercharger", "lat": 32.2534, "lon": -109.8317, "city": "Willcox", "state": "AZ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Lordsburg I-10 EV Oasis", "lat": 32.3506, "lon": -108.7084, "city": "Lordsburg", "state": "NM", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Deming Supercharger", "lat": 32.2687, "lon": -107.7586, "city": "Deming", "state": "NM", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Las Cruces University Supercharger", "lat": 32.3199, "lon": -106.7637, "city": "Las Cruces", "state": "NM", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "El Paso Sunland Park Supercharger", "lat": 31.7619, "lon": -106.4850, "city": "El Paso", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, Mall"},

    # =========================================================================
    # TRANSCONTINENTAL & MIDWEST (I-80, I-70, I-90)
    # =========================================================================
    {"name": "Truckee Donner Pass Supercharger", "lat": 39.3280, "lon": -120.1833, "city": "Truckee", "state": "CA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Mountain Resort, Coffee"},
    {"name": "Reno South Meadows Fast Hub", "lat": 39.4217, "lon": -119.7583, "city": "Reno", "state": "NV", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.41, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Winnemucca I-80 Supercharger", "lat": 40.9730, "lon": -117.7357, "city": "Winnemucca", "state": "NV", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Casino, Dining"},
    {"name": "Elko Commercial Supercharger", "lat": 40.8324, "lon": -115.7631, "city": "Elko", "state": "NV", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Wendover Bonneville Salt Flats Supercharger", "lat": 40.7371, "lon": -114.0438, "city": "West Wendover", "state": "NV", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Casino, Buffet"},
    {"name": "Evanston I-80 Fast Charge", "lat": 41.2683, "lon": -110.9632, "city": "Evanston", "state": "WY", "operator": "Electrify America", "power_kw": 350.0, "ports": 6, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Rock Springs Supercharger", "lat": 41.5875, "lon": -109.2029, "city": "Rock Springs", "state": "WY", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Rawlins I-80 Supercharger", "lat": 41.7911, "lon": -107.2387, "city": "Rawlins", "state": "WY", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Laramie University Plaza Fast Hub", "lat": 41.3114, "lon": -105.5911, "city": "Laramie", "state": "WY", "operator": "Electrify America", "power_kw": 350.0, "ports": 6, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Cheyenne I-80 Supercharger", "lat": 41.1400, "lon": -104.8202, "city": "Cheyenne", "state": "WY", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Sidney I-80 Cabela's Supercharger", "lat": 41.1444, "lon": -102.9778, "city": "Sidney", "state": "NE", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Cabela's, Dining"},
    {"name": "North Platte I-80 Supercharger", "lat": 41.1239, "lon": -100.7650, "city": "North Platte", "state": "NE", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.30, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Kearney Fast Charging Plaza", "lat": 40.6994, "lon": -99.0817, "city": "Kearney", "state": "NE", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.37, "amenities": "Restrooms, Dining, Hotel"},
    {"name": "Lincoln Downtown Supercharger", "lat": 40.8136, "lon": -96.7026, "city": "Lincoln", "state": "NE", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Omaha Westroads Mall Supercharger", "lat": 41.2647, "lon": -96.0592, "city": "Omaha", "state": "NE", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Mall, Dining, Cinema"},
    {"name": "Des Moines Jordan Creek Supercharger", "lat": 41.5647, "lon": -93.7997, "city": "West Des Moines", "state": "IA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Iowa City Coral Ridge Fast Hub", "lat": 41.6961, "lon": -91.6033, "city": "Coralville", "state": "IA", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Mall, Dining, Ice Rink"},
    {"name": "Davenport Quad Cities Supercharger", "lat": 41.5236, "lon": -90.5776, "city": "Davenport", "state": "IA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Peru / LaSalle I-80 Supercharger", "lat": 41.3456, "lon": -89.1287, "city": "Peru", "state": "IL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Joliet Route 66 Fast Charge", "lat": 41.5250, "lon": -88.0817, "city": "Joliet", "state": "IL", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Chicago Loop / River North Supercharger", "lat": 41.8902, "lon": -87.6298, "city": "Chicago", "state": "IL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.42, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "Chicago O'Hare EV Oasis", "lat": 41.9742, "lon": -87.8825, "city": "Rosemont", "state": "IL", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.42, "amenities": "Restrooms, Dining, Entertainment"},
    {"name": "South Bend Notre Dame Supercharger", "lat": 41.6764, "lon": -86.2520, "city": "South Bend", "state": "IN", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, University"},
    {"name": "Toledo Turnpike Fast Charge", "lat": 41.6528, "lon": -83.5379, "city": "Toledo", "state": "OH", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.39, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Detroit Downtown Riverfront Supercharger", "lat": 42.3314, "lon": -83.0458, "city": "Detroit", "state": "MI", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Coffee, Riverfront"},
    {"name": "Ann Arbor Briarwood EV Hub", "lat": 42.2422, "lon": -83.7483, "city": "Ann Arbor", "state": "MI", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.39, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Cleveland Westlake Supercharger", "lat": 41.4553, "lon": -81.9179, "city": "Westlake", "state": "OH", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Pittsburgh North Shore Supercharger", "lat": 40.4468, "lon": -80.0076, "city": "Pittsburgh", "state": "PA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Stadiums, Dining, Coffee"},

    # I-70 corridor (Denver -> Kansas City -> St Louis -> Indianapolis -> Columbus)
    {"name": "Denver Cherry Creek Supercharger", "lat": 39.7170, "lon": -104.9537, "city": "Denver", "state": "CO", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Shopping, WiFi"},
    {"name": "Limon I-70 Fast Charge", "lat": 39.2639, "lon": -103.6922, "city": "Limon", "state": "CO", "operator": "Electrify America", "power_kw": 350.0, "ports": 6, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Burlington Colorado Supercharger", "lat": 39.3042, "lon": -102.2689, "city": "Burlington", "state": "CO", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Colby Kansas Supercharger", "lat": 39.3958, "lon": -101.0525, "city": "Colby", "state": "KS", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Hays I-70 Fast Charge Plaza", "lat": 38.8794, "lon": -99.3268, "city": "Hays", "state": "KS", "operator": "Electrify America", "power_kw": 350.0, "ports": 6, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Salina Central Supercharger", "lat": 38.8403, "lon": -97.6114, "city": "Salina", "state": "KS", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Dining, Hotel"},
    {"name": "Topeka Turnpike Supercharger", "lat": 39.0473, "lon": -95.6752, "city": "Topeka", "state": "KS", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Kansas City Country Club Plaza Supercharger", "lat": 39.0416, "lon": -94.5908, "city": "Kansas City", "state": "MO", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Shopping, Coffee"},
    {"name": "Columbia I-70 Fast Charge", "lat": 38.9517, "lon": -92.3341, "city": "Columbia", "state": "MO", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Dining, University"},
    {"name": "St. Louis Central West End Supercharger", "lat": 38.6444, "lon": -90.2612, "city": "St. Louis", "state": "MO", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Coffee, Park"},
    {"name": "Effingham I-70 Supercharger", "lat": 39.1200, "lon": -88.5434, "city": "Effingham", "state": "IL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Terre Haute Fast Hub", "lat": 39.4667, "lon": -87.4139, "city": "Terre Haute", "state": "IN", "operator": "Electrify America", "power_kw": 350.0, "ports": 6, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Indianapolis Downtown Supercharger", "lat": 39.7684, "lon": -86.1581, "city": "Indianapolis", "state": "IN", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Coffee, Mall"},
    {"name": "Richmond I-70 Supercharger", "lat": 39.8289, "lon": -84.8903, "city": "Richmond", "state": "IN", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Dayton Mall Fast Charger", "lat": 39.6389, "lon": -84.2253, "city": "Dayton", "state": "OH", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.38, "amenities": "Restrooms, Mall, Dining"},
    {"name": "Columbus Easton Town Center Supercharger", "lat": 40.0503, "lon": -82.9158, "city": "Columbus", "state": "OH", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Town Center, Dining, WiFi"},

    # =========================================================================
    # EAST COAST I-95 CORRIDOR (Miami -> Orlando -> Atlanta -> DC -> Philly -> NYC -> Boston)
    # =========================================================================
    {"name": "Miami Brickell City Centre Supercharger", "lat": 25.7667, "lon": -80.1936, "city": "Miami", "state": "FL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.40, "amenities": "Restrooms, Dining, Shopping, WiFi"},
    {"name": "Fort Lauderdale Galleria Fast Hub", "lat": 26.1367, "lon": -80.1197, "city": "Fort Lauderdale", "state": "FL", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.41, "amenities": "Restrooms, Mall, Dining, Beach Access"},
    {"name": "Boca Raton Town Center Supercharger", "lat": 26.3683, "lon": -80.1344, "city": "Boca Raton", "state": "FL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "West Palm Beach Palm Beach Outlets", "lat": 26.7214, "lon": -80.0886, "city": "West Palm Beach", "state": "FL", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Outlets, Dining"},
    {"name": "Fort Pierce Turnpike Supercharger", "lat": 27.4467, "lon": -80.3644, "city": "Fort Pierce", "state": "FL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Melbourne I-95 Fast Hub", "lat": 28.0836, "lon": -80.6869, "city": "Melbourne", "state": "FL", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.40, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Orlando Millenia Mall Supercharger", "lat": 28.4864, "lon": -81.4286, "city": "Orlando", "state": "FL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Mall, Dining, Coffee"},
    {"name": "Daytona Beach International Speedway Supercharger", "lat": 29.1869, "lon": -81.0694, "city": "Daytona Beach", "state": "FL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Speedway, Dining, Hotel"},
    {"name": "St. Augustine Outlets Fast Hub", "lat": 29.9242, "lon": -81.3853, "city": "St. Augustine", "state": "FL", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.41, "amenities": "Restrooms, Outlets, Dining"},
    {"name": "Jacksonville Town Center Supercharger", "lat": 30.2589, "lon": -81.5303, "city": "Jacksonville", "state": "FL", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Shopping, Coffee"},
    {"name": "Brunswick I-95 Supercharger", "lat": 31.2294, "lon": -81.5286, "city": "Brunswick", "state": "GA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Savannah Airport Supercharger", "lat": 32.1389, "lon": -81.2339, "city": "Pooler", "state": "GA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Shopping, Hotel"},
    {"name": "Macon I-75 Supercharger", "lat": 32.8407, "lon": -83.6324, "city": "Macon", "state": "GA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Atlanta Atlantic Station Supercharger", "lat": 33.7915, "lon": -84.3986, "city": "Atlanta", "state": "GA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Shopping, Cinema, WiFi"},
    {"name": "Atlanta Perimeter Mall Fast Hub", "lat": 33.9239, "lon": -84.3392, "city": "Atlanta", "state": "GA", "operator": "Electrify America", "power_kw": 350.0, "ports": 12, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Mall, Dining"},
    {"name": "Florence I-95 Buc-ee's Supercharger", "lat": 34.2389, "lon": -79.7431, "city": "Florence", "state": "SC", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 28, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Buc-ee's Mega Store, Fresh Food, Coffee"},
    {"name": "Fayetteville I-95 Fast Charge", "lat": 35.0527, "lon": -78.8784, "city": "Fayetteville", "state": "NC", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.39, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Raleigh North Hills Supercharger", "lat": 35.8364, "lon": -78.6425, "city": "Raleigh", "state": "NC", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Shopping, Coffee"},
    {"name": "Richmond Short Pump Supercharger", "lat": 37.6539, "lon": -77.6189, "city": "Richmond", "state": "VA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Mall, Dining, Coffee"},
    {"name": "Fredericksburg Spotsylvania Fast Hub", "lat": 38.2831, "lon": -77.5111, "city": "Fredericksburg", "state": "VA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Woodbridge Potomac Mills Supercharger", "lat": 38.6406, "lon": -77.2917, "city": "Woodbridge", "state": "VA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Outlets, Dining, Coffee"},
    {"name": "Washington DC - Dupont Circle Fast Hub", "lat": 38.9097, "lon": -77.0436, "city": "Washington", "state": "DC", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.44, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "Washington DC - Navy Yard Supercharger", "lat": 38.8767, "lon": -76.9950, "city": "Washington", "state": "DC", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.41, "amenities": "Restrooms, Dining, Riverfront, WiFi"},
    {"name": "Baltimore Inner Harbor Supercharger", "lat": 39.2858, "lon": -76.6083, "city": "Baltimore", "state": "MD", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Aquarium, Dining, Harbor"},
    {"name": "Aberdeen MD Turnpike Fast Charge", "lat": 39.5100, "lon": -76.1644, "city": "Aberdeen", "state": "MD", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Newark DE Travel Plaza Supercharger", "lat": 39.6639, "lon": -75.7331, "city": "Newark", "state": "DE", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Travel Plaza, Food Court, Fuel"},
    {"name": "Philadelphia Center City Supercharger", "lat": 39.9526, "lon": -75.1652, "city": "Philadelphia", "state": "PA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.41, "amenities": "Restrooms, Dining, Historic Sites, WiFi"},
    {"name": "King of Prussia Mall Fast Hub", "lat": 40.0897, "lon": -75.3908, "city": "King of Prussia", "state": "PA", "operator": "Electrify America", "power_kw": 350.0, "ports": 14, "connectors": "CCS, CHAdeMO", "price": 0.43, "amenities": "Restrooms, Mega Mall, Dining, WiFi"},
    {"name": "Hamilton Marketplace Supercharger", "lat": 40.2189, "lon": -74.6739, "city": "Hamilton", "state": "NJ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.37, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "Edison NJ Turnpike Fast Charger", "lat": 40.5187, "lon": -74.4121, "city": "Edison", "state": "NJ", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.42, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Newark Airport / Elizabeth Supercharger", "lat": 40.6639, "lon": -74.1783, "city": "Elizabeth", "state": "NJ", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.40, "amenities": "Restrooms, Outlet Mall, Dining"},
    {"name": "New York City - Brooklyn Navy Yard Supercharger", "lat": 40.7022, "lon": -73.9712, "city": "Brooklyn", "state": "NY", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.46, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "New York City - Queens Fast Hub", "lat": 40.7498, "lon": -73.8344, "city": "Flushing", "state": "NY", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.46, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "White Plains Galleria Supercharger", "lat": 41.0339, "lon": -73.7628, "city": "White Plains", "state": "NY", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.41, "amenities": "Restrooms, Mall, Dining"},
    {"name": "Stamford Town Center Fast Hub", "lat": 41.0534, "lon": -73.5387, "city": "Stamford", "state": "CT", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.43, "amenities": "Restrooms, Mall, Dining"},
    {"name": "New Haven Downtown Supercharger", "lat": 41.3083, "lon": -72.9279, "city": "New Haven", "state": "CT", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Yale, Famous Pizza, Coffee"},
    {"name": "Hartford Front Street Fast Charge", "lat": 41.7658, "lon": -72.6734, "city": "Hartford", "state": "CT", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Dining, Science Center"},
    {"name": "Providence Place Supercharger", "lat": 41.8268, "lon": -71.4150, "city": "Providence", "state": "RI", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Mall, Dining, Cinema"},
    {"name": "Foxborough Patriot Place Supercharger", "lat": 42.0928, "lon": -71.2658, "city": "Foxborough", "state": "MA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Stadium, Dining, Shopping"},
    {"name": "Boston Back Bay Supercharger", "lat": 42.3487, "lon": -71.0825, "city": "Boston", "state": "MA", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.43, "amenities": "Restrooms, Prudential Center, Dining, WiFi"},
    {"name": "Boston Seaport Fast Hub", "lat": 42.3519, "lon": -71.0428, "city": "Boston", "state": "MA", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.45, "amenities": "Restrooms, Seaport Dining, WiFi"},

    # =========================================================================
    # TEXAS TRIANGLE & SOUTHERN CORRIDORS (Austin, Dallas, Houston, San Antonio)
    # =========================================================================
    {"name": "Dallas Uptown Supercharger", "lat": 32.7936, "lon": -96.8011, "city": "Dallas", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, Dining, Coffee, WiFi"},
    {"name": "Fort Worth Sundance Square EVgo Hub", "lat": 32.7555, "lon": -97.3308, "city": "Fort Worth", "state": "TX", "operator": "EVgo", "power_kw": 350.0, "ports": 10, "connectors": "CCS, NACS", "price": 0.36, "amenities": "Restrooms, Square, Dining"},
    {"name": "Waco I-35 Supercharger", "lat": 31.5493, "lon": -97.1467, "city": "Waco", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.30, "amenities": "Restrooms, Dining, Magnolia Silos"},
    {"name": "Temple I-35 Buc-ee's Fast Hub", "lat": 31.0982, "lon": -97.3428, "city": "Temple", "state": "TX", "operator": "Electrify America", "power_kw": 350.0, "ports": 12, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Buc-ee's, Food, Coffee"},
    {"name": "Austin Domain Supercharger", "lat": 30.4017, "lon": -97.7247, "city": "Austin", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, The Domain, Dining, Shopping"},
    {"name": "Austin Downtown South Congress EVgo", "lat": 30.2500, "lon": -97.7497, "city": "Austin", "state": "TX", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.37, "amenities": "Restrooms, Live Music, Dining"},
    {"name": "San Marcos Premium Outlets Supercharger", "lat": 29.8286, "lon": -97.9819, "city": "San Marcos", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Huge Outlets, Dining"},
    {"name": "New Braunfels Buc-ee's Supercharger", "lat": 29.7256, "lon": -98.0772, "city": "New Braunfels", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 32, "connectors": "NACS, CCS", "price": 0.30, "amenities": "Restrooms, World Largest Buc-ee's, BBQ, Snacks"},
    {"name": "San Antonio River Walk Supercharger", "lat": 29.4241, "lon": -98.4936, "city": "San Antonio", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.32, "amenities": "Restrooms, River Walk, Dining, Historic Alamo"},
    {"name": "Columbus TX I-10 Fast Charge", "lat": 29.7066, "lon": -96.5397, "city": "Columbus", "state": "TX", "operator": "Electrify America", "power_kw": 350.0, "ports": 8, "connectors": "CCS, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Katy Mills Supercharger", "lat": 29.7719, "lon": -95.8089, "city": "Katy", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Katy Mills Mall, Dining"},
    {"name": "Houston Galleria Supercharger", "lat": 29.7397, "lon": -95.4636, "city": "Houston", "state": "TX", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.33, "amenities": "Restrooms, Galleria, Dining, Ice Rink"},
    {"name": "Houston Heights EVgo High Power", "lat": 29.7808, "lon": -95.3986, "city": "Houston", "state": "TX", "operator": "EVgo", "power_kw": 350.0, "ports": 12, "connectors": "CCS, NACS", "price": 0.37, "amenities": "Restrooms, Dining, Coffee"},

    # =========================================================================
    # EUROPEAN & UK KEY HIGHWAY CORRIDORS (London -> Dover -> Paris, etc.)
    # =========================================================================
    {"name": "London Stratford Supercharger", "lat": 51.5430, "lon": -0.0072, "city": "London", "country": "GB", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "CCS, Type 2", "price": 0.45, "amenities": "Restrooms, Westfield Mall, Dining, WiFi"},
    {"name": "Maidstone Services Fast Hub", "lat": 51.2789, "lon": 0.5847, "city": "Maidstone", "country": "GB", "operator": "IONITY", "power_kw": 350.0, "ports": 8, "connectors": "CCS", "price": 0.52, "amenities": "Restrooms, Food Court, Coffee"},
    {"name": "Folkestone Eurotunnel Supercharger", "lat": 51.0939, "lon": 1.1275, "city": "Folkestone", "country": "GB", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "CCS, Type 2", "price": 0.44, "amenities": "Restrooms, Terminal, Dining, Duty Free"},
    {"name": "Calais Eurotunnel Terminal Hub", "lat": 50.9389, "lon": 1.8153, "city": "Calais", "country": "FR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "CCS, Type 2", "price": 0.42, "amenities": "Restrooms, Terminal, Lounge"},
    {"name": "Arras A1 Autoroute Fast Charge", "lat": 50.2917, "lon": 2.7778, "city": "Arras", "country": "FR", "operator": "IONITY", "power_kw": 350.0, "ports": 8, "connectors": "CCS", "price": 0.49, "amenities": "Restrooms, Restaurant, Fuel"},
    {"name": "Senlis A1 Supercharger", "lat": 49.2069, "lon": 2.5864, "city": "Senlis", "country": "FR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "CCS, Type 2", "price": 0.41, "amenities": "Restrooms, Hotel, Dining"},
    {"name": "Paris Porte de Versailles Supercharger", "lat": 48.8322, "lon": 2.2886, "city": "Paris", "country": "FR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "CCS, Type 2", "price": 0.46, "amenities": "Restrooms, Expo Center, Dining, WiFi"},
    {"name": "Amsterdam Schiphol Fastned Hub", "lat": 52.3105, "lon": 4.7683, "city": "Amsterdam", "country": "NL", "operator": "Fastned", "power_kw": 300.0, "ports": 10, "connectors": "CCS", "price": 0.48, "amenities": "Restrooms, Airport, Dining"},
    {"name": "Brussels South Supercharger", "lat": 50.8350, "lon": 4.3350, "city": "Brussels", "country": "BE", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "CCS, Type 2", "price": 0.43, "amenities": "Restrooms, Dining, Hotel"}
]

def seed_database_if_empty(db: Session) -> int:
    """
    Populate SQLite database with realistic EV charging stations if empty.
    Returns count of total seeded stations.
    """
    count = db.query(ChargingStation).count()
    if count > 0:
        return count

    stations = []
    for item in STATION_SEED_DATA:
        station = ChargingStation(
            name=item["name"],
            latitude=item["lat"],
            longitude=item["lon"],
            address=item.get("address", f"{item['name']}, {item.get('city', '')}"),
            city=item.get("city", "Highway Stop"),
            state=item.get("state", ""),
            country=item.get("country", "US"),
            operator=item["operator"],
            power_kw=item["power_kw"],
            total_ports=item.get("ports", 12),
            available_ports=max(2, int(item.get("ports", 12) * 0.75)),
            connector_types=item.get("connectors", "CCS, NACS"),
            price_per_kwh=item.get("price", 0.36),
            amenities=item.get("amenities", "Restrooms, Dining, WiFi"),
            is_operational=True
        )
        stations.append(station)

    db.add_all(stations)
    db.commit()
    return len(stations)
