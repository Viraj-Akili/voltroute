"use client";

import React, { useState } from "react";
import { BatteryProfilePoint } from "../lib/types";
import { Activity, Zap, ShieldCheck } from "lucide-react";

interface BatteryProfileChartProps {
  profile: BatteryProfilePoint[];
  totalDistanceKm: number;
}

export const BatteryProfileChart: React.FC<BatteryProfileChartProps> = ({
  profile,
  totalDistanceKm,
}) => {
  const [hoveredPoint, setHoveredPoint] = useState<BatteryProfilePoint | null>(null);
  const [hoverPos, setHoverPos] = useState<{ x: number; y: number } | null>(null);

  if (!profile || profile.length < 2) return null;

  // Chart dimensions & margins
  const width = 600;
  const height = 180;
  const padding = { top: 20, right: 30, bottom: 30, left: 45 };

  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;

  // Coordinate mapping
  const getX = (distKm: number) => {
    return padding.left + (distKm / Math.max(1, totalDistanceKm)) * innerWidth;
  };

  const getY = (socPct: number) => {
    const clamped = Math.max(0, Math.min(100, socPct));
    return padding.top + innerHeight - (clamped / 100.0) * innerHeight;
  };

  // Generate SVG path strings
  let pathD = "";
  let areaD = `M ${getX(profile[0].distance_km)} ${padding.top + innerHeight}`;

  profile.forEach((pt, idx) => {
    const x = getX(pt.distance_km);
    const y = getY(pt.soc_pct);

    if (idx === 0) {
      pathD += `M ${x} ${y}`;
      areaD += ` L ${x} ${y}`;
    } else {
      pathD += ` L ${x} ${y}`;
      areaD += ` L ${x} ${y}`;
    }
  });

  areaD += ` L ${getX(profile[profile.length - 1].distance_km)} ${padding.top + innerHeight} Z`;

  // Buffer threshold line at 10%
  const bufferY = getY(10);

  return (
    <div className="glass-panel rounded-2xl p-5 shadow-card-glass border border-white/10 space-y-3 relative">
      <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-volt-400" />
          <h4 className="text-sm font-bold text-white tracking-wide">
            Battery SOC Consumption Profile
          </h4>
        </div>
        <div className="flex items-center space-x-3 text-[11px] text-slate-400">
          <span className="flex items-center space-x-1">
            <span className="w-2.5 h-0.5 bg-volt-400 inline-block"></span>
            <span>State of Charge (%)</span>
          </span>
          <span className="flex items-center space-x-1">
            <span className="w-2.5 h-0.5 border-b border-dashed border-rose-400 inline-block"></span>
            <span>Safety Buffer (10%)</span>
          </span>
        </div>
      </div>

      {/* SVG Chart */}
      <div className="relative w-full overflow-hidden">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto overflow-visible"
        >
          <defs>
            <linearGradient id="batteryAreaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.4" />
              <stop offset="60%" stopColor="#06b6d4" stopOpacity="0.15" />
              <stop offset="100%" stopColor="#0f172a" stopOpacity="0.0" />
            </linearGradient>

            <linearGradient id="batteryLineGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#34d399" />
              <stop offset="50%" stopColor="#06b6d4" />
              <stop offset="100%" stopColor="#10b981" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {[0, 25, 50, 75, 100].map((val) => {
            const y = getY(val);
            return (
              <g key={val}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="rgba(255,255,255,0.06)"
                  strokeDasharray={val === 0 || val === 100 ? "0" : "3,3"}
                />
                <text
                  x={padding.left - 8}
                  y={y + 3.5}
                  textAnchor="end"
                  className="fill-slate-500 text-[9px] font-medium"
                >
                  {val}%
                </text>
              </g>
            );
          })}

          {/* Buffer threshold line */}
          <line
            x1={padding.left}
            y1={bufferY}
            x2={width - padding.right}
            y2={bufferY}
            stroke="rgba(244, 63, 94, 0.6)"
            strokeDasharray="4,4"
            strokeWidth="1.2"
          />

          {/* Shaded Area */}
          <path d={areaD} fill="url(#batteryAreaGrad)" />

          {/* Profile Line */}
          <path
            d={pathD}
            fill="none"
            stroke="url(#batteryLineGrad)"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Key Waypoint Points (Chargers & Ends) */}
          {profile.map((pt, i) => {
            const isEvent =
              pt.event === "arrival_at_charger" ||
              pt.event === "charged_at_charger" ||
              pt.event === "start" ||
              pt.event === "destination";

            if (!isEvent) return null;

            const cx = getX(pt.distance_km);
            const cy = getY(pt.soc_pct);
            const isCharging = pt.event === "charged_at_charger";

            return (
              <g
                key={i}
                className="cursor-pointer transition-all hover:scale-125"
                onMouseEnter={() => {
                  setHoveredPoint(pt);
                  setHoverPos({ x: cx, y: cy });
                }}
                onMouseLeave={() => {
                  setHoveredPoint(null);
                  setHoverPos(null);
                }}
              >
                <circle
                  cx={cx}
                  cy={cy}
                  r={isCharging ? "5" : "4"}
                  className={
                    isCharging
                      ? "fill-volt-400 stroke-space-900 stroke-2"
                      : pt.event === "arrival_at_charger"
                      ? "fill-yellow-400 stroke-space-900 stroke-2"
                      : "fill-electric-400 stroke-space-900 stroke-2"
                  }
                />
              </g>
            );
          })}

          {/* X-axis distance labels */}
          <text
            x={padding.left}
            y={height - 8}
            textAnchor="start"
            className="fill-slate-500 text-[9px] font-medium"
          >
            0 km
          </text>
          <text
            x={width - padding.right}
            y={height - 8}
            textAnchor="end"
            className="fill-slate-500 text-[9px] font-medium"
          >
            {Math.round(totalDistanceKm)} km
          </text>
        </svg>

        {/* Floating Tooltip */}
        {hoveredPoint && hoverPos && (
          <div
            className="absolute z-20 pointer-events-none transform -translate-x-1/2 -translate-y-full mb-2 bg-space-900/95 border border-volt-500/40 px-3 py-1.5 rounded-lg shadow-volt-glow text-xs"
            style={{
              left: `${(hoverPos.x / width) * 100}%`,
              top: `${(hoverPos.y / height) * 100}%`,
            }}
          >
            <p className="font-bold text-white flex items-center space-x-1">
              <Zap className="w-3 h-3 text-volt-400" />
              <span>{hoveredPoint.soc_pct}% SOC</span>
            </p>
            <p className="text-[10px] text-slate-300 font-medium truncate max-w-[160px]">
              {hoveredPoint.location_name}
            </p>
            <p className="text-[9px] text-slate-500">
              @ {hoveredPoint.distance_km} km
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
