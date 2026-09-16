"use client";

import React, { useState, useEffect } from "react";
import {
  MapPin,
  Flag,
  BatteryCharging,
  BatteryMedium,
  Zap,
  Sliders,
  ChevronDown,
  ChevronUp,
  ArrowUpDown,
  Car,
  Gauge,
  ShieldAlert,
  Settings2,
} from "lucide-react";
import { RouteRequest, VehiclePreset } from "../lib/types";

interface RoutePlannerFormProps {
  presets: VehiclePreset[];
  loading: boolean;
  onPlanRoute: (request: RouteRequest) => void;
  initialValues?: Partial<RouteRequest>;
}

export const RoutePlannerForm: React.FC<RoutePlannerFormProps> = ({
  presets,
  loading,
  onPlanRoute,
  initialValues,
}) => {
  const [startLocation, setStartLocation] = useState<string>("Los Angeles, CA");
  const [destination, setDestination] = useState<string>("San Francisco, CA");
  const [selectedPresetId, setSelectedPresetId] = useState<string>("tesla-model-3-lr");
  const [batteryCapacity, setBatteryCapacity] = useState<number>(75.0);
  const [efficiency, setEfficiency] = useState<number>(150.0);
  const [currentBatteryPct, setCurrentBatteryPct] = useState<number>(70);
  const [minStopSoc, setMinStopSoc] = useState<number>(10);
  const [targetDestSoc, setTargetDestSoc] = useState<number>(15);
  const [maxChargeSoc, setMaxChargeSoc] = useState<number>(80);
  const [minPowerKw, setMinPowerKw] = useState<number>(150);
  const [showAdvanced, setShowAdvanced] = useState<boolean>(false);

  // Sync initial values when updated from external triggers (e.g. demo routes modal)
  useEffect(() => {
    if (initialValues) {
      if (initialValues.start_location && typeof initialValues.start_location === "string") {
        setStartLocation(initialValues.start_location);
      }
      if (initialValues.destination && typeof initialValues.destination === "string") {
        setDestination(initialValues.destination);
      }
      if (initialValues.current_battery_pct !== undefined) {
        setCurrentBatteryPct(initialValues.current_battery_pct);
      }
      if (initialValues.battery_capacity_kwh !== undefined) {
        setBatteryCapacity(initialValues.battery_capacity_kwh);
      }
      if (initialValues.vehicle_efficiency_wh_per_km !== undefined) {
        setEfficiency(initialValues.vehicle_efficiency_wh_per_km);
      }
      if (initialValues.vehicle_model) {
        const found = presets.find((p) => p.name === initialValues.vehicle_model);
        if (found) setSelectedPresetId(found.id);
      }
    }
  }, [initialValues, presets]);

  // Handle vehicle preset change
  const handlePresetChange = (presetId: string) => {
    setSelectedPresetId(presetId);
    if (presetId === "custom") return;

    const preset = presets.find((p) => p.id === presetId);
    if (preset) {
      setBatteryCapacity(preset.battery_capacity_kwh);
      setEfficiency(preset.efficiency_wh_per_km);
    }
  };

  // Swap Start & Destination
  const handleSwapLocations = () => {
    const temp = startLocation;
    setStartLocation(destination);
    setDestination(temp);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!startLocation.trim() || !destination.trim()) return;

    const selectedPreset = presets.find((p) => p.id === selectedPresetId);

    const request: RouteRequest = {
      start_location: startLocation.trim(),
      destination: destination.trim(),
      current_battery_pct: currentBatteryPct,
      battery_capacity_kwh: batteryCapacity,
      vehicle_efficiency_wh_per_km: efficiency,
      vehicle_model: selectedPreset?.name || "Custom EV",
      min_stop_soc_pct: minStopSoc,
      target_dest_soc_pct: targetDestSoc,
      max_charge_soc_pct: maxChargeSoc,
      min_charger_power_kw: minPowerKw > 0 ? minPowerKw : undefined,
    };

    onPlanRoute(request);
  };

  // Battery percentage color helper
  const getBatteryColor = (pct: number) => {
    if (pct >= 60) return "text-volt-400";
    if (pct >= 25) return "text-yellow-400";
    return "text-rose-400";
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="glass-panel rounded-2xl p-5 sm:p-6 shadow-card-glass border border-white/10 space-y-5"
    >
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <div className="flex items-center space-x-2">
          <Sliders className="w-5 h-5 text-volt-400" />
          <h2 className="text-base sm:text-lg font-bold text-white tracking-wide">
            Plan EV Journey
          </h2>
        </div>
        <span className="text-xs text-slate-400 font-medium">Route Parameters</span>
      </div>

      {/* Locations Input Group */}
      <div className="space-y-3 relative">
        {/* Origin */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-volt-400 inline-block animate-pulse"></span>
            <span>Origin Location</span>
          </label>
          <div className="relative">
            <MapPin className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-volt-400" />
            <input
              type="text"
              required
              value={startLocation}
              onChange={(e) => setStartLocation(e.target.value)}
              placeholder="e.g. Los Angeles, CA or Address"
              className="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-sm text-white placeholder-slate-500 font-medium"
            />
          </div>
        </div>

        {/* Swap Button */}
        <div className="flex justify-end -my-1.5 pr-2">
          <button
            type="button"
            onClick={handleSwapLocations}
            title="Swap Origin & Destination"
            className="p-1.5 rounded-full bg-space-750 hover:bg-space-700 text-slate-300 hover:text-volt-400 border border-white/10 shadow-sm transition-all hover:scale-110 active:scale-95 z-10"
          >
            <ArrowUpDown className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Destination */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-rose-400 inline-block"></span>
            <span>Final Destination</span>
          </label>
          <div className="relative">
            <Flag className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-rose-400" />
            <input
              type="text"
              required
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="e.g. San Francisco, CA or Address"
              className="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-sm text-white placeholder-slate-500 font-medium"
            />
          </div>
        </div>
      </div>

      {/* Vehicle Preset Selector */}
      <div>
        <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center space-x-1.5">
          <Car className="w-3.5 h-3.5 text-electric-cyan" />
          <span>Vehicle Model</span>
        </label>
        <div className="relative">
          <select
            value={selectedPresetId}
            onChange={(e) => handlePresetChange(e.target.value)}
            className="glass-input w-full px-3.5 py-2.5 rounded-xl text-sm text-white font-medium appearance-none cursor-pointer pr-10"
          >
            {presets.map((p) => (
              <option key={p.id} value={p.id} className="bg-space-900 text-slate-200">
                {p.name} ({p.battery_capacity_kwh} kWh)
              </option>
            ))}
            <option value="custom" className="bg-space-900 text-slate-200">
              Custom Vehicle Specs...
            </option>
          </select>
          <ChevronDown className="absolute right-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
        </div>
      </div>

      {/* Battery Capacity & Efficiency Grid */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">
            Battery Size (kWh)
          </label>
          <div className="relative">
            <input
              type="number"
              min={15}
              max={250}
              step={0.5}
              value={batteryCapacity}
              onChange={(e) => {
                setBatteryCapacity(parseFloat(e.target.value) || 75);
                setSelectedPresetId("custom");
              }}
              className="glass-input w-full px-3 py-2 rounded-lg text-sm text-white font-semibold"
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-500 font-medium">
              kWh
            </span>
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">
            Efficiency (Wh/km)
          </label>
          <div className="relative">
            <input
              type="number"
              min={80}
              max={450}
              step={1}
              value={efficiency}
              onChange={(e) => {
                setEfficiency(parseFloat(e.target.value) || 160);
                setSelectedPresetId("custom");
              }}
              className="glass-input w-full px-3 py-2 rounded-lg text-sm text-white font-semibold"
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-500 font-medium">
              Wh/km
            </span>
          </div>
        </div>
      </div>

      {/* Starting Battery Level Slider */}
      <div className="bg-space-850/60 rounded-xl p-3.5 border border-white/5 space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-300 flex items-center space-x-1.5">
            <BatteryMedium className={`w-4 h-4 ${getBatteryColor(currentBatteryPct)}`} />
            <span>Starting Battery SOC</span>
          </label>
          <span
            className={`text-sm font-extrabold px-2 py-0.5 rounded-md bg-space-900 border border-white/10 ${getBatteryColor(
              currentBatteryPct
            )}`}
          >
            {currentBatteryPct}%
          </span>
        </div>
        <input
          type="range"
          min={10}
          max={100}
          step={1}
          value={currentBatteryPct}
          onChange={(e) => setCurrentBatteryPct(parseInt(e.target.value, 10))}
          className="w-full h-2 bg-space-700 rounded-lg appearance-none cursor-pointer accent-volt-400"
        />
        <div className="flex justify-between text-[10px] text-slate-500 font-medium">
          <span>10% (Low)</span>
          <span>50%</span>
          <span>80% (Recommended)</span>
          <span>100% (Full)</span>
        </div>
      </div>

      {/* Advanced Optimization Options Accordion */}
      <div>
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center justify-between w-full text-xs font-semibold text-slate-400 hover:text-slate-200 py-1 transition-colors"
        >
          <span className="flex items-center space-x-1.5">
            <Settings2 className="w-3.5 h-3.5 text-volt-400" />
            <span>Advanced Charging Controls</span>
          </span>
          {showAdvanced ? (
            <ChevronUp className="w-3.5 h-3.5" />
          ) : (
            <ChevronDown className="w-3.5 h-3.5" />
          )}
        </button>

        {showAdvanced && (
          <div className="mt-3 p-3.5 bg-space-850/70 rounded-xl border border-white/5 space-y-3 text-xs">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[11px] text-slate-400 font-medium block mb-1">
                  Min Stop Buffer (%)
                </label>
                <input
                  type="number"
                  min={5}
                  max={25}
                  value={minStopSoc}
                  onChange={(e) => setMinStopSoc(parseInt(e.target.value, 10) || 10)}
                  className="glass-input w-full px-2.5 py-1.5 rounded-lg text-white font-medium"
                />
              </div>
              <div>
                <label className="text-[11px] text-slate-400 font-medium block mb-1">
                  Dest Arrival Target (%)
                </label>
                <input
                  type="number"
                  min={5}
                  max={40}
                  value={targetDestSoc}
                  onChange={(e) => setTargetDestSoc(parseInt(e.target.value, 10) || 15)}
                  className="glass-input w-full px-2.5 py-1.5 rounded-lg text-white font-medium"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[11px] text-slate-400 font-medium block mb-1">
                  Max Stop Charge Limit (%)
                </label>
                <input
                  type="number"
                  min={60}
                  max={95}
                  value={maxChargeSoc}
                  onChange={(e) => setMaxChargeSoc(parseInt(e.target.value, 10) || 80)}
                  className="glass-input w-full px-2.5 py-1.5 rounded-lg text-white font-medium"
                />
              </div>
              <div>
                <label className="text-[11px] text-slate-400 font-medium block mb-1">
                  Min Charger Speed (kW)
                </label>
                <select
                  value={minPowerKw}
                  onChange={(e) => setMinPowerKw(parseInt(e.target.value, 10))}
                  className="glass-input w-full px-2.5 py-1.5 rounded-lg text-white font-medium bg-space-900"
                >
                  <option value={50}>50 kW+ (All DC)</option>
                  <option value={150}>150 kW+ (Fast DC)</option>
                  <option value={250}>250 kW+ (Ultra-Fast)</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Plan Route Button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full relative group overflow-hidden rounded-xl bg-gradient-to-r from-volt-500 via-volt-400 to-electric-cyan p-px font-semibold shadow-volt-glow transition-all hover:shadow-cyan-glow active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <div className="w-full bg-space-900 group-hover:bg-transparent transition-colors py-3.5 px-4 rounded-[11px] flex items-center justify-center space-x-2">
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-volt-400 border-t-transparent rounded-full animate-spin"></div>
              <span className="text-volt-300 font-bold tracking-wide">
                Simulating Energy & Charging Stops...
              </span>
            </>
          ) : (
            <>
              <Zap className="w-5 h-5 text-volt-400 fill-volt-400 group-hover:text-space-900 group-hover:fill-space-900 transition-colors" />
              <span className="text-white group-hover:text-space-900 font-bold tracking-wide transition-colors">
                Calculate Optimal EV Route
              </span>
            </>
          )}
        </div>
      </button>
    </form>
  );
};
