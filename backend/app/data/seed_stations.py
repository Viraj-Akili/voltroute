"""
Realistic Seed Dataset of EV Fast Charging Stations
Focusing primarily on India (Tamil Nadu, Karnataka, Andhra Pradesh, and National Highways):
- NH 48: Chennai -> Sriperumbudur -> Kanchipuram -> Ranipet -> Vellore -> Ambur -> Vaniyambadi -> Krishnagiri -> Hosur -> Bengaluru
- NH 40 / NH 234: Vellore -> Chittoor -> Tirupati
- NH 38 / NH 32: Vellore -> Arani -> Tindivanam -> Pondicherry (Puducherry)
- Southern Arterials: Chennai -> Tindivanam -> Villupuram -> Trichy -> Madurai, Salem -> Coimbatore
- Major Urban Centers: Vellore, Chennai, Bengaluru, Hyderabad, Mumbai, Delhi
- Plus international corridor stations maintained for global compatibility.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.station import ChargingStation

VEHICLE_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "tata-nexon-ev-lr",
        "name": "Tata Nexon EV Long Range",
        "make": "Tata",
        "model": "Nexon EV LR",
        "year": 2024,
        "battery_capacity_kwh": 40.5,
        "efficiency_wh_per_km": 138.0,
        "max_charge_rate_kw": 50.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "India's most popular electric SUV with 40.5 kWh LFP pack and real-world range of ~280 km."
    },
    {
        "id": "tata-punch-ev-lr",
        "name": "Tata Punch EV Long Range",
        "make": "Tata",
        "model": "Punch EV LR",
        "year": 2024,
        "battery_capacity_kwh": 35.0,
        "efficiency_wh_per_km": 128.0,
        "max_charge_rate_kw": 50.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "Compact electric SUV built on Tata's pure EV acti.ev platform."
    },
    {
        "id": "mg-zs-ev",
        "name": "MG ZS EV",
        "make": "MG",
        "model": "ZS EV",
        "year": 2024,
        "battery_capacity_kwh": 50.3,
        "efficiency_wh_per_km": 150.0,
        "max_charge_rate_kw": 80.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "Premium electric crossover with 50.3 kWh battery and 80kW DC fast charging."
    },
    {
        "id": "mahindra-xuv400",
        "name": "Mahindra XUV400 EV",
        "make": "Mahindra",
        "model": "XUV400 EL Pro",
        "year": 2024,
        "battery_capacity_kwh": 39.4,
        "efficiency_wh_per_km": 145.0,
        "max_charge_rate_kw": 50.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "Spacious electric SUV from Mahindra with fast acceleration and 39.4 kWh capacity."
    },
    {
        "id": "tata-tiago-ev",
        "name": "Tata Tiago EV Long Range",
        "make": "Tata",
        "model": "Tiago EV LR",
        "year": 2024,
        "battery_capacity_kwh": 24.0,
        "efficiency_wh_per_km": 115.0,
        "max_charge_rate_kw": 30.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "Efficient city EV hatchback with 24 kWh pack for intercity commutes."
    },
    {
        "id": "hyundai-ioniq-5-in",
        "name": "Hyundai Ioniq 5 (72.6 kWh)",
        "make": "Hyundai",
        "model": "Ioniq 5",
        "year": 2024,
        "battery_capacity_kwh": 72.6,
        "efficiency_wh_per_km": 165.0,
        "max_charge_rate_kw": 235.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "800V ultra-fast charging architecture capable of 10% to 80% charge in ~18 minutes."
    },
    {
        "id": "byd-atto-3",
        "name": "BYD Atto 3",
        "make": "BYD",
        "model": "Atto 3",
        "year": 2024,
        "battery_capacity_kwh": 60.48,
        "efficiency_wh_per_km": 155.0,
        "max_charge_rate_kw": 80.0,
        "supported_connectors": ["CCS2", "CCS", "Type 2"],
        "description": "Blade battery crossover offering high thermal stability and 60.48 kWh capacity."
    },
    {
        "id": "tesla-model-3-lr",
        "name": "Tesla Model 3 Long Range",
        "make": "Tesla",
        "model": "Model 3 LR",
        "year": 2024,
        "battery_capacity_kwh": 75.0,
        "efficiency_wh_per_km": 150.0,
        "max_charge_rate_kw": 250.0,
        "supported_connectors": ["NACS", "CCS2", "CCS"],
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
        "supported_connectors": ["NACS", "CCS2", "CCS"],
        "description": "The world's best-selling electric crossover."
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
        "supported_connectors": ["CCS2", "CCS", "NACS"],
        "description": "Spacious performance SUV with long-range battery."
    }
]

# Realistic charging stations dataset with primary Indian infrastructure
STATION_SEED_DATA: List[Dict[str, Any]] = [
    # =========================================================================
    # VELLORE, CHENNAI, BENGALURU, TIRUPATI & TAMIL NADU CORRIDORS (NH 48, NH 40, NH 38)
    # =========================================================================
    # Vellore City & Bypass
    {"name": "Tata Power EZ Charge - Green Circle", "lat": 12.9250, "lon": 79.1350, "city": "Vellore", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 4, "connectors": "CCS2, Type 2", "price": 19.50, "amenities": "Restrooms, Dining, Coffee, Parking"},
    {"name": "Zeon Charging - Katpadi Fast Hub", "lat": 12.9730, "lon": 79.1410, "city": "Vellore", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Hotel, Restaurant, WiFi"},
    {"name": "Jio-bp pulse - VIT Bypass Hub", "lat": 12.9450, "lon": 79.1550, "city": "Vellore", "state": "Tamil Nadu", "country": "India", "operator": "Jio-bp pulse", "power_kw": 60.0, "ports": 4, "connectors": "CCS2, Type 2", "price": 20.00, "amenities": "Restrooms, Snacks, Convenience Store"},
    {"name": "ChargeZone - Hotel GRT Grand Fast Charger", "lat": 12.9220, "lon": 79.1280, "city": "Vellore", "state": "Tamil Nadu", "country": "India", "operator": "ChargeZone", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 20.50, "amenities": "Restrooms, Fine Dining, Coffee, Hotel"},

    # Vellore -> Chennai Corridor (NH 48 Eastward: Ranipet -> Walajah -> Kanchipuram -> Sriperumbudur -> Poonamallee -> Chennai)
    {"name": "Relux Electric - Walajah Toll Fast Hub", "lat": 12.9360, "lon": 79.3520, "city": "Ranipet", "state": "Tamil Nadu", "country": "India", "operator": "Relux Electric", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 20.00, "amenities": "Restrooms, Highway Restaurant, Coffee"},
    {"name": "Zeon Charging - Hotel Saravana Bhavan, Kanchipuram Bypass", "lat": 12.8450, "lon": 79.6850, "city": "Kanchipuram", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Vegetarian Dining, Coffee, Shopping"},
    {"name": "ChargeZone - Kanchipuram Highway Oasis", "lat": 12.8380, "lon": 79.7120, "city": "Kanchipuram", "state": "Tamil Nadu", "country": "India", "operator": "ChargeZone", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 20.00, "amenities": "Restrooms, Dining, Snacks"},
    {"name": "Tata Power - Sriperumbudur Industrial Fast Hub", "lat": 12.9710, "lon": 79.9480, "city": "Sriperumbudur", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 19.50, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Jio-bp pulse - Sriperumbudur Highway Plaza", "lat": 12.9680, "lon": 79.9550, "city": "Sriperumbudur", "state": "Tamil Nadu", "country": "India", "operator": "Jio-bp pulse", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 20.00, "amenities": "Restrooms, Food Court, Fuel"},
    {"name": "Statiq - Poonamallee Gateway EV Hub", "lat": 13.0480, "lon": 80.0890, "city": "Chennai West", "state": "Tamil Nadu", "country": "India", "operator": "Statiq", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 20.50, "amenities": "Restrooms, Fast Food, Coffee"},

    # Chennai City & Tech Hubs
    {"name": "Tata Power EZ Charge - Phoenix Marketcity", "lat": 12.9915, "lon": 80.2170, "city": "Chennai", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 20.00, "amenities": "Restrooms, Mall, Dining, Cinema, WiFi"},
    {"name": "Zeon Charging - Ampa Skywalk Mall", "lat": 13.0720, "lon": 80.2180, "city": "Chennai", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 4, "connectors": "CCS2, Type 2", "price": 21.50, "amenities": "Restrooms, Shopping, Dining, Coffee"},
    {"name": "Jio-bp pulse - Guindy Tech Park Hub", "lat": 13.0080, "lon": 80.2040, "city": "Chennai", "state": "Tamil Nadu", "country": "India", "operator": "Jio-bp pulse", "power_kw": 150.0, "ports": 8, "connectors": "CCS2, Type 2", "price": 22.00, "amenities": "Restrooms, Tech Park Dining, Coffee"},
    {"name": "ChargeZone - Chennai Central EV Plaza", "lat": 13.0820, "lon": 80.2740, "city": "Chennai", "state": "Tamil Nadu", "country": "India", "operator": "ChargeZone", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 20.00, "amenities": "Restrooms, Railway Station, Food"},
    {"name": "Tata Power - OMR Sholinganallur Fast Hub", "lat": 12.9010, "lon": 80.2280, "city": "Chennai", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, IT Corridor, Coffee, Dining"},

    # Vellore -> Bengaluru Corridor (NH 48 Westward: Ambur -> Vaniyambadi -> Krishnagiri -> Hosur -> Electronic City -> Bengaluru)
    {"name": "Zeon Charging - Ambur Biryani Highway Plaza", "lat": 12.7910, "lon": 78.7180, "city": "Ambur", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Famous Ambur Biryani Dining, Coffee, Rest Area"},
    {"name": "Tata Power - Vaniyambadi Highway Retreat", "lat": 12.6840, "lon": 78.6200, "city": "Vaniyambadi", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 4, "connectors": "CCS2, Type 2", "price": 19.50, "amenities": "Restrooms, Highway Motel, Dining"},
    {"name": "ChargeZone - Krishnagiri Toll Plaza Ultra-Fast", "lat": 12.5280, "lon": 78.2160, "city": "Krishnagiri", "state": "Tamil Nadu", "country": "India", "operator": "ChargeZone", "power_kw": 150.0, "ports": 8, "connectors": "CCS2, Type 2", "price": 22.00, "amenities": "Restrooms, Food Court, Coffee, Fuel"},
    {"name": "Zeon Charging - Hotel Murugan Idli Shop, Krishnagiri", "lat": 12.5410, "lon": 78.1920, "city": "Krishnagiri", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Murugan Idli Dining, Filter Coffee"},
    {"name": "Relux - Hosur Highway Fast Charge Plaza", "lat": 12.7420, "lon": 77.8280, "city": "Hosur", "state": "Tamil Nadu", "country": "India", "operator": "Relux Electric", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 20.50, "amenities": "Restrooms, Restaurant, Coffee"},
    {"name": "Jio-bp pulse - Electronic City Hub", "lat": 12.8450, "lon": 77.6650, "city": "Bengaluru", "state": "Karnataka", "country": "India", "operator": "Jio-bp pulse", "power_kw": 150.0, "ports": 8, "connectors": "CCS2, Type 2", "price": 22.00, "amenities": "Restrooms, Dining, Coffee, Tech Corridor"},
    {"name": "Tata Power EZ Charge - Indiranagar", "lat": 12.9780, "lon": 77.6400, "city": "Bengaluru", "state": "Karnataka", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 20.00, "amenities": "Restrooms, Cafes, Dining, Shopping"},
    {"name": "Zeon Charging - Nexus Koramangala", "lat": 12.9350, "lon": 77.6180, "city": "Bengaluru", "state": "Karnataka", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.50, "amenities": "Restrooms, Mall, Dining, Entertainment"},

    # Vellore -> Tirupati Corridor (NH 40 / NH 234: Katpadi -> Chittoor -> Kanipakam -> Tirupati)
    {"name": "Tata Power - Chittoor Highway Fast Hub", "lat": 13.2200, "lon": 79.1020, "city": "Chittoor", "state": "Andhra Pradesh", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 4, "connectors": "CCS2, Type 2", "price": 19.50, "amenities": "Restrooms, Dining, Snacks"},
    {"name": "ChargeZone - Kanipakam Temple Junction Hub", "lat": 13.2850, "lon": 79.1550, "city": "Chittoor", "state": "Andhra Pradesh", "country": "India", "operator": "ChargeZone", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 20.00, "amenities": "Restrooms, Vegetarian Food, Tea"},
    {"name": "Zeon Charging - Tirupati Alipiri Foothills Hub", "lat": 13.6340, "lon": 79.4120, "city": "Tirupati", "state": "Andhra Pradesh", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Temple Pilgrim Center, Dining, Hotel"},
    {"name": "Tata Power - Tirupati Airport Road EV Station", "lat": 13.6260, "lon": 79.4350, "city": "Tirupati", "state": "Andhra Pradesh", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 20.00, "amenities": "Restrooms, Dining, Coffee"},

    # Vellore -> Pondicherry Corridor (NH 38 / NH 32: Arani -> Chetpet -> Gingee -> Tindivanam -> Pondicherry)
    {"name": "Tata Power - Arani Bypass Fast Charger", "lat": 12.6710, "lon": 79.2880, "city": "Arani", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 19.50, "amenities": "Restrooms, Dining, Silk Stores"},
    {"name": "Zeon Charging - Tindivanam Highway Junction", "lat": 12.2350, "lon": 79.6540, "city": "Tindivanam", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Highway Restaurant, Filter Coffee"},
    {"name": "Relux - Pondicherry Beach Promenade Hub", "lat": 11.9360, "lon": 79.8320, "city": "Pondicherry", "state": "Puducherry", "country": "India", "operator": "Relux Electric", "power_kw": 60.0, "ports": 4, "connectors": "CCS2, Type 2", "price": 20.00, "amenities": "Restrooms, French Quarter Cafes, Beach View"},
    {"name": "Jio-bp pulse - ECR Coastal Fast Charge", "lat": 11.9540, "lon": 79.8180, "city": "Pondicherry", "state": "Puducherry", "country": "India", "operator": "Jio-bp pulse", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.50, "amenities": "Restrooms, Coastal Resort, Dining"},

    # Tamil Nadu & National Corridors (Salem, Coimbatore, Madurai, Trichy, Hyderabad, Mumbai, Delhi)
    {"name": "Zeon Charging - Salem Bypass Fast Hub", "lat": 11.6680, "lon": 78.1420, "city": "Salem", "state": "Tamil Nadu", "country": "India", "operator": "Zeon Charging", "power_kw": 120.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Restaurant, Coffee"},
    {"name": "Tata Power - Coimbatore Avinashi Road", "lat": 11.0210, "lon": 76.9620, "city": "Coimbatore", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 6, "connectors": "CCS2, Type 2", "price": 20.00, "amenities": "Restrooms, Dining, Shopping"},
    {"name": "ChargeZone - Madurai Ring Road Fast Plaza", "lat": 9.9320, "lon": 78.1250, "city": "Madurai", "state": "Tamil Nadu", "country": "India", "operator": "ChargeZone", "power_kw": 120.0, "ports": 6, "connectors": "CCS2", "price": 20.50, "amenities": "Restrooms, Temple Tourism Center, Dining"},
    {"name": "Tata Power - Trichy Junction Hub", "lat": 10.7930, "lon": 78.7080, "city": "Tiruchirappalli", "state": "Tamil Nadu", "country": "India", "operator": "Tata Power", "power_kw": 60.0, "ports": 4, "connectors": "CCS2", "price": 19.50, "amenities": "Restrooms, Dining, Hotel"},
    {"name": "Tata Power - Gachibowli Tech Hub, Hyderabad", "lat": 17.4400, "lon": 78.3480, "city": "Hyderabad", "state": "Telangana", "country": "India", "operator": "Tata Power", "power_kw": 120.0, "ports": 8, "connectors": "CCS2, Type 2", "price": 21.00, "amenities": "Restrooms, Tech Park Dining, WiFi"},
    {"name": "Jio-bp pulse - Mumbai-Pune Expressway Hub", "lat": 18.7540, "lon": 73.4120, "city": "Lonavala", "state": "Maharashtra", "country": "India", "operator": "Jio-bp pulse", "power_kw": 150.0, "ports": 12, "connectors": "CCS2, Type 2", "price": 22.00, "amenities": "Restrooms, Food Court, Coffee, Rest Area"},
    {"name": "Statiq - Cyber Hub, Gurugram (Delhi NCR)", "lat": 28.4950, "lon": 77.0890, "city": "Gurugram", "state": "Haryana", "country": "India", "operator": "Statiq", "power_kw": 150.0, "ports": 10, "connectors": "CCS2, Type 2", "price": 22.00, "amenities": "Restrooms, Cyber Hub Dining, Entertainment"},

    # Key International Hubs (Preserved for global test routes)
    {"name": "Kettleman City Bravo Farms Mega Supercharger", "lat": 35.9868, "lon": -119.9575, "city": "Kettleman City", "state": "CA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 96, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Dining, Lounge, Coffee"},
    {"name": "Kettleman City Electrify America Hub", "lat": 35.9882, "lon": -119.9592, "city": "Kettleman City", "state": "CA", "country": "US", "operator": "Electrify America", "power_kw": 350.0, "ports": 12, "connectors": "CCS, CHAdeMO", "price": 0.42, "amenities": "Restrooms, Fast Food, Coffee"},
    {"name": "Harris Ranch Inn Supercharger", "lat": 36.2514, "lon": -120.2378, "city": "Coalinga", "state": "CA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 80, "connectors": "NACS, CCS", "price": 0.35, "amenities": "Restrooms, Dining, Hotel"},
    {"name": "Tejon Ranch / Outlets Supercharger", "lat": 34.9867, "lon": -118.9442, "city": "Arvin", "state": "CA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 48, "connectors": "NACS, CCS", "price": 0.36, "amenities": "Restrooms, Dining, Outlets"},
    {"name": "Downtown Los Angeles Supercharger", "lat": 34.0488, "lon": -118.2518, "city": "Los Angeles", "state": "CA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.42, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "San Francisco - SOMA Supercharger", "lat": 37.7785, "lon": -122.4056, "city": "San Francisco", "state": "CA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.45, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Oakland Bay Bridge Fast Hub", "lat": 37.8282, "lon": -122.2891, "city": "Oakland", "state": "CA", "country": "US", "operator": "EVgo", "power_kw": 350.0, "ports": 10, "connectors": "CCS, NACS", "price": 0.42, "amenities": "Restrooms, Dining"},
    {"name": "Seattle Downtown Supercharger", "lat": 47.6062, "lon": -122.3321, "city": "Seattle", "state": "WA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 20, "connectors": "NACS, CCS", "price": 0.42, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Portland Pearl District Supercharger", "lat": 45.5231, "lon": -122.6765, "city": "Portland", "state": "OR", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Dining, Coffee"},
    {"name": "Centralia Factory Outlets Supercharger", "lat": 46.7262, "lon": -122.9771, "city": "Centralia", "state": "WA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "NACS, CCS", "price": 0.34, "amenities": "Restrooms, Shopping, Dining"},
    {"name": "Barstow EVgo High Desert Hub", "lat": 34.8986, "lon": -117.0228, "city": "Barstow", "state": "CA", "country": "US", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.41, "amenities": "Restrooms, Dining, Fuel"},
    {"name": "Baker - World Tallest Thermometer Supercharger", "lat": 35.2638, "lon": -116.0747, "city": "Baker", "state": "CA", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 40, "connectors": "NACS, CCS", "price": 0.38, "amenities": "Restrooms, Fast Food, Fuel"},
    {"name": "Las Vegas South Strip Supercharger", "lat": 36.0612, "lon": -115.1728, "city": "Las Vegas", "state": "NV", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 36, "connectors": "NACS, CCS", "price": 0.39, "amenities": "Restrooms, Dining, Casino"},
    {"name": "Stamford Town Center Fast Hub", "lat": 41.0534, "lon": -73.5387, "city": "Stamford", "state": "CT", "country": "US", "operator": "EVgo", "power_kw": 350.0, "ports": 8, "connectors": "CCS, NACS", "price": 0.43, "amenities": "Restrooms, Mall, Dining"},
    {"name": "Boston Seaport Fast Hub", "lat": 42.3519, "lon": -71.0428, "city": "Boston", "state": "MA", "country": "US", "operator": "Electrify America", "power_kw": 350.0, "ports": 10, "connectors": "CCS, CHAdeMO", "price": 0.45, "amenities": "Restrooms, Dining, Seaport"},
    {"name": "Katy Mills Supercharger", "lat": 29.7719, "lon": -95.8089, "city": "Katy", "state": "TX", "country": "US", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 24, "connectors": "NACS, CCS", "price": 0.31, "amenities": "Restrooms, Dining"},
    {"name": "London Stratford Supercharger", "lat": 51.5430, "lon": -0.0072, "city": "London", "country": "GB", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "CCS2, Type 2", "price": 0.45, "amenities": "Restrooms, Westfield, Dining"},
    {"name": "Ionity - Milton Keynes Motorway Services (M1)", "lat": 52.0720, "lon": -0.7300, "city": "Milton Keynes", "country": "GB", "operator": "Ionity", "power_kw": 350.0, "ports": 12, "connectors": "CCS2, Type 2", "price": 0.52, "amenities": "Restrooms, Costa Coffee, Waitrose, Burger King"},
    {"name": "Gridserve - Rugby Motorway Services Super Hub (M6)", "lat": 52.3780, "lon": -1.2320, "city": "Rugby", "country": "GB", "operator": "Gridserve", "power_kw": 350.0, "ports": 24, "connectors": "CCS2, Type 2, CHAdeMO", "price": 0.48, "amenities": "Restrooms, Greggs, Costa, M&S, EV Lounge"},
    {"name": "Gridserve - Moto Keele Services (M6 Northbound)", "lat": 52.9980, "lon": -2.2850, "city": "Keele", "country": "GB", "operator": "Gridserve", "power_kw": 350.0, "ports": 12, "connectors": "CCS2, Type 2", "price": 0.48, "amenities": "Restrooms, Starbucks, KFC, WHSmith"},
    {"name": "Tesla Supercharger - Manchester Trafford Centre", "lat": 53.4670, "lon": -2.3480, "city": "Manchester", "country": "GB", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 18, "connectors": "CCS2, Type 2", "price": 0.44, "amenities": "Restrooms, Mall, Dining, Cinema"},
    {"name": "ENEOS Charge Plus - Shizuoka Highway Hub", "lat": 34.9750, "lon": 138.3820, "city": "Shizuoka", "country": "Japan", "operator": "ENEOS Charge Plus", "power_kw": 150.0, "ports": 8, "connectors": "CHAdeMO", "price": 0.35, "amenities": "Restrooms, Ramen, Snacks"},
    {"name": "Tesla Supercharger - Hamamatsu Service Area", "lat": 34.7820, "lon": 137.7260, "city": "Hamamatsu", "country": "Japan", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 12, "connectors": "Tesla, CHAdeMO", "price": 0.38, "amenities": "Restrooms, Dining, Gyoza Food Court"},
    {"name": "Paris Porte de Versailles Supercharger", "lat": 48.8322, "lon": 2.2886, "city": "Paris", "country": "FR", "operator": "Tesla Supercharger", "power_kw": 250.0, "ports": 16, "connectors": "CCS2, Type 2", "price": 0.46, "amenities": "Restrooms, Dining"}
]

def seed_database_if_empty(db: Session, force_reseed: bool = False) -> int:
    """
    Populate SQLite database with realistic EV charging stations.
    Returns count of total seeded stations.
    """
    count = db.query(ChargingStation).count()
    # Check if Indian stations are already present
    indian_count = db.query(ChargingStation).filter(ChargingStation.country == "India").count()

    if count > 0 and indian_count >= 20 and not force_reseed:
        return count

    # Clean and re-seed if missing Indian stations
    db.query(ChargingStation).delete()
    db.commit()

    stations = []
    for item in STATION_SEED_DATA:
        station = ChargingStation(
            name=item["name"],
            latitude=item["lat"],
            longitude=item["lon"],
            address=item.get("address", f"{item['name']}, {item.get('city', '')}"),
            city=item.get("city", "Highway Stop"),
            state=item.get("state", ""),
            country=item.get("country", "India"),
            operator=item["operator"],
            power_kw=item["power_kw"],
            total_ports=item.get("ports", 6),
            available_ports=max(2, int(item.get("ports", 6) * 0.75)),
            connector_types=item.get("connectors", "CCS2, Type 2"),
            price_per_kwh=item.get("price", 20.00),
            amenities=item.get("amenities", "Restrooms, Dining, Coffee"),
            is_operational=True
        )
        stations.append(station)

    db.add_all(stations)
    db.commit()
    return len(stations)
