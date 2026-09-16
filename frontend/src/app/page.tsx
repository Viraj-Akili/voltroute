"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { Header } from "../components/Header";
import { RoutePlannerForm } from "../components/RoutePlannerForm";
import { RouteSummaryCard } from "../components/RouteSummaryCard";
import { BatteryProfileChart } from "../components/BatteryProfileChart";
import { ItineraryTimeline } from "../components/ItineraryTimeline";
import { DemoRoutesModal } from "../components/DemoRoutesModal";
import {
  RouteRequest,
  RouteResponse,
  VehiclePreset,
  StationResponse,
} from "../lib/types";
import {
  checkHealth,
  getVehiclePresets,
  planRoute,
  getStations,
} from "../lib/api";
import { Zap, AlertCircle, Sparkles, MapPin, Compass } from "lucide-react";

// Client-side only Leaflet map
const MapComponent = dynamic(
  () => import("../components/MapComponent").then((mod) => mod.MapComponent),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full min-h-[420px] lg:min-h-[580px] rounded-2xl glass-panel border border-white/10 flex items-center justify-center space-x-3 text-volt-400">
        <div className="w-6 h-6 border-2 border-volt-400 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-sm font-semibold tracking-wide">
          Loading OpenStreetMap & Stations...
        </span>
      </div>
    ),
  }
);

export default function Home() {
  const [presets, setPresets] = useState<VehiclePreset[]>([]);
  const [routeData, setRouteData] = useState<RouteResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<"online" | "offline" | "checking">("checking");
  const [stationCount, setStationCount] = useState<number>(0);
  const [isDemoModalOpen, setIsDemoModalOpen] = useState<boolean>(false);
  const [selectedStopIndex, setSelectedStopIndex] = useState<number | null>(null);
  const [formInitialValues, setFormInitialValues] = useState<Partial<RouteRequest>>({});

  // Initialize and load default route
  useEffect(() => {
    async function init() {
      // 1. Check health
      const health = await checkHealth();
      if (health.status === "ok") {
        setBackendStatus("online");
        setStationCount(health.charging_stations_loaded || 0);
      } else {
        setBackendStatus("offline");
      }

      // 2. Fetch vehicle presets
      const fetchedPresets = await getVehiclePresets();
      setPresets(fetchedPresets);

      // 3. Auto-calculate initial demo route (LA to SF) for instant WOW factor
      handleCalculateRoute({
        start_location: "Los Angeles, CA",
        destination: "San Francisco, CA",
        current_battery_pct: 70,
        battery_capacity_kwh: 75.0,
        vehicle_efficiency_wh_per_km: 150.0,
        vehicle_model: "Tesla Model 3 Long Range",
        min_stop_soc_pct: 10.0,
        target_dest_soc_pct: 15.0,
        max_charge_soc_pct: 80.0,
      });
    }

    init();
  }, []);

  const handleCalculateRoute = async (request: RouteRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await planRoute(request);
      setRouteData(response);
      setBackendStatus("online");
    } catch (err: any) {
      console.error("Route planning error:", err);
      setError(
        err.message || "Failed to calculate optimal EV route. Please check the locations or backend service."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDemoRoute = (
    start: string,
    dest: string,
    batteryPct: number,
    vehicleModel: string
  ) => {
    const matchedPreset = presets.find((p) => p.name === vehicleModel);
    const capacity = matchedPreset?.battery_capacity_kwh || 75;
    const eff = matchedPreset?.efficiency_wh_per_km || 160;

    const request: RouteRequest = {
      start_location: start,
      destination: dest,
      current_battery_pct: batteryPct,
      battery_capacity_kwh: capacity,
      vehicle_efficiency_wh_per_km: eff,
      vehicle_model: vehicleModel,
      min_stop_soc_pct: 10,
      target_dest_soc_pct: 15,
      max_charge_soc_pct: 80,
    };

    setFormInitialValues(request);
    handleCalculateRoute(request);
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar Header */}
      <Header
        backendStatus={backendStatus}
        stationCount={stationCount}
        onOpenDemoModal={() => setIsDemoModalOpen(true)}
      />

      {/* Main Content Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
        {/* Error Alert if any */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start space-x-3 animate-fadeIn">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <h5 className="font-bold">Route Calculation Error</h5>
              <p className="text-xs text-rose-200 mt-0.5">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-xs text-rose-400 hover:text-white font-bold"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Dashboard Grid: Left Form & Itinerary / Right Interactive Map */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Form & Route Results (5 cols on Desktop) */}
          <div className="lg:col-span-5 space-y-6">
            {/* Input Parameters Form */}
            <RoutePlannerForm
              presets={presets}
              loading={loading}
              onPlanRoute={handleCalculateRoute}
              initialValues={formInitialValues}
            />

            {/* Trip Results Section (rendered once route is available) */}
            {routeData && (
              <div className="space-y-6 animate-fadeIn">
                {/* Trip Summary Card */}
                <RouteSummaryCard
                  summary={routeData.summary}
                  origin={routeData.origin}
                  destination={routeData.destination}
                />

                {/* Battery SOC Graph */}
                <BatteryProfileChart
                  profile={routeData.battery_profile}
                  totalDistanceKm={routeData.summary.total_distance_km}
                />

                {/* Turn-by-turn Leg & Stop Timeline */}
                <ItineraryTimeline
                  origin={routeData.origin}
                  destination={routeData.destination}
                  legs={routeData.legs}
                  stops={routeData.stops}
                  initialSoc={routeData.summary.initial_battery_pct}
                />
              </div>
            )}
          </div>

          {/* Right Column: Sticky Interactive Leaflet Map (7 cols on Desktop) */}
          <div className="lg:col-span-7 lg:sticky lg:top-20 space-y-4">
            <MapComponent
              routeData={routeData}
              allCorridorStations={routeData?.candidate_stations || []}
              selectedStopIndex={selectedStopIndex}
              onSelectStop={(idx) => setSelectedStopIndex(idx)}
            />
          </div>
        </div>
      </main>

      {/* Demo Routes Selection Modal */}
      <DemoRoutesModal
        isOpen={isDemoModalOpen}
        onClose={() => setIsDemoModalOpen(false)}
        onSelectRoute={handleSelectDemoRoute}
      />

      {/* Footer */}
      <footer className="w-full border-t border-white/5 py-4 px-6 text-center text-xs text-slate-500">
        <p>
          VoltRoute — Intelligent EV Route Planner • Powered by FastAPI & Next.js • OpenStreetMap & OSRM
        </p>
      </footer>
    </div>
  );
}
