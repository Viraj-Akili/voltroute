export interface VehiclePreset {
  id: string;
  name: string;
  make: string;
  model: string;
  year: number;
  battery_capacity_kwh: number;
  efficiency_wh_per_km: number;
  max_charge_rate_kw: number;
  max_charging_power_kw?: number;
  supported_connectors: string[];
  description?: string;
}

export interface ResolvedLocation {
  name: string;
  latitude: number;
  longitude: number;
  formatted_address?: string;
  place_id?: string;
}

export interface StationResponse {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  operator: string;
  power_kw: number;
  total_ports: number;
  available_ports: number;
  connector_types: string[];
  price_per_kwh: number;
  amenities: string[];
  is_operational: boolean;
  detour_km?: number;
  place_id?: string;
}

export interface ChargingStop {
  stop_index: number;
  station: StationResponse;
  arrival_soc_pct: number;
  departure_soc_pct: number;
  energy_added_kwh: number;
  charge_duration_min: number;
  estimated_cost_usd: number;
  distance_from_start_km: number;
  distance_from_prev_stop_km: number;
}

export interface RouteLeg {
  leg_index: number;
  from_name: string;
  to_name: string;
  distance_km: number;
  duration_min: number;
  energy_used_kwh: number;
  energy_consumed_kwh?: number;
  start_soc_pct: number;
  start_battery_pct?: number;
  end_soc_pct: number;
  end_battery_pct?: number;
  polyline?: [number, number][];
}

export interface BatteryProfilePoint {
  distance_km: number;
  soc_pct: number;
  battery_pct?: number;
  location_name: string;
  event: "start" | "driving" | "arrival_at_charger" | "charged_at_charger" | "destination";
}

export interface TripSummary {
  total_distance_km: number;
  total_distance_miles: number;
  total_drive_time_min: number;
  total_charge_time_min: number;
  total_trip_time_min: number;
  initial_battery_pct: number;
  final_battery_pct: number;
  total_energy_consumed_kwh: number;
  total_energy_charged_kwh: number;
  total_charging_cost_usd: number;
  co2_saved_kg: number;
  num_stops: number;
  is_feasible: boolean;
  status_message: string;
}

export interface RouteRequest {
  start_location: string | { name?: string; lat?: number; lon?: number; place_id?: string };
  start_lat?: number;
  start_lng?: number;
  destination: string | { name?: string; lat?: number; lon?: number; place_id?: string };
  dest_lat?: number;
  dest_lng?: number;
  current_battery_pct: number;
  battery_capacity_kwh: number;
  vehicle_efficiency_wh_per_km: number;
  vehicle_model?: string;
  min_stop_soc_pct?: number;
  target_dest_soc_pct?: number;
  max_charge_soc_pct?: number;
  preferred_connectors?: string[];
  min_charger_power_kw?: number;
  optimization_mode?: "fastest" | "cheapest" | "fewest_stops";
}

export interface RouteResponse {
  summary: TripSummary;
  origin: ResolvedLocation;
  destination: ResolvedLocation;
  legs: RouteLeg[];
  stops: ChargingStop[];
  battery_profile: BatteryProfilePoint[];
  route_geometry: [number, number][];
  candidate_stations: StationResponse[];
}

// Convenient Aliases
export type RouteSummary = TripSummary;
export type ChargingStation = StationResponse;
export type RouteStop = ChargingStop;
export type RouteLocation = ResolvedLocation;

