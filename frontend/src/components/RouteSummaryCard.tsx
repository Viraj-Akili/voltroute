'use client';

import React from 'react';
import { RouteSummary, RouteLocation } from '../lib/types';

interface RouteSummaryCardProps {
  summary: RouteSummary;
  origin: RouteLocation;
  destination: RouteLocation;
}

export default function RouteSummaryCard({
  summary,
  origin,
  destination,
}: RouteSummaryCardProps) {
  const formatTime = (minutes: number) => {
    const hrs = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    if (hrs === 0) return `${mins} min`;
    return `${hrs} hr ${mins > 0 ? `${mins} min` : ''}`;
  };

  const originShort = origin.name.split(',')[0].trim();
  const destShort = destination.name.split(',')[0].trim();

  return (
    <div className="absolute left-3 top-3 z-10 min-w-[240px] max-w-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white/95 dark:bg-slate-900/95 p-3.5 shadow-md backdrop-blur-md transition-colors">
      <div>
        <h3 className="text-xs font-bold text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
          <span>{originShort}</span>
          <span className="text-slate-400 font-normal">→</span>
          <span>{destShort}</span>
        </h3>
        <div className="mt-1.5 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs font-medium text-slate-600 dark:text-slate-300">
          <span>{summary.total_distance_km.toFixed(0)} km</span>
          <span className="text-slate-300 dark:text-slate-600">•</span>
          <span>{formatTime(summary.total_trip_time_min)}</span>
          <span className="text-slate-300 dark:text-slate-600">•</span>
          <span className="font-semibold text-emerald-600 dark:text-emerald-400">
            {summary.num_stops === 0
              ? 'No charging stops'
              : `${summary.num_stops} stop${summary.num_stops > 1 ? 's' : ''}`}
          </span>
        </div>
        <div className="mt-2 pt-2 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-slate-500 dark:text-slate-400">
          <span>
            Arrival: <strong className="text-slate-700 dark:text-slate-200">{summary.final_battery_pct.toFixed(0)}% battery</strong>
          </span>
          {summary.total_charging_cost_usd > 0 && (
            <span>
              Est. cost: <strong className="text-slate-700 dark:text-slate-200">₹{Math.round(summary.total_charging_cost_usd)}</strong>
            </span>
          )}
          {summary.co2_saved_kg > 0 && (
            <span>
              CO₂ saved: <strong className="text-emerald-600 dark:text-emerald-400">{summary.co2_saved_kg.toFixed(1)} kg</strong>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

