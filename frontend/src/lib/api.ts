import { RouteRequest, RouteResponse, VehiclePreset, StationResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkHealth(): Promise<{ status: string; charging_stations_loaded?: number }> {
  try {
    const res = await fetch(`${API_BASE}/health`, { cache: "no-store" });
    if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Backend /health unreachable:", err);
    return { status: "offline", charging_stations_loaded: 0 };
  }
}

export async function getVehiclePresets(): Promise<VehiclePreset[]> {
  try {
    const res = await fetch(`${API_BASE}/api/vehicles/presets`, { cache: "force-cache" });
    if (!res.ok) throw new Error(`Presets failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed fetching presets from API, using fallback presets:", err);
    return [
      {
        id: "tesla-model-3-lr",
        name: "Tesla Model 3 Long Range",
        make: "Tesla",
        model: "Model 3 LR",
        year: 2024,
        battery_capacity_kwh: 75.0,
        efficiency_wh_per_km: 150.0,
        max_charge_rate_kw: 250.0,
        supported_connectors: ["NACS", "CCS"],
        description: "High efficiency aero sedan with 250kW Supercharging."
      },
      {
        id: "tesla-model-y-lr",
        name: "Tesla Model Y Long Range",
        make: "Tesla",
        model: "Model Y LR",
        year: 2024,
        battery_capacity_kwh: 75.0,
        efficiency_wh_per_km: 168.0,
        max_charge_rate_kw: 250.0,
        supported_connectors: ["NACS", "CCS"],
        description: "The world's best-selling electric crossover."
      },
      {
        id: "hyundai-ioniq-5",
        name: "Hyundai Ioniq 5 AWD (77.4 kWh)",
        make: "Hyundai",
        model: "Ioniq 5",
        year: 2024,
        battery_capacity_kwh: 77.4,
        efficiency_wh_per_km: 182.0,
        max_charge_rate_kw: 235.0,
        supported_connectors: ["CCS", "NACS"],
        description: "800V ultra-fast architecture (10% to 80% in ~18 mins)."
      },
      {
        id: "ford-mustang-mach-e",
        name: "Ford Mustang Mach-E Extended Range",
        make: "Ford",
        model: "Mustang Mach-E ER",
        year: 2024,
        battery_capacity_kwh: 91.0,
        efficiency_wh_per_km: 195.0,
        max_charge_rate_kw: 150.0,
        supported_connectors: ["CCS", "NACS"],
        description: "Spacious performance SUV with long-range battery."
      },
      {
        id: "porsche-taycan",
        name: "Porsche Taycan Performance Battery Plus",
        make: "Porsche",
        model: "Taycan Plus",
        year: 2024,
        battery_capacity_kwh: 93.4,
        efficiency_wh_per_km: 210.0,
        max_charge_rate_kw: 270.0,
        supported_connectors: ["CCS", "Type 2"],
        description: "800V sports EV with sustained 270kW charging."
      },
      {
        id: "chevrolet-bolt-ev",
        name: "Chevrolet Bolt EV",
        make: "Chevrolet",
        model: "Bolt EV",
        year: 2023,
        battery_capacity_kwh: 65.0,
        efficiency_wh_per_km: 160.0,
        max_charge_rate_kw: 55.0,
        supported_connectors: ["CCS"],
        description: "Affordable compact EV with 55kW DC fast charging."
      }
    ];
  }
}

export async function planRoute(request: RouteRequest): Promise<RouteResponse> {
  const res = await fetch(`${API_BASE}/api/route`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    let errorMsg = `Server returned status ${res.status}`;
    try {
      const errJson = await res.json();
      if (errJson.detail) errorMsg = errJson.detail;
    } catch {
      // ignore json parse error
    }
    throw new Error(errorMsg);
  }

  return await res.json();
}

export async function getStations(limit: number = 250): Promise<StationResponse[]> {
  try {
    const res = await fetch(`${API_BASE}/api/stations?limit=${limit}`);
    if (!res.ok) throw new Error(`Stations fetch failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed fetching stations:", err);
    return [];
  }
}
