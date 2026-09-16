"use client";

import React from "react";
import {
  Clock,
  Navigation,
  BatteryCharging,
  Zap,
  DollarSign,
  Leaf,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";
import { TripSummary, ResolvedLocation } from "../lib/types";

interface RouteSummaryCardProps {
  summary: TripSummary;
  origin: ResolvedLocation;
  destination: ResolvedLocation;
}

export const RouteSummaryCard: React.FC<RouteSummaryCardProps> = ({
  summary,
  origin,
  destination,
}) => {
  // Format minutes into hours and minutes
  const formatTime = (minutes: number) => {
    const hrs = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    if (hrs === 0) return `${mins}m`;
    return `${hrs}h ${mins > 0 ? `${mins}m` : ""}`;
  };

  const drivePct = Math.round(
    (summary.total_drive_time_min / Math.max(1, summary.total_trip_time_min)) * 100
  );
  const chargePct = 100 - drivePct;

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 shadow-card-glass border border-white/10 space-y-4">
      {/* Route Title & Feasibility Badge */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/5 pb-3">
        <div>
          <div className="flex items-center space-x-2 text-xs text-slate-400 font-medium">
            <span>Trip Plan</span>
            <span>•</span>
            <span className="text-slate-300 font-semibold">{origin.name}</span>
            <span>→</span>
            <span className="text-slate-300 font-semibold">{destination.name}</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-black text-white tracking-tight mt-0.5">
            {formatTime(summary.total_trip_time_min)}
            <span className="text-xs text-slate-400 font-normal ml-2">Total Journey Time</span>
          </h3>
        </div>

        <div>
          {summary.is_feasible ? (
            <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-volt-500/15 text-volt-400 border border-volt-500/30 text-xs font-bold">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Route Feasible</span>
            </span>
          ) : (
            <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 text-xs font-bold">
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>Charging Gap Detected</span>
            </span>
          )}
        </div>
      </div>

      {/* Time Split Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs text-slate-300 font-medium">
          <span className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 rounded-sm bg-electric-500 inline-block"></span>
            <span>Driving: {formatTime(summary.total_drive_time_min)} ({drivePct}%)</span>
          </span>
          <span className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 rounded-sm bg-volt-400 inline-block"></span>
            <span>Charging: {formatTime(summary.total_charge_time_min)} ({chargePct}%)</span>
          </span>
        </div>
        <div className="w-full h-2.5 bg-space-800 rounded-full overflow-hidden flex p-0.5 border border-white/5">
          <div
            style={{ width: `${drivePct}%` }}
            className="h-full bg-electric-500 rounded-l-full transition-all"
            title={`Drive time: ${formatTime(summary.total_drive_time_min)}`}
          ></div>
          <div
            style={{ width: `${chargePct}%` }}
            className="h-full bg-volt-400 rounded-r-full transition-all"
            title={`Charge time: ${formatTime(summary.total_charge_time_min)}`}
          ></div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
        {/* Total Distance */}
        <div className="bg-space-850/60 rounded-xl p-3 border border-white/5">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium mb-1">
            <Navigation className="w-3.5 h-3.5 text-electric-400" />
            <span>Total Distance</span>
          </div>
          <p className="text-base sm:text-lg font-extrabold text-white">
            {summary.total_distance_km}{" "}
            <span className="text-xs text-slate-400 font-normal">km</span>
          </p>
          <p className="text-[10px] text-slate-500 font-medium">
            ({summary.total_distance_miles} mi)
          </p>
        </div>

        {/* Charging Stops */}
        <div className="bg-space-850/60 rounded-xl p-3 border border-white/5">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium mb-1">
            <BatteryCharging className="w-3.5 h-3.5 text-volt-400" />
            <span>Charging Stops</span>
          </div>
          <p className="text-base sm:text-lg font-extrabold text-volt-300">
            {summary.num_stops}{" "}
            <span className="text-xs text-slate-400 font-normal">
              {summary.num_stops === 1 ? "Stop" : "Stops"}
            </span>
          </p>
          <p className="text-[10px] text-slate-500 font-medium">
            {summary.num_stops === 0 ? "Non-stop drive" : `${formatTime(summary.total_charge_time_min)} at plugs`}
          </p>
        </div>

        {/* Energy & Cost */}
        <div className="bg-space-850/60 rounded-xl p-3 border border-white/5">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium mb-1">
            <DollarSign className="w-3.5 h-3.5 text-yellow-400" />
            <span>Est. Energy Cost</span>
          </div>
          <p className="text-base sm:text-lg font-extrabold text-white">
            ${summary.total_charging_cost_usd.toFixed(2)}
          </p>
          <p className="text-[10px] text-slate-500 font-medium">
            {summary.total_energy_consumed_kwh} kWh consumed
          </p>
        </div>

        {/* CO2 Saved */}
        <div className="bg-space-850/60 rounded-xl p-3 border border-white/5">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium mb-1">
            <Leaf className="w-3.5 h-3.5 text-emerald-400" />
            <span>CO₂ Avoided</span>
          </div>
          <p className="text-base sm:text-lg font-extrabold text-emerald-300">
            {summary.co2_saved_kg}{" "}
            <span className="text-xs text-slate-400 font-normal">kg</span>
          </p>
          <p className="text-[10px] text-slate-500 font-medium">
            vs Gasoline Engine
          </p>
        </div>
      </div>

      {/* Arrival SOC Note */}
      <div className="flex items-center justify-between text-xs bg-space-900/90 rounded-lg px-3.5 py-2 border border-white/5">
        <span className="text-slate-400">Destination Arrival Battery:</span>
        <span className="font-bold text-volt-300 flex items-center space-x-1">
          <Zap className="w-3.5 h-3.5 text-volt-400" />
          <span>{summary.final_battery_pct}% remaining</span>
        </span>
      </div>
    </div>
  );
};
