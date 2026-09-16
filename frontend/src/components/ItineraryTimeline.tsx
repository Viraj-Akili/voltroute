"use client";

import React from "react";
import {
  MapPin,
  Flag,
  BatteryCharging,
  Zap,
  Coffee,
  Utensils,
  Wifi,
  ShoppingBag,
  DollarSign,
  Clock,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";
import { RouteLeg, ChargingStop, ResolvedLocation } from "../lib/types";

interface ItineraryTimelineProps {
  origin: ResolvedLocation;
  destination: ResolvedLocation;
  legs: RouteLeg[];
  stops: ChargingStop[];
  initialSoc: number;
}

export const ItineraryTimeline: React.FC<ItineraryTimelineProps> = ({
  origin,
  destination,
  legs,
  stops,
  initialSoc,
}) => {
  // Render amenity icon based on string
  const renderAmenityIcon = (amenity: string) => {
    const lower = amenity.toLowerCase();
    if (lower.includes("coffee")) return <span title="Coffee"><Coffee className="w-3.5 h-3.5 text-amber-400" /></span>;
    if (lower.includes("dining") || lower.includes("food") || lower.includes("restaurant"))
      return <span title="Dining"><Utensils className="w-3.5 h-3.5 text-orange-400" /></span>;
    if (lower.includes("wifi")) return <span title="WiFi"><Wifi className="w-3.5 h-3.5 text-sky-400" /></span>;
    if (lower.includes("shopping") || lower.includes("outlets") || lower.includes("mall"))
      return <span title="Shopping"><ShoppingBag className="w-3.5 h-3.5 text-purple-400" /></span>;
    return <span title={amenity}><ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /></span>;
  };

  const formatMinutes = (mins: number) => {
    const h = Math.floor(mins / 60);
    const m = Math.round(mins % 60);
    if (h === 0) return `${m}m`;
    return `${h}h ${m > 0 ? `${m}m` : ""}`;
  };

  return (
    <div className="glass-panel rounded-2xl p-5 sm:p-6 shadow-card-glass border border-white/10 space-y-4">
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <h4 className="text-base font-bold text-white tracking-wide flex items-center space-x-2">
          <Clock className="w-4 h-4 text-volt-400" />
          <span>Turn-by-Turn EV Itinerary</span>
        </h4>
        <span className="text-xs text-slate-400 font-medium">
          {stops.length === 0 ? "Non-Stop Direct Leg" : `${stops.length} Optimized Stop${stops.length > 1 ? "s" : ""}`}
        </span>
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-gradient-to-b before:from-volt-400 before:via-electric-cyan before:to-rose-400">
        {/* Origin Step */}
        <div className="relative">
          <div className="absolute -left-6 top-1 w-5 h-5 rounded-full bg-space-900 border-2 border-volt-400 flex items-center justify-center shadow-volt-glow">
            <div className="w-2 h-2 rounded-full bg-volt-400 animate-pulse"></div>
          </div>
          <div className="bg-space-850/60 rounded-xl p-3.5 border border-white/5 space-y-1">
            <div className="flex items-center justify-between">
              <span className="text-xs font-extrabold uppercase tracking-wider text-volt-400">
                Departure
              </span>
              <span className="text-xs font-bold text-white bg-space-900 px-2 py-0.5 rounded border border-white/10">
                {initialSoc}% Battery
              </span>
            </div>
            <p className="text-sm font-bold text-white">{origin.name}</p>
            <p className="text-xs text-slate-400 truncate">{origin.formatted_address}</p>
          </div>
        </div>

        {/* Legs and Stops */}
        {legs.map((leg, idx) => {
          const correspondingStop = stops[idx]; // stop after this leg (if any)

          return (
            <React.Fragment key={leg.leg_index}>
              {/* Driving Leg info */}
              <div className="relative my-2">
                <div className="flex items-center justify-between text-xs text-slate-400 bg-space-900/40 rounded-lg px-3 py-1.5 border border-dashed border-white/10">
                  <span className="flex items-center space-x-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-electric-400"></span>
                    <span>Drive {leg.distance_km} km ({formatMinutes(leg.duration_min)})</span>
                  </span>
                  <span className="text-slate-500 font-medium">
                    Uses {leg.energy_used_kwh} kWh ({leg.start_soc_pct}% → {leg.end_soc_pct}%)
                  </span>
                </div>
              </div>

              {/* Charging Stop Card (if not final destination) */}
              {correspondingStop && (
                <div className="relative">
                  <div className="absolute -left-6 top-1 w-5 h-5 rounded-full bg-space-900 border-2 border-electric-cyan flex items-center justify-center shadow-cyan-glow">
                    <Zap className="w-3 h-3 text-electric-cyan" />
                  </div>

                  <div className="bg-gradient-to-br from-space-800 to-space-850 rounded-xl p-4 border border-electric-cyan/25 shadow-card-glass space-y-2.5">
                    {/* Header */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="px-2 py-0.5 rounded bg-electric-cyan/15 text-electric-cyan text-[11px] font-extrabold uppercase tracking-wide border border-electric-cyan/30">
                          Stop #{correspondingStop.stop_index}
                        </span>
                        <span className="text-xs text-slate-400 font-medium">
                          {correspondingStop.station.operator}
                        </span>
                      </div>
                      <span className="text-xs font-extrabold text-volt-300 bg-volt-500/10 px-2.5 py-1 rounded-full border border-volt-500/20 flex items-center space-x-1">
                        <BatteryCharging className="w-3.5 h-3.5" />
                        <span>Charge {correspondingStop.charge_duration_min} min</span>
                      </span>
                    </div>

                    {/* Station Name & Power */}
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h5 className="text-sm font-bold text-white">
                          {correspondingStop.station.name}
                        </h5>
                        <p className="text-xs text-slate-400">
                          {correspondingStop.station.city}, {correspondingStop.station.state}
                        </p>
                      </div>
                      <div className="text-right shrink-0">
                        <span className="inline-block px-2 py-0.5 rounded bg-amber-500/15 text-amber-300 font-black text-xs border border-amber-500/30">
                          {correspondingStop.station.power_kw} kW
                        </span>
                      </div>
                    </div>

                    {/* Battery SOC Jump and Energy Details */}
                    <div className="grid grid-cols-2 gap-2 bg-space-900/80 rounded-lg p-2.5 border border-white/5 text-xs">
                      <div>
                        <span className="text-slate-500 text-[10px] block">Battery Level</span>
                        <span className="font-bold text-white flex items-center space-x-1">
                          <span className="text-yellow-400">{correspondingStop.arrival_soc_pct}%</span>
                          <ArrowRight className="w-3 h-3 text-slate-400" />
                          <span className="text-volt-400">{correspondingStop.departure_soc_pct}%</span>
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-500 text-[10px] block">Energy Added & Cost</span>
                        <span className="font-bold text-white">
                          +{correspondingStop.energy_added_kwh} kWh (${correspondingStop.estimated_cost_usd.toFixed(2)})
                        </span>
                      </div>
                    </div>

                    {/* Amenities & Connectors */}
                    <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-white/5 text-xs">
                      <div className="flex items-center space-x-1.5 text-slate-400">
                        <span className="text-[10px] text-slate-500 font-medium">Plugs:</span>
                        <span className="font-medium text-slate-300">
                          {correspondingStop.station.connector_types.join(", ")}
                        </span>
                      </div>

                      {/* Amenity Icons */}
                      <div className="flex items-center space-x-2">
                        {correspondingStop.station.amenities.map((amenity, aIdx) => (
                          <span key={aIdx} className="p-1 rounded bg-space-750 border border-white/5">
                            {renderAmenityIcon(amenity)}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </React.Fragment>
          );
        })}

        {/* Destination Step */}
        <div className="relative">
          <div className="absolute -left-6 top-1 w-5 h-5 rounded-full bg-space-900 border-2 border-rose-400 flex items-center justify-center">
            <Flag className="w-3 h-3 text-rose-400" />
          </div>
          <div className="bg-space-850/60 rounded-xl p-3.5 border border-white/5 space-y-1">
            <div className="flex items-center justify-between">
              <span className="text-xs font-extrabold uppercase tracking-wider text-rose-400">
                Destination Arrival
              </span>
              <span className="text-xs font-bold text-volt-300 bg-volt-500/10 px-2 py-0.5 rounded border border-volt-500/20">
                {legs[legs.length - 1]?.end_soc_pct ?? 15}% Battery
              </span>
            </div>
            <p className="text-sm font-bold text-white">{destination.name}</p>
            <p className="text-xs text-slate-400 truncate">{destination.formatted_address}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
