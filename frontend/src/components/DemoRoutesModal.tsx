"use client";

import React from "react";
import { X, Sparkles, ArrowRight, Zap, MapPin, Navigation } from "lucide-react";
import { RouteRequest } from "../lib/types";

interface DemoRouteItem {
  title: string;
  category: string;
  start: string;
  dest: string;
  distance: string;
  vehicle: string;
  batteryPct: number;
  description: string;
  stopsExpected: string;
}

const DEMO_ROUTES: DemoRouteItem[] = [
  {
    title: "California Highway I-5 Classic",
    category: "West Coast",
    start: "Los Angeles, CA",
    dest: "San Francisco, CA",
    distance: "615 km (382 mi)",
    vehicle: "Tesla Model 3 Long Range",
    batteryPct: 70,
    description: "Iconic California interstate drive through Central Valley featuring Kettleman City & Harris Ranch Superchargers.",
    stopsExpected: "1-2 Stops (Kettleman City / Harris Ranch)"
  },
  {
    title: "Pacific Northwest Green Corridor",
    category: "PNW",
    start: "Seattle, WA",
    dest: "Portland, OR",
    distance: "280 km (174 mi)",
    vehicle: "Hyundai Ioniq 5 AWD (77.4 kWh)",
    batteryPct: 85,
    description: "Scenic Interstate 5 route linking the Emerald City with Portland via Olympia and Centralia.",
    stopsExpected: "0-1 Stop (Centralia Outlets)"
  },
  {
    title: "Northeast Megalopolis",
    category: "East Coast",
    start: "New York, NY",
    dest: "Boston, MA",
    distance: "350 km (217 mi)",
    vehicle: "Tesla Model Y Long Range",
    batteryPct: 75,
    description: "High-density I-95 coastal corridor through Connecticut and Rhode Island.",
    stopsExpected: "1 Stop (New Haven / Foxborough)"
  },
  {
    title: "Mojave Desert Run",
    category: "Southwest",
    start: "Los Angeles, CA",
    dest: "Las Vegas, NV",
    distance: "435 km (270 mi)",
    vehicle: "Ford Mustang Mach-E Extended Range",
    batteryPct: 80,
    description: "Trans-desert climb across the Cajon Pass, Barstow, and world-famous Baker oasis.",
    stopsExpected: "1-2 Stops (Barstow / Baker)"
  },
  {
    title: "Texas Innovation Triangle",
    category: "Texas",
    start: "Austin, TX",
    dest: "Houston, TX",
    distance: "265 km (165 mi)",
    vehicle: "Porsche Taycan Performance Battery Plus",
    batteryPct: 65,
    description: "Fast sprint across Texas State Highway 71 and I-10 with Buc-ee's high power hubs.",
    stopsExpected: "1 Stop (Columbus Buc-ee's)"
  },
  {
    title: "Eurotunnel Cross-Channel Expressway",
    category: "Europe",
    start: "London",
    dest: "Paris",
    distance: "460 km (285 mi)",
    vehicle: "Tesla Model 3 Long Range",
    batteryPct: 90,
    description: "Cross-border European route from Greater London via Folkestone Eurotunnel to Paris.",
    stopsExpected: "1-2 Stops (Folkestone / Calais / Senlis)"
  }
];

interface DemoRoutesModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectRoute: (start: string, dest: string, batteryPct: number, vehicleModel: string) => void;
}

export const DemoRoutesModal: React.FC<DemoRoutesModalProps> = ({
  isOpen,
  onClose,
  onSelectRoute,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-900/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-2xl bg-space-850 rounded-2xl border border-white/15 shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-5 border-b border-white/10 bg-space-900/80">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 rounded-xl bg-volt-500/10 border border-volt-500/20">
              <Sparkles className="w-5 h-5 text-volt-400" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white tracking-tight">
                Curated EV Road Trips
              </h3>
              <p className="text-xs text-slate-400">
                Test real-world energy simulation and fast-charging stop recommendations
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Routes Grid */}
        <div className="p-5 overflow-y-auto space-y-3">
          {DEMO_ROUTES.map((route, i) => (
            <div
              key={i}
              onClick={() => {
                onSelectRoute(route.start, route.dest, route.batteryPct, route.vehicle);
                onClose();
              }}
              className="group cursor-pointer bg-space-800/80 hover:bg-space-750 p-4 rounded-xl border border-white/5 hover:border-volt-500/40 shadow-sm transition-all hover:shadow-volt-glow flex flex-col sm:flex-row sm:items-center justify-between gap-3"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded bg-volt-500/10 text-volt-400 border border-volt-500/20">
                    {route.category}
                  </span>
                  <span className="text-xs font-semibold text-slate-300">
                    {route.distance}
                  </span>
                </div>

                <h4 className="text-sm font-bold text-white group-hover:text-volt-300 transition-colors flex items-center space-x-2">
                  <span>{route.start}</span>
                  <ArrowRight className="w-3.5 h-3.5 text-volt-400" />
                  <span>{route.dest}</span>
                </h4>

                <p className="text-xs text-slate-400 line-clamp-2">
                  {route.description}
                </p>

                <div className="flex items-center space-x-3 text-[11px] text-slate-400 pt-0.5">
                  <span className="text-slate-300 font-medium">
                    ⚡ {route.vehicle}
                  </span>
                  <span>•</span>
                  <span className="text-amber-300">
                    {route.stopsExpected}
                  </span>
                </div>
              </div>

              <div className="sm:self-center shrink-0">
                <span className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-volt-500/10 text-volt-400 border border-volt-500/30 text-xs font-bold group-hover:bg-volt-500 group-hover:text-space-900 transition-all">
                  <span>Load Trip</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
