'use client';

import React from 'react';
import { RouteLeg, RouteStop, RouteLocation } from '../lib/types';

interface ItineraryTimelineProps {
  legs: RouteLeg[];
  stops: RouteStop[];
  origin: RouteLocation;
  destination: RouteLocation;
  onHoverStop?: (index: number | null) => void;
  onSelectStop?: (stop: RouteStop) => void;
}

export default function ItineraryTimeline({
  legs,
  stops,
  origin,
  destination,
  onHoverStop,
  onSelectStop,
}: ItineraryTimelineProps) {
  const formatTime = (minutes: number) => {
    const hrs = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    if (hrs === 0) return `${mins} min`;
    return `${hrs} hr ${mins > 0 ? `${mins} min` : ''}`;
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4 transition-colors">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
          Trip Itinerary
        </h3>
        <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
          {stops.length === 0
            ? 'Direct trip (0 stops)'
            : `${stops.length} stop${stops.length > 1 ? 's' : ''}`}
        </span>
      </div>

      <div className="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200 dark:before:bg-slate-800">
        {/* Origin / Start */}
        <div className="relative">
          <span className="absolute -left-6 top-0.5 w-4 h-4 rounded-full bg-blue-500 border-2 border-white dark:border-slate-900 flex items-center justify-center text-white text-[9px] font-bold shadow-sm">
            ●
          </span>
          <div>
            <p className="text-xs font-bold text-slate-900 dark:text-slate-100 leading-tight">
              {origin.name}
            </p>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Start location</p>
          </div>
        </div>

        {/* Driving Legs & Charging Stops */}
        {legs.map((leg, idx) => {
          const matchingStop = stops[idx];
          return (
            <div key={idx} className="space-y-3">
              {/* Driving distance / time */}
              <div className="text-[11px] text-slate-500 dark:text-slate-400 flex items-center gap-1.5 font-medium py-0.5">
                <span>🚗 Drive {leg.distance_km.toFixed(0)} km</span>
                <span>•</span>
                <span>{formatTime(leg.duration_min)}</span>
              </div>

              {/* Recommended Stop Card */}
              {matchingStop && (
                <div
                  onMouseEnter={() => onHoverStop && onHoverStop(idx)}
                  onMouseLeave={() => onHoverStop && onHoverStop(null)}
                  onClick={() => onSelectStop && onSelectStop(matchingStop)}
                  className="p-3.5 bg-emerald-50/60 dark:bg-emerald-950/20 rounded-xl border border-emerald-200/80 dark:border-emerald-800/50 hover:border-emerald-400 transition-colors cursor-pointer shadow-sm group"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-emerald-600 inline-block"></span>
                        <span className="text-[10px] font-bold text-emerald-700 dark:text-emerald-300 uppercase tracking-wider">
                          Recommended stop {idx + 1}
                        </span>
                      </div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100 mt-0.5 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                        {matchingStop.station.name}
                      </h4>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                        {matchingStop.station.operator}
                        {matchingStop.station.city ? ` • ${matchingStop.station.city}` : ''}
                      </p>
                    </div>

                    <a
                      href={`https://www.google.com/maps/dir/?api=1&destination=${matchingStop.station.latitude},${matchingStop.station.longitude}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="px-2.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white text-xs font-bold rounded-lg shadow-sm flex items-center gap-1 transition-colors flex-shrink-0"
                    >
                      Navigate
                    </a>
                  </div>

                  <div className="grid grid-cols-3 gap-2 mt-3 pt-2.5 border-t border-emerald-200/60 dark:border-emerald-800/40 text-[11px]">
                    <div>
                      <span className="text-slate-500 dark:text-slate-400 text-[10px] block">Arrival SOC</span>
                      <span className="font-bold text-slate-800 dark:text-slate-200">
                        {matchingStop.arrival_soc_pct.toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-500 dark:text-slate-400 text-[10px] block">Charge to</span>
                      <span className="font-bold text-emerald-600 dark:text-emerald-400">
                        {matchingStop.departure_soc_pct.toFixed(0)}% ({matchingStop.charge_duration_min.toFixed(0)} min)
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-500 dark:text-slate-400 text-[10px] block">Estimated cost</span>
                      <span className="font-bold text-slate-800 dark:text-slate-200">
                        ₹{Math.round(matchingStop.estimated_cost_usd)}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {/* Destination */}
        <div className="relative">
          <span className="absolute -left-6 top-0.5 w-4 h-4 rounded-full bg-red-500 border-2 border-white dark:border-slate-900 flex items-center justify-center text-white text-[9px] font-bold shadow-sm">
            ●
          </span>
          <div>
            <p className="text-xs font-bold text-slate-900 dark:text-slate-100 leading-tight">
              {destination.name}
            </p>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Destination</p>
          </div>
        </div>
      </div>
    </div>
  );
}
