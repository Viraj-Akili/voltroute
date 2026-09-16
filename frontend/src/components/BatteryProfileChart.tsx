'use client';

import React from 'react';
import { BatteryProfilePoint, RouteStop } from '../lib/types';

interface BatteryProfileChartProps {
  profilePoints: BatteryProfilePoint[];
  stops: RouteStop[];
  initialPct: number;
  batteryCapacityKwh: number;
}

export default function BatteryProfileChart({
  profilePoints,
  stops,
  initialPct,
  batteryCapacityKwh,
}: BatteryProfileChartProps) {
  if (!profilePoints || profilePoints.length === 0) {
    return null;
  }

  const maxDist = Math.max(...profilePoints.map((p) => p.distance_km), 1);
  const chartHeight = 160;
  const chartWidth = 460;
  const padding = { top: 20, right: 25, bottom: 30, left: 35 };

  const usableWidth = chartWidth - padding.left - padding.right;
  const usableHeight = chartHeight - padding.top - padding.bottom;

  // Scale functions
  const scaleX = (d: number) => padding.left + (d / maxDist) * usableWidth;
  const scaleY = (soc: number) => padding.top + usableHeight - (soc / 100) * usableHeight;

  // Generate SVG path for battery profile
  const pathD = profilePoints.reduce((acc, point, index) => {
    const x = scaleX(point.distance_km);
    const y = scaleY(point.soc_pct ?? point.battery_pct ?? 0);
    return index === 0 ? `M ${x} ${y}` : `${acc} L ${x} ${y}`;
  }, '');

  // Fill area under path
  const areaD = `${pathD} L ${scaleX(maxDist)} ${scaleY(0)} L ${scaleX(0)} ${scaleY(0)} Z`;

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3 transition-colors">
      <div className="flex items-center justify-between pb-1 border-b border-slate-100 dark:border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
            Battery Profile
          </h3>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
            Estimated state of charge along your route
          </p>
        </div>
        <div className="flex items-center gap-3 text-[11px] text-slate-500">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-0.5 bg-emerald-500 inline-block rounded"></span> SOC %
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span> Charge Stop
          </span>
        </div>
      </div>

      <div className="w-full overflow-x-auto">
        <svg
          viewBox={`0 0 ${chartWidth} ${chartHeight}`}
          className="w-full h-auto min-w-[320px] text-slate-400 select-none"
        >
          <defs>
            <linearGradient id="batteryGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.35" />
              <stop offset="80%" stopColor="#10b981" stopOpacity="0.05" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {[0, 25, 50, 75, 100].map((soc) => (
            <g key={soc}>
              <line
                x1={padding.left}
                y1={scaleY(soc)}
                x2={chartWidth - padding.right}
                y2={scaleY(soc)}
                stroke="currentColor"
                strokeOpacity={soc === 0 || soc === 100 ? 0.2 : 0.1}
                strokeDasharray={soc === 0 || soc === 100 ? '' : '3,3'}
              />
              <text
                x={padding.left - 6}
                y={scaleY(soc) + 3}
                fontSize="9"
                fill="currentColor"
                textAnchor="end"
                className="font-mono text-[9px]"
              >
                {soc}%
              </text>
            </g>
          ))}

          {/* Buffer warning zone (below 15%) */}
          <rect
            x={padding.left}
            y={scaleY(15)}
            width={usableWidth}
            height={scaleY(0) - scaleY(15)}
            fill="#ef4444"
            fillOpacity="0.06"
          />

          {/* Area fill */}
          <path d={areaD} fill="url(#batteryGrad)" />

          {/* SOC curve */}
          <path d={pathD} fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />

          {/* Charging stops indicators */}
          {stops.map((stop, idx) => {
            const stopPoint = profilePoints.find((p) => p.distance_km >= stop.arrival_soc_pct); // approximate
            const cx = scaleX(idx === 0 ? maxDist * 0.45 : maxDist * 0.75); // fallback approximation
            return (
              <g key={idx}>
                <circle cx={cx} cy={scaleY(stop.arrival_soc_pct)} r="4" fill="#10b981" stroke="#ffffff" strokeWidth="1.5" />
                <line
                  x1={cx}
                  y1={scaleY(stop.arrival_soc_pct)}
                  x2={cx}
                  y2={scaleY(stop.departure_soc_pct)}
                  stroke="#10b981"
                  strokeWidth="2"
                  strokeDasharray="2,2"
                />
                <circle cx={cx} cy={scaleY(stop.departure_soc_pct)} r="4" fill="#047857" stroke="#ffffff" strokeWidth="1.5" />
              </g>
            );
          })}

          {/* X Axis distance marks */}
          {[0, 0.25, 0.5, 0.75, 1.0].map((frac) => {
            const dist = maxDist * frac;
            return (
              <text
                key={frac}
                x={scaleX(dist)}
                y={chartHeight - 10}
                fontSize="9"
                fill="currentColor"
                textAnchor="middle"
                className="font-mono"
              >
                {dist.toFixed(0)} km
              </text>
            );
          })}
        </svg>
      </div>
    </div>
  );
}
