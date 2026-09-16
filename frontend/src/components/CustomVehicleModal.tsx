'use client';

import React, { useState } from 'react';
import { VehiclePreset } from '../lib/types';

interface CustomVehicleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (vehicle: VehiclePreset) => void;
}

export default function CustomVehicleModal({
  isOpen,
  onClose,
  onSave,
}: CustomVehicleModalProps) {
  const [name, setName] = useState('My EV');
  const [batteryCapacity, setBatteryCapacity] = useState<string>('40.5');
  const [efficiency, setEfficiency] = useState<string>('138');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [maxPower, setMaxPower] = useState<string>('50');
  const [connectorType, setConnectorType] = useState('CCS2');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    const trimmedName = name.trim();
    if (!trimmedName) {
      setErrorMessage('Please enter your vehicle name.');
      return;
    }

    const capacityNum = parseFloat(batteryCapacity);
    if (isNaN(capacityNum) || capacityNum <= 0) {
      setErrorMessage('Please enter a valid battery capacity.');
      return;
    }
    if (capacityNum < 5 || capacityNum > 250) {
      setErrorMessage('Please enter a realistic battery capacity (e.g. 20 to 120 kWh).');
      return;
    }

    const efficiencyNum = parseFloat(efficiency);
    if (isNaN(efficiencyNum) || efficiencyNum <= 0) {
      setErrorMessage("Please enter your vehicle's energy efficiency.");
      return;
    }
    if (efficiencyNum < 50 || efficiencyNum > 400) {
      setErrorMessage('Please enter a realistic energy efficiency (e.g. 100 to 250 Wh/km).');
      return;
    }

    const maxPowerNum = parseFloat(maxPower) || 50;

    const customVehicle: VehiclePreset = {
      id: `custom-${Date.now()}`,
      name: trimmedName,
      make: 'Custom',
      model: trimmedName,
      year: new Date().getFullYear(),
      battery_capacity_kwh: capacityNum,
      efficiency_wh_per_km: efficiencyNum,
      max_charge_rate_kw: maxPowerNum,
      max_charging_power_kw: maxPowerNum,
      supported_connectors: [connectorType, 'Type 2'],
      description: `Custom ${trimmedName} (${capacityNum} kWh)`,
    };

    onSave(customVehicle);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-md w-full overflow-hidden shadow-xl">
        {/* Modal Header */}
        <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex items-start justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
              Add custom vehicle
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Enter your battery specifications to calculate charging stops accurately.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className="w-7 h-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-sm"
          >
            ✕
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          {errorMessage && (
            <div className="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/60 text-rose-700 dark:text-rose-300 text-xs">
              {errorMessage}
            </div>
          )}

          {/* 1. Vehicle Name */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">
              Vehicle name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. My EV"
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500 transition-colors placeholder:text-slate-400"
            />
          </div>

          {/* 2. Battery Capacity */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Battery capacity
              </label>
              <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">kWh</span>
            </div>
            <input
              type="number"
              step="0.1"
              value={batteryCapacity}
              onChange={(e) => setBatteryCapacity(e.target.value)}
              placeholder="40.5"
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500 transition-colors font-medium"
            />
          </div>

          {/* 3. Energy Efficiency */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Energy efficiency
              </label>
              <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">Wh/km</span>
            </div>
            <input
              type="number"
              step="1"
              value={efficiency}
              onChange={(e) => setEfficiency(e.target.value)}
              placeholder="138"
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-500 transition-colors font-medium"
            />
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
              Typical highway consumption (e.g. 130 to 180 Wh/km).
            </p>
          </div>

          {/* Collapsible Optional Advanced Settings */}
          <div className="pt-1">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-emerald-600 flex items-center gap-1 transition-colors"
            >
              <span>{showAdvanced ? '▾' : '▸'} Advanced settings</span>
            </button>

            {showAdvanced && (
              <div className="mt-2.5 p-3.5 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700 space-y-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 dark:text-slate-400 mb-1">
                    Maximum charging speed (kW)
                  </label>
                  <input
                    type="number"
                    value={maxPower}
                    onChange={(e) => setMaxPower(e.target.value)}
                    placeholder="50"
                    className="w-full px-3 py-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500/30"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 dark:text-slate-400 mb-1">
                    Connector type
                  </label>
                  <select
                    value={connectorType}
                    onChange={(e) => setConnectorType(e.target.value)}
                    className="w-full px-3 py-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500/30"
                  >
                    <option value="CCS2">CCS-2</option>
                    <option value="Type 2">Type 2</option>
                    <option value="GB/T">GB/T</option>
                    <option value="NACS">NACS</option>
                  </select>
                </div>
              </div>
            )}
          </div>

          {/* Submit Button */}
          <div className="pt-2">
            <button
              type="submit"
              className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white font-bold rounded-xl shadow-sm transition-colors text-sm"
            >
              Save Vehicle
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
