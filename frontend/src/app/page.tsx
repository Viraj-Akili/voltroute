'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { APIProvider } from '@vis.gl/react-google-maps';
import Header from '../components/Header';
import RoutePlannerForm from '../components/RoutePlannerForm';
import RouteSummaryCard from '../components/RouteSummaryCard';
import ItineraryTimeline from '../components/ItineraryTimeline';
import BatteryProfileChart from '../components/BatteryProfileChart';
import MapComponent from '../components/MapComponent';
import CustomVehicleModal from '../components/CustomVehicleModal';
import DemoRoutesModal from '../components/DemoRoutesModal';
import { planRoute, getChargingStations } from '../lib/api';
import { RouteRequest, RouteResponse, ChargingStation, VehiclePreset } from '../lib/types';

export default function Home() {
  const [theme, setTheme] = useState<'light' | 'dark'>('dark');
  const [routeData, setRouteData] = useState<RouteResponse | null>(null);
  const [allStations, setAllStations] = useState<ChargingStation[]>([]);
  const [showAllChargingPoints, setShowAllChargingPoints] = useState(true);
  const [selectedStation, setSelectedStation] = useState<ChargingStation | null>(null);
  const [highlightedStopIndex, setHighlightedStopIndex] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isCustomVehicleModalOpen, setIsCustomVehicleModalOpen] = useState(false);
  const [isDemoModalOpen, setIsDemoModalOpen] = useState(false);
  const [customVehicles, setCustomVehicles] = useState<VehiclePreset[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [apiKeyMissing, setApiKeyMissing] = useState(false);

  const [formData, setFormData] = useState<RouteRequest>({
    start_location: 'Vellore, Tamil Nadu, India',
    start_lat: 12.9165,
    start_lng: 79.1325,
    destination: 'Chennai, Tamil Nadu, India',
    dest_lat: 13.0827,
    dest_lng: 80.2707,
    current_battery_pct: 70,
    battery_capacity_kwh: 40.5,
    vehicle_efficiency_wh_per_km: 138,
    vehicle_model: 'Tata Nexon EV Long Range',
    min_stop_soc_pct: 10,
    target_dest_soc_pct: 15,
    max_charge_soc_pct: 80,
    optimization_mode: 'fastest',
  });

  // Theme synchronization
  useEffect(() => {
    const savedTheme = localStorage.getItem('voltroute_theme') as 'light' | 'dark' | null;
    const initialTheme = savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    setTheme(initialTheme);
    if (initialTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const handleToggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('voltroute_theme', newTheme);
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  // Check Google Maps API Key
  const googleMapsApiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

  useEffect(() => {
    if (!googleMapsApiKey) {
      setApiKeyMissing(true);
    }
  }, [googleMapsApiKey]);

  // Load charging points along corridor
  const fetchAllChargingPoints = useCallback(async () => {
    try {
      const stations = await getChargingStations(150);
      setAllStations(stations);
    } catch (err) {
      console.warn('Could not load charging stations:', err);
    }
  }, []);

  useEffect(() => {
    fetchAllChargingPoints();
  }, [fetchAllChargingPoints]);

  // Friendly human error translator
  const formatFriendlyError = (rawError: any): string => {
    const text = (rawError?.response?.data?.detail || rawError?.message || String(rawError || '')).toLowerCase();
    
    if (text.includes('charging') || text.includes('infeasible') || text.includes('battery') || text.includes('reach')) {
      return "Charging data isn't available for this route or the vehicle cannot reach the destination with current battery levels. Try starting with a higher battery percentage.";
    }
    if (text.includes('location') || text.includes('geocode') || text.includes('route') || text.includes('not found') || text.includes('osrm')) {
      return "Couldn't calculate this route. Please check the locations and try again.";
    }
    return "Something went wrong. Please check your locations and try again.";
  };

  // Handle route calculation
  const handlePlanRoute = async (requestData: RouteRequest) => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const result = await planRoute(requestData);
      setRouteData(result);
      if (!result.summary.is_feasible) {
        setErrorMessage("Charging data isn't available for this route or the battery buffer cannot be met. Try increasing starting battery level.");
      }
    } catch (err: any) {
      console.error('Route calculation error:', err);
      setErrorMessage(formatFriendlyError(err));
    } finally {
      setIsLoading(false);
    }
  };

  // Initial calculation on load
  useEffect(() => {
    handlePlanRoute(formData);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Save custom vehicle from modal
  const handleSaveCustomVehicle = (vehicle: VehiclePreset) => {
    setCustomVehicles((prev) => [...prev, vehicle]);
    const updatedForm: RouteRequest = {
      ...formData,
      vehicle_model: vehicle.model,
      battery_capacity_kwh: vehicle.battery_capacity_kwh,
      vehicle_efficiency_wh_per_km: vehicle.efficiency_wh_per_km,
    };
    setFormData(updatedForm);
    handlePlanRoute(updatedForm);
  };

  return (
    <APIProvider apiKey={googleMapsApiKey} solutionChannel="gmp_git_agentskills_v1">
      <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
        <Header
          theme={theme}
          onToggleTheme={handleToggleTheme}
          onOpenDemoModal={() => setIsDemoModalOpen(true)}
        />

        <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">
          {/* Left Panel: Compact Planner & Itinerary */}
          <section
            aria-label="Trip Planner"
            className="w-full lg:w-[380px] xl:w-[410px] flex-shrink-0 flex flex-col h-auto lg:h-[calc(100vh-56px)] overflow-y-auto border-r border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 z-10 p-4 sm:p-5 space-y-4"
          >
            <RoutePlannerForm
              formData={formData}
              onChange={setFormData}
              onSubmit={handlePlanRoute}
              onOpenCustomVehicleModal={() => setIsCustomVehicleModalOpen(true)}
              isLoading={isLoading}
              customVehicles={customVehicles}
            />

            {/* Friendly Error Notice */}
            {errorMessage && (
              <div
                role="alert"
                className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-amber-900 dark:text-amber-200 text-xs leading-relaxed shadow-sm flex items-start gap-2.5"
              >
                <span className="text-base leading-none">⚠️</span>
                <span>{errorMessage}</span>
              </div>
            )}

            {/* Calculated Trip Itinerary */}
            {routeData && (
              <ItineraryTimeline
                legs={routeData.legs}
                stops={routeData.stops}
                origin={routeData.origin}
                destination={routeData.destination}
                onHoverStop={(idx) => setHighlightedStopIndex(idx)}
                onSelectStop={(stop) => setSelectedStation(stop.station)}
              />
            )}

            {/* Battery SOC Profile Chart */}
            {routeData && routeData.battery_profile && routeData.battery_profile.length > 0 && (
              <BatteryProfileChart
                profilePoints={routeData.battery_profile}
                stops={routeData.stops}
                initialPct={routeData.summary.initial_battery_pct}
                batteryCapacityKwh={formData.battery_capacity_kwh}
              />
            )}
          </section>

          {/* Right Panel: Hero Google Map */}
          <section aria-label="Interactive Map" className="flex-1 relative h-[520px] lg:h-[calc(100vh-56px)] w-full">
            {routeData && (
              <RouteSummaryCard
                summary={routeData.summary}
                origin={routeData.origin}
                destination={routeData.destination}
              />
            )}
            <MapComponent
              theme={theme}
              routeData={routeData}
              allStations={allStations}
              showAllStations={showAllChargingPoints}
              selectedStation={selectedStation}
              onSelectStation={setSelectedStation}
              highlightedStopIndex={highlightedStopIndex}
              apiKeyMissing={apiKeyMissing}
            />
          </section>
        </main>

        {/* Custom Vehicle Modal */}
        <CustomVehicleModal
          isOpen={isCustomVehicleModalOpen}
          onClose={() => setIsCustomVehicleModalOpen(false)}
          onSave={handleSaveCustomVehicle}
        />

        {/* Demo Routes Modal */}
        {isDemoModalOpen && (
          <DemoRoutesModal
            onClose={() => setIsDemoModalOpen(false)}
            onSelectRoute={(route) => {
              const updatedForm: RouteRequest = {
                ...formData,
                start_location: route.start_location,
                start_lat: route.start_lat,
                start_lng: route.start_lng,
                destination: route.destination,
                dest_lat: route.dest_lat,
                dest_lng: route.dest_lng,
                vehicle_model: route.vehicle_model,
                battery_capacity_kwh: route.battery_capacity_kwh,
                vehicle_efficiency_wh_per_km: route.vehicle_efficiency_wh_per_km,
                current_battery_pct: route.current_battery_pct,
              };
              setFormData(updatedForm);
              handlePlanRoute(updatedForm);
              setIsDemoModalOpen(false);
            }}
          />
        )}
      </div>
    </APIProvider>
  );
}
