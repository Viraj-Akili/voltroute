'use client';

import React, { useEffect, useState } from 'react';
import { useMapsLibrary } from '@vis.gl/react-google-maps';
import PlaceAutocompleteInput from './PlaceAutocompleteInput';
import { RouteRequest, VehiclePreset } from '../lib/types';
import { getVehiclePresets } from '../lib/api';

interface RoutePlannerFormProps {
  formData: RouteRequest;
  onChange: (data: RouteRequest) => void;
  onSubmit: (data: RouteRequest) => void;
  onOpenCustomVehicleModal: () => void;
  isLoading: boolean;
  customVehicles: VehiclePreset[];
}

const QUICK_TRIPS = [
  { title: 'Vellore → Chennai', from: 'Vellore, Tamil Nadu, India', to: 'Chennai, Tamil Nadu, India', fromLat: 12.9165, fromLng: 79.1325, toLat: 13.0827, toLng: 80.2707 },
  { title: 'Vellore → Bengaluru', from: 'Vellore, Tamil Nadu, India', to: 'Bengaluru, Karnataka, India', fromLat: 12.9165, fromLng: 79.1325, toLat: 12.9716, toLng: 77.5946 },
  { title: 'Vellore → Tirupati', from: 'Vellore, Tamil Nadu, India', to: 'Tirupati, Andhra Pradesh, India', fromLat: 12.9165, fromLng: 79.1325, toLat: 13.6288, toLng: 79.4192 },
];

export default function RoutePlannerForm({
  formData,
  onChange,
  onSubmit,
  onOpenCustomVehicleModal,
  isLoading,
  customVehicles,
}: RoutePlannerFormProps) {
  const placesLibrary = useMapsLibrary('places');
  const [presets, setPresets] = useState<VehiclePreset[]>([]);

  useEffect(() => {
    getVehiclePresets()
      .then(setPresets)
      .catch((err) => console.warn('Could not load vehicle presets:', err));
  }, []);

  const allAvailableVehicles = [...presets, ...customVehicles];

  const updateLocation = (
    field: 'start' | 'destination',
    place: { name: string; formatted_address?: string; lat?: number; lng?: number }
  ) => {
    if (field === 'start') {
      onChange({
        ...formData,
        start_location: place.formatted_address || place.name,
        start_lat: place.lat,
        start_lng: place.lng,
      });
    } else {
      onChange({
        ...formData,
        destination: place.formatted_address || place.name,
        dest_lat: place.lat,
        dest_lng: place.lng,
      });
    }
  };

  const selectQuickTrip = async (trip: typeof QUICK_TRIPS[0]) => {
    if (placesLibrary?.Place) {
      try {
        const [fromResult, toResult] = await Promise.all([
          placesLibrary.Place.searchByText({ textQuery: trip.from, fields: ['id', 'displayName', 'formattedAddress', 'location'] }),
          placesLibrary.Place.searchByText({ textQuery: trip.to, fields: ['id', 'displayName', 'formattedAddress', 'location'] }),
        ]);
        const origin = fromResult?.places?.[0];
        const destination = toResult?.places?.[0];
        if (origin && destination) {
          onChange({
            ...formData,
            start_location: origin.formattedAddress || origin.displayName || trip.from,
            start_lat: origin.location?.lat() ?? trip.fromLat,
            start_lng: origin.location?.lng() ?? trip.fromLng,
            destination: destination.formattedAddress || destination.displayName || trip.to,
            dest_lat: destination.location?.lat() ?? trip.toLat,
            dest_lng: destination.location?.lng() ?? trip.toLng,
          });
          return;
        }
      } catch (error) {
        console.warn('Google Places search fallback to standard coordinates:', error);
      }
    }

    // Direct fallback if places library is pending or unavailable
    onChange({
      ...formData,
      start_location: trip.from,
      start_lat: trip.fromLat,
      start_lng: trip.fromLng,
      destination: trip.to,
      dest_lat: trip.toLat,
      dest_lng: trip.toLng,
    });
  };

  const handleVehicleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    if (event.target.value === '__custom_modal__') {
      onOpenCustomVehicleModal();
      return;
    }
    const matched = allAvailableVehicles.find(
      (vehicle) => vehicle.model === event.target.value || vehicle.id === event.target.value
    );
    onChange({
      ...formData,
      vehicle_model: matched?.model || event.target.value,
      battery_capacity_kwh: matched?.battery_capacity_kwh || formData.battery_capacity_kwh,
      vehicle_efficiency_wh_per_km: matched?.efficiency_wh_per_km || formData.vehicle_efficiency_wh_per_km,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm space-y-5 transition-colors">
      <div>
        <h2 className="text-base font-bold text-slate-900 dark:text-slate-100">
          Plan your EV trip
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
          Enter your route and vehicle details to calculate charging stops.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* From */}
        <PlaceAutocompleteInput
          id="origin-input"
          label="From"
          placeholder="Starting city or address"
          value={typeof formData.start_location === 'string' ? formData.start_location : ''}
          icon="🔵"
          required
          onChangeText={(text) =>
            onChange({ ...formData, start_location: text, start_lat: undefined, start_lng: undefined })
          }
          onSelectPlace={(place) => updateLocation('start', place)}
        />

        {/* To */}
        <PlaceAutocompleteInput
          id="destination-input"
          label="To"
          placeholder="Destination city or address"
          value={typeof formData.destination === 'string' ? formData.destination : ''}
          icon="🔴"
          required
          onChangeText={(text) =>
            onChange({ ...formData, destination: text, dest_lat: undefined, dest_lng: undefined })
          }
          onSelectPlace={(place) => updateLocation('destination', place)}
        />

        {/* Quick Trips Shortcuts */}
        <div>
          <span className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1.5">
            Quick trips
          </span>
          <div className="flex flex-wrap gap-1.5">
            {QUICK_TRIPS.map((trip) => (
              <button
                key={trip.title}
                type="button"
                onClick={() => selectQuickTrip(trip)}
                className="px-2.5 py-1 text-xs font-medium rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition-colors"
              >
                {trip.title}
              </button>
            ))}
          </div>
        </div>

        {/* Vehicle */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label htmlFor="vehicle-model" className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
              Vehicle <span className="text-emerald-500">*</span>
            </label>
            <button
              type="button"
              onClick={onOpenCustomVehicleModal}
              className="text-xs font-semibold text-emerald-600 hover:text-emerald-700 dark:text-emerald-400"
            >
              + Custom EV
            </button>
          </div>
          <select
            id="vehicle-model"
            value={formData.vehicle_model}
            onChange={handleVehicleChange}
            className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500 transition-colors font-medium"
          >
            {presets.map((preset) => (
              <option key={preset.id} value={preset.model}>
                {preset.model} ({preset.battery_capacity_kwh} kWh)
              </option>
            ))}
            {customVehicles.map((vehicle) => (
              <option key={vehicle.id} value={vehicle.model}>
                {vehicle.name} ({vehicle.battery_capacity_kwh} kWh)
              </option>
            ))}
            <option value="__custom_modal__">+ Add custom vehicle...</option>
          </select>
        </div>

        {/* Battery */}
        <div>
          <div className="flex items-center justify-between mb-1">
            <label htmlFor="current-battery" className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
              Starting Battery
            </label>
            <output htmlFor="current-battery" className="text-sm font-bold text-emerald-600 dark:text-emerald-400">
              {formData.current_battery_pct}%
            </output>
          </div>
          {(() => {
            const min = 10;
            const max = 100;
            const currentVal = Math.min(max, Math.max(min, formData.current_battery_pct ?? 70));
            const fillPercent = ((currentVal - min) / (max - min)) * 100;
            return (
              <input
                id="current-battery"
                type="range"
                min={min}
                max={max}
                step="1"
                value={currentVal}
                onChange={(event) =>
                  onChange({ ...formData, current_battery_pct: Number(event.target.value) })
                }
                style={{
                  background: `linear-gradient(to right, var(--accent-emerald) 0%, var(--accent-emerald) ${fillPercent}%, var(--border-color) ${fillPercent}%, var(--border-color) 100%)`,
                }}
                className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-emerald-600"
              />
            );
          })()}
          <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-medium">
            <span>10% (Low)</span>
            <span>50%</span>
            <span>100% (Full)</span>
          </div>
        </div>

        {/* Trip Preference */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
            Trip Preference
          </label>
          <div className="grid grid-cols-3 gap-1.5">
            {[
              { id: 'fastest', label: 'Fastest', desc: 'High kW' },
              { id: 'cheapest', label: 'Cheapest', desc: 'Lowest ₹' },
              { id: 'fewest_stops', label: 'Fewest Stops', desc: 'Max leg' },
            ].map((mode) => {
              const active = (formData.optimization_mode || 'fastest') === mode.id;
              return (
                <button
                  key={mode.id}
                  type="button"
                  onClick={() => onChange({ ...formData, optimization_mode: mode.id as any })}
                  className={`py-2 px-2 rounded-xl text-xs font-semibold border transition-all text-center ${
                    active
                      ? 'bg-emerald-50 dark:bg-emerald-950/50 border-emerald-500 text-emerald-700 dark:text-emerald-300 shadow-sm'
                      : 'bg-slate-50 dark:bg-slate-800/80 border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <div>{mode.label}</div>
                  <div className="text-[10px] font-normal opacity-75">{mode.desc}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Plan Route Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 disabled:opacity-60 text-white font-bold text-sm rounded-xl shadow-sm transition-colors flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>Planning route...</span>
            </>
          ) : (
            <span>Plan Route</span>
          )}
        </button>
      </form>
    </div>
  );
}
