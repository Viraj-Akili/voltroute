import { RouteRequest, RouteResponse, VehiclePreset, StationResponse } from "./types";

const getApiBaseUrl = (): string => {
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl && envUrl.trim().length > 0) {
    return envUrl.trim().replace(/\/+$/, "");
  }
  return "http://localhost:8000";
};

export async function checkHealth(): Promise<{ status: string; charging_stations_loaded?: number }> {
  try {
    const API_URL = getApiBaseUrl();
    const res = await fetch(`${API_URL}/health`, { cache: "no-store" });
    if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Backend /health unreachable:", err);
    return { status: "offline", charging_stations_loaded: 0 };
  }
}

export async function getVehiclePresets(): Promise<VehiclePreset[]> {
  try {
    const API_URL = getApiBaseUrl();
    const res = await fetch(`${API_URL}/api/vehicles/presets`, { cache: "force-cache" });
    if (!res.ok) throw new Error(`Presets failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed fetching presets from API, using fallback presets:", err);
    return [
      {
        id: "tata-nexon-ev-lr",
        name: "Tata Nexon EV Long Range",
        make: "Tata",
        model: "Nexon EV LR",
        year: 2024,
        battery_capacity_kwh: 40.5,
        efficiency_wh_per_km: 138.0,
        max_charge_rate_kw: 50.0,
        supported_connectors: ["CCS2", "CCS", "Type 2"],
        description: "India's most popular electric SUV with 40.5 kWh LFP pack and real-world range of ~280 km."
      },
      {
        id: "tata-punch-ev-lr",
        name: "Tata Punch EV Long Range",
        make: "Tata",
        model: "Punch EV LR",
        year: 2024,
        battery_capacity_kwh: 35.0,
        efficiency_wh_per_km: 128.0,
        max_charge_rate_kw: 50.0,
        supported_connectors: ["CCS2", "CCS", "Type 2"],
        description: "Compact electric SUV built on Tata's pure EV acti.ev platform."
      },
      {
        id: "mg-zs-ev",
        name: "MG ZS EV",
        make: "MG",
        model: "ZS EV",
        year: 2024,
        battery_capacity_kwh: 50.3,
        efficiency_wh_per_km: 150.0,
        max_charge_rate_kw: 80.0,
        supported_connectors: ["CCS2", "CCS", "Type 2"],
        description: "Premium electric crossover with 50.3 kWh battery and 80kW DC fast charging."
      },
      {
        id: "mahindra-xuv400",
        name: "Mahindra XUV400 EV",
        make: "Mahindra",
        model: "XUV400 EL Pro",
        year: 2024,
        battery_capacity_kwh: 39.4,
        efficiency_wh_per_km: 145.0,
        max_charge_rate_kw: 50.0,
        supported_connectors: ["CCS2", "CCS", "Type 2"],
        description: "Spacious electric SUV from Mahindra with fast acceleration and 39.4 kWh capacity."
      },
      {
        id: "tata-tiago-ev",
        name: "Tata Tiago EV Long Range",
        make: "Tata",
        model: "Tiago EV LR",
        year: 2024,
        battery_capacity_kwh: 24.0,
        efficiency_wh_per_km: 115.0,
        max_charge_rate_kw: 30.0,
        supported_connectors: ["CCS2", "CCS", "Type 2"],
        description: "Efficient city EV hatchback with 24 kWh pack for intercity commutes."
      },
      {
        id: "hyundai-ioniq-5-in",
        name: "Hyundai Ioniq 5 (72.6 kWh)",
        make: "Hyundai",
        model: "Ioniq 5",
        year: 2024,
        battery_capacity_kwh: 72.6,
        efficiency_wh_per_km: 165.0,
        max_charge_rate_kw: 235.0,
        supported_connectors: ["CCS2", "CCS", "Type 2"],
        description: "800V ultra-fast charging architecture capable of 10% to 80% charge in ~18 minutes."
      }
    ];
  }
}

export async function planRoute(request: RouteRequest): Promise<RouteResponse> {
  const API_URL = getApiBaseUrl();
  const res = await fetch(`${API_URL}/route`, {
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

export async function getStations(params: number | { limit?: number } = 250): Promise<StationResponse[]> {
  const limitVal = typeof params === "number" ? params : params?.limit || 250;
  try {
    const API_URL = getApiBaseUrl();
    const res = await fetch(`${API_URL}/api/stations?limit=${limitVal}`);
    if (!res.ok) throw new Error(`Stations fetch failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed fetching stations:", err);
    return [];
  }
}

export const getChargingStations = getStations;

