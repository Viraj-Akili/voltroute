'use client';

import React from 'react';

interface DemoRouteItem {
  id: string;
  title: string;
  region: string;
  start_location: string;
  start_lat?: number;
  start_lng?: number;
  destination: string;
  dest_lat?: number;
  dest_lng?: number;
  distance: string;
  vehicle_model: string;
  battery_capacity_kwh: number;
  vehicle_efficiency_wh_per_km: number;
  current_battery_pct: number;
  badge: string;
  description: string;
}

const DEMO_ROUTES: DemoRouteItem[] = [
  {
    id: 'vellore-chennai',
    title: 'Vellore ➔ Chennai',
    region: 'Tamil Nadu, India',
    start_location: 'Vellore, Tamil Nadu, India',
    start_lat: 12.9165,
    start_lng: 79.1325,
    destination: 'Chennai, Tamil Nadu, India',
    dest_lat: 13.0827,
    dest_lng: 80.2707,
    distance: '138 km',
    vehicle_model: 'Tata Nexon EV Long Range',
    battery_capacity_kwh: 40.5,
    vehicle_efficiency_wh_per_km: 143,
    current_battery_pct: 70,
    badge: 'Direct / 0 Stops',
    description: 'NH 48 expressway route connecting VIT Vellore to Chennai Marina & IT Corridor.',
  },
  {
    id: 'vellore-bangalore',
    title: 'Vellore ➔ Bengaluru',
    region: 'TN & Karnataka, India',
    start_location: 'Vellore, Tamil Nadu, India',
    start_lat: 12.9165,
    start_lng: 79.1325,
    destination: 'Bengaluru, Karnataka, India',
    dest_lat: 12.9716,
    dest_lng: 77.5946,
    distance: '189 km',
    vehicle_model: 'Tata Nexon EV Long Range',
    battery_capacity_kwh: 40.5,
    vehicle_efficiency_wh_per_km: 143,
    current_battery_pct: 50,
    badge: '1 Fast Charging Stop',
    description: 'High-speed highway with fast chargers in Ambur / Krishnagiri corridor.',
  },
  {
    id: 'vellore-tirupati',
    title: 'Vellore ➔ Tirupati',
    region: 'TN & Andhra Pradesh, India',
    start_location: 'Vellore, Tamil Nadu, India',
    start_lat: 12.9165,
    start_lng: 79.1325,
    destination: 'Tirupati, Andhra Pradesh, India',
    dest_lat: 13.6288,
    dest_lng: 79.4192,
    distance: '108 km',
    vehicle_model: 'MG ZS EV',
    battery_capacity_kwh: 50.3,
    vehicle_efficiency_wh_per_km: 156,
    current_battery_pct: 80,
    badge: 'Direct Scenic Route',
    description: 'Chittoor highway route connecting Vellore with Sri Venkateswara Temple foothills.',
  },
  {
    id: 'chennai-bangalore',
    title: 'Chennai ➔ Bengaluru',
    region: 'South India Highway',
    start_location: 'Chennai, Tamil Nadu, India',
    start_lat: 13.0827,
    start_lng: 80.2707,
    destination: 'Bengaluru, Karnataka, India',
    dest_lat: 12.9716,
    dest_lng: 77.5946,
    distance: '346 km',
    vehicle_model: 'Mahindra XUV400 EL Pro',
    battery_capacity_kwh: 39.4,
    vehicle_efficiency_wh_per_km: 150,
    current_battery_pct: 75,
    badge: '2 Fast Charging Stops',
    description: 'Major industrial corridor passing Kanchipuram, Ranipet, Vellore & Hosur.',
  },
  {
    id: 'vellore-pondicherry',
    title: 'Vellore ➔ Pondicherry',
    region: 'Tamil Nadu & Puducherry',
    start_location: 'Vellore, Tamil Nadu, India',
    start_lat: 12.9165,
    start_lng: 79.1325,
    destination: 'Pondicherry, Puducherry, India',
    dest_lat: 11.9416,
    dest_lng: 79.8083,
    distance: '155 km',
    vehicle_model: 'Tata Punch EV Long Range',
    battery_capacity_kwh: 35.0,
    vehicle_efficiency_wh_per_km: 135,
    current_battery_pct: 65,
    badge: 'Coastal Weekend Trip',
    description: 'Scenic drive via Arani and Tindivanam to the French Quarter promenade.',
  },
  {
    id: 'london-manchester',
    title: 'London ➔ Manchester',
    region: 'United Kingdom (Global Demo)',
    start_location: 'London, UK',
    start_lat: 51.5074,
    start_lng: -0.1278,
    destination: 'Manchester, UK',
    dest_lat: 53.4808,
    dest_lng: -2.2426,
    distance: '335 km',
    vehicle_model: 'Tesla Model 3 Long Range',
    battery_capacity_kwh: 75.0,
    vehicle_efficiency_wh_per_km: 150,
    current_battery_pct: 60,
    badge: 'M1 / M6 Corridor',
    description: 'High-power Ionity and Gridserve motorway service hubs test route.',
  },
];

interface DemoRoutesModalProps {
  onClose: () => void;
  onSelectRoute: (route: DemoRouteItem) => void;
}

export default function DemoRoutesModal({ onClose, onSelectRoute }: DemoRoutesModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden shadow-2xl flex flex-col">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <span>🛣️</span> Select a Popular EV Road Trip
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              1-Click testing with real Indian EV models and verified corridor fast chargers
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* List of Routes */}
        <div className="p-4 sm:p-5 overflow-y-auto space-y-3">
          {DEMO_ROUTES.map((route) => (
            <div
              key={route.id}
              onClick={() => onSelectRoute(route)}
              className="p-3.5 bg-slate-50 dark:bg-slate-800/50 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 border border-slate-200 dark:border-slate-700/70 hover:border-emerald-500 rounded-xl cursor-pointer transition-all group"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                    {route.title}
                  </h4>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-semibold border border-emerald-200 dark:border-emerald-800/60">
                    {route.badge}
                  </span>
                </div>
                <span className="text-xs font-mono font-bold text-slate-500">{route.distance}</span>
              </div>

              <p className="text-xs text-slate-600 dark:text-slate-300 mt-1">{route.description}</p>

              <div className="flex flex-wrap items-center gap-3 mt-2.5 pt-2 border-t border-slate-200/60 dark:border-slate-700/40 text-[11px] text-slate-500 dark:text-slate-400">
                <span>🚗 {route.vehicle_model}</span>
                <span>🔋 Battery: {route.current_battery_pct}%</span>
                <span>📍 {route.region}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
