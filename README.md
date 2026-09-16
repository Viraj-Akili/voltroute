# ⚡ VoltRoute — Intelligent EV Route Planner

> **Production-grade full-stack EV route planning web application that simulates real-world battery consumption, projects real charging corridors, and optimizes fast-charging stops using Google Maps Platform.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2+-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Google Maps Platform](https://img.shields.io/badge/Google%20Maps-Platform-4285F4.svg?logo=googlemaps&logoColor=white)](https://developers.google.com/maps)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://python.org)

---

## 📌 Problem & Project Overview

Planning long-distance electric vehicle (EV) road trips requires balancing multiple real-world factors:
1. **Battery Capacity & State of Charge (SOC %)**: Knowing when the battery will reach critical buffer levels.
2. **Vehicle Efficiency & Consumption**: Variations in Wh/km across vehicle aerodynamics and highway speeds.
3. **Charging Speed Curves**: Batteries charge significantly faster between 10% and 50% than above 80% (non-linear taper curve).
4. **Charging Station Placement & Detour**: Finding high-power DC fast chargers (50kW–350kW) along highway corridors without excessive detour off the route.

**VoltRoute** delivers a production-grade experience with **Google Maps Platform** for interactive mapping, Google Places Autocomplete for worldwide and Indian location search, live corridor charging station visualization, and a physics-backed optimization engine tailored for Indian and global EV journeys.

---

## 🚀 Key Features

- **🗺️ Google Maps Platform Integration**:
  - Full Google Maps vector map with dynamic light and dark theme styling.
  - **Google Places Autocomplete** with instant geocoding, recent history, and live worldwide search.
  - Smooth auto-fitting bounds to route polylines and charging points.
  - Interactive custom SVG markers: 🔵 Origin, 🔴 Destination, 🟢 Recommended Charging Stops, and 🟡 Corridor Fast Chargers.
  - **One-Click Navigation**: "Navigate in Google Maps" links for every charging stop and candidate station.
- **⚡ Physics-Based EV Battery Modeling & Multi-Objective Optimization**:
  - Simulates dynamic energy consumption based on usable capacity (kWh), vehicle efficiency (Wh/km), and real-world highway overhead factors.
  - Realistic non-linear charging curve simulation (peak power below 50% SOC, 72% power up to 80% SOC, and heavy taper above 80% to protect cell health).
  - **3 Optimization Modes**: `Fastest` (prioritizes high-kW chargers and low trip time), `Cheapest` (prioritizes low ₹/kWh rates), and `Fewest Stops` (maximizes leg distance).
- **🇮🇳 India & Global Corridor Focus**:
  - Preloaded with major Indian EV charging networks (Tata Power EZ Charge, Zeon Charging, Jio-bp pulse, Ather Grid, ChargeZone, Statiq, Shell Recharge) across Tamil Nadu, Karnataka, Andhra Pradesh, and golden quadrilateral highways.
  - Preloaded EV presets: *Tata Nexon EV LR, Tata Punch EV, MG ZS EV, Mahindra XUV400, Hyundai Ioniq 5, BYD Atto 3, Tesla Model 3 LR, BMW i4*.
- **📊 Interactive Battery SOC Profile Chart**:
  - Visual SVG graph plotting battery percentage along the entire trip distance with elevation buffer guides.
- **📋 Turn-by-Turn Leg & Stop Itinerary**:
  - Detailed leg-by-leg timeline displaying departure/arrival SOC %, energy consumed (kWh), charging duration (minutes), plug types (CCS-2, Type 2, GB/T, NACS), estimated charging cost in ₹ / $, and amenities.
- **✨ 1-Click Popular Road Trips**:
  - Instant testing with curated routes: *Vellore ➔ Chennai*, *Vellore ➔ Bengaluru*, *Vellore ➔ Tirupati*, *Chennai ➔ Bengaluru*, *Vellore ➔ Pondicherry*, and *London ➔ Manchester*.

---

## 🧠 Optimization Algorithm & Math Model

The route planner implements a multi-stage optimization pipeline:

```
[Start & End Input] ➔ [Google Places / Coordinates] ➔ [Road Geometry & Polyline]
                                            │
                                            ▼
                    [Spatial Projection of Seeded & Corridor Stations]
                                            │
                                            ▼
                        [Direct Trip Feasibility Check]
                        /                             \
                (Can Reach Dest)               (Needs Charging)
                      /                                 \
          [Generate Direct Plan]               [Forward Search Loop]
                                                        │
                                            [Filter Reachable Stations]
                                                        │
                                            [Multi-Factor Strategy Scoring]
                                                        │
                                            [Simulate Non-Linear Charging]
                                                        │
                                            [Produce Stops & Itinerary]
```

### 1. Spatial Corridor Projection
Each candidate charging station in SQLite is projected onto the route polyline segments:
- Perpendicular distance from route line = $\text{Detour Distance (km)}$
- Cumulative distance from route start = $\text{Distance Along Route (km)}$
- Only stations within a 35 km detour buffer are considered.

### 2. Multi-Factor Candidate Scoring
When the vehicle battery approaches the safe buffer threshold (e.g. 10–15% SOC), reachable stations are evaluated with a composite scoring function adjusted by the chosen optimization mode:
$$\text{Score} = \text{Power Score} + \text{Depletion Window Score} + \text{Progress Score} - \text{Detour Penalty} - \text{Price Penalty}$$

### 3. Non-Linear Charging Physics Model
Charging duration is calculated across 5% incremental SOC slices using a piecewise power taper model:
- **$\text{SOC} < 50\%$**: $95\%$ of peak charger/vehicle power.
- **$50\% \le \text{SOC} < 80\%$**: $72\%$ of peak power.
- **$\text{SOC} \ge 80\%$**: $35\%$ of peak power (steep taper to prevent thermal degradation).

---

## 🛠️ Architecture & Tech Stack

```
voltroute/
├── backend/                  # Python FastAPI Backend
│   ├── app/
│   │   ├── config.py         # App settings & CORS
│   │   ├── database.py       # SQLite database & sessionmaker
│   │   ├── main.py           # FastAPI application entrypoint & lifespan
│   │   ├── data/
│   │   │   └── seed_stations.py # 200+ realistic EV fast charger records (India & Global)
│   │   ├── models/
│   │   │   └── station.py    # SQLAlchemy ChargingStation model
│   │   ├── routes/
│   │   │   └── route_api.py  # /route, /health, /api/stations, /api/vehicles
│   │   ├── schemas/
│   │   │   └── route.py      # Pydantic request/response schemas
│   │   └── services/
│   │       ├── geocoding.py  # Fast offline cache + OSM Nominatim
│   │       ├── routing.py    # Road geometry & Haversine projection
│   │       └── optimizer.py  # EV battery simulation & charging optimizer
│   ├── tests/
│   │   ├── test_api.py       # Pytest automated test suite
│   │   └── verify_routes.py  # Multi-route scenario verifier
│   ├── requirements.txt      # Python dependencies
│   └── render.yaml           # Render deployment configuration
│
├── frontend/                 # Next.js 14 Web Application
│   ├── src/
│   │   ├── app/
│   │   │   ├── globals.css   # Dark / Light theme & Google Maps styles
│   │   │   ├── layout.tsx    # HTML layout, font setup, & theme detector
│   │   │   └── page.tsx      # Responsive dashboard page with Google Maps APIProvider
│   │   ├── components/
│   │   │   ├── Header.tsx    # Navbar, theme toggle, and charging points toggle
│   │   │   ├── PlaceAutocompleteInput.tsx # Google Places Autocomplete component
│   │   │   ├── RoutePlannerForm.tsx # EV parameters & route planner form
│   │   │   ├── RouteSummaryCard.tsx # Trip metrics & cost card
│   │   │   ├── BatteryProfileChart.tsx # SVG Battery SOC chart
│   │   │   ├── ItineraryTimeline.tsx   # Step-by-step itinerary with Maps links
│   │   │   ├── MapComponent.tsx        # Google Maps Platform interactive map
│   │   │   └── DemoRoutesModal.tsx     # Popular trips selector
│   │   └── lib/
│   │       ├── api.ts        # API client
│   │       └── types.ts      # TypeScript interfaces
│   ├── package.json          # Node dependencies (@vis.gl/react-google-maps)
│   ├── tailwind.config.js    # Design tokens
│   └── tsconfig.json         # TypeScript configuration
│
├── .gitignore
└── README.md
```

---

## 💻 Local Setup & Development

### 1. Prerequisites
- **Node.js** 18.x or 20.x+
- **Python** 3.10 or 3.11+
- **Google Maps Platform API Key** (optional in dev; falls back to demo key)

---

### 2. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# (Optional) Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server (starts at http://localhost:8000)
python -m uvicorn app.main:app --reload --port 8000
```

- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

#### Run Automated Tests:
```bash
cd backend
python -m pytest tests/test_api.py -v
python tests/verify_routes.py
```

---

### 3. Frontend Setup (Next.js)

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Copy environment file
cp .env.example .env.local
# Set NEXT_PUBLIC_GOOGLE_MAPS_API_KEY in .env.local

# Install dependencies
npm install

# Start development server (starts at http://localhost:3000)
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

---

## 📡 API Reference

### `POST /route` or `POST /api/route`
Calculate an optimal EV route and recommended charging stops.

**Request Payload:**
```json
{
  "start_location": "Los Angeles, CA",
  "destination": "San Francisco, CA",
  "current_battery_pct": 70.0,
  "battery_capacity_kwh": 75.0,
  "vehicle_efficiency_wh_per_km": 150.0,
  "vehicle_model": "Tesla Model 3 Long Range",
  "min_stop_soc_pct": 10.0,
  "target_dest_soc_pct": 15.0,
  "max_charge_soc_pct": 80.0
}
```

**Response Payload (Summary Snippet):**
```json
{
  "summary": {
    "total_distance_km": 614.6,
    "total_distance_miles": 381.9,
    "total_drive_time_min": 427.7,
    "total_charge_time_min": 22.4,
    "total_trip_time_min": 450.1,
    "initial_battery_pct": 70.0,
    "final_battery_pct": 30.2,
    "total_energy_consumed_kwh": 95.9,
    "total_energy_charged_kwh": 51.2,
    "total_charging_cost_usd": 27.74,
    "co2_saved_kg": 118.0,
    "num_stops": 2,
    "is_feasible": true,
    "status_message": "Optimal EV route computed successfully."
  },
  "origin": { "name": "Los Angeles, CA", "latitude": 34.0522, "longitude": -118.2437 },
  "destination": { "name": "San Francisco, CA", "latitude": 37.7749, "longitude": -122.4194 },
  "stops": [
    {
      "stop_index": 1,
      "station": {
        "id": 17,
        "name": "Kettleman City Electrify America Hub",
        "operator": "Electrify America",
        "power_kw": 350.0,
        "connector_types": ["CCS", "CHAdeMO"],
        "price_per_kwh": 0.42,
        "amenities": ["Restrooms", "Fast Food", "Coffee"]
      },
      "arrival_soc_pct": 11.9,
      "departure_soc_pct": 80.0,
      "energy_added_kwh": 51.08,
      "charge_duration_min": 16.6,
      "estimated_cost_usd": 21.45
    }
  ]
}
```

### `GET /api/vehicles/presets`
Returns all preconfigured EV vehicle models and battery specifications.

### `GET /api/stations`
Query charging stations with optional spatial radius filter (`lat`, `lon`, `radius_km`).

### `GET /health`
Service health check and loaded database station count.

---

## 🚢 Deployment Guide

### Deploying Backend to Render
1. Push this repository to GitHub.
2. In [Render Dashboard](https://dashboard.render.com), click **New +** ➔ **Blueprint** and select this repository.
3. Render reads `backend/render.yaml` and deploys the web service automatically.
4. Environment variables handled automatically:
   - `PORT`: (Provided by Render)
   - `DATABASE_URL`: `sqlite:///./charging_stations.db`
   - `OSRM_BASE_URL`: `https://router.project-osrm.org`

### Deploying Frontend to Vercel
1. In [Vercel Dashboard](https://vercel.com), click **Add New** ➔ **Project** and import this repository.
2. Set **Root Directory** to `frontend`.
3. Set Environment Variable:
   - `NEXT_PUBLIC_API_URL`: URL of your deployed Render backend (e.g. `https://voltroute-backend.onrender.com`).
4. Click **Deploy**.

---

## 🔮 Future Improvements

1. **Elevation & Regenerative Braking**: Integrate digital elevation models (DEM) to simulate energy recovered through regenerative braking on mountain descents and increased consumption during steep climbs.
2. **Ambient Temperature & HVAC Simulation**: Dynamic adjustments for extreme cold (sub-zero capacity loss and battery preconditioning) and hot climates (cabin A/C draw).
3. **Live OCPI / Open Charge Point Interface Integration**: Real-time occupancy status (e.g. 6/8 stalls available) and live queue time predictions.
4. **Time-of-Use (TOU) Electricity Pricing**: Optimizing stops to take advantage of off-peak charging utility rates.

---

## ⚖️ License
MIT License. Built for evaluation.
