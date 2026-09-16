"use client";

import React from "react";
import { Zap, Activity, Compass, Info, Sparkles, Navigation } from "lucide-react";

interface HeaderProps {
  backendStatus: "online" | "offline" | "checking";
  stationCount: number;
  onOpenDemoModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  backendStatus,
  stationCount,
  onOpenDemoModal,
}) => {
  return (
    <header className="sticky top-0 z-30 w-full glass-panel border-b border-white/10 px-4 lg:px-8 py-3 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand Logo */}
        <div className="flex items-center space-x-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-volt-500 to-electric-cyan p-0.5 shadow-volt-glow">
            <div className="w-full h-full bg-space-900 rounded-[10px] flex items-center justify-center">
              <Zap className="w-5 h-5 text-volt-400 fill-volt-400 animate-pulse-subtle" />
            </div>
            <div className="absolute -inset-0.5 bg-volt-500 rounded-xl blur opacity-30 animate-pulse"></div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-volt-300 bg-clip-text text-transparent">
                VoltRoute
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-volt-500/10 text-volt-400 border border-volt-500/20">
                AI EV Planner
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Intelligent Energy Simulation & Fast-Charging Optimization
            </p>
          </div>
        </div>

        {/* Action Controls & Backend Status */}
        <div className="flex items-center space-x-3 sm:space-x-4">
          {/* Quick Demo Road Trips */}
          <button
            onClick={onOpenDemoModal}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-xs sm:text-sm font-medium text-volt-300 border border-volt-500/30 hover:border-volt-500/60 shadow-sm transition-all hover:shadow-volt-glow"
          >
            <Sparkles className="w-4 h-4 text-volt-400" />
            <span className="hidden xs:inline">Popular Trips</span>
            <span className="xs:hidden">Trips</span>
          </button>

          {/* Live Station DB Status */}
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-space-850/80 border border-white/5 text-xs text-slate-300">
            <span className="relative flex h-2 w-2">
              {backendStatus === "online" ? (
                <>
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-volt-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-volt-500"></span>
                </>
              ) : backendStatus === "checking" ? (
                <span className="relative inline-flex rounded-full h-2 w-2 bg-yellow-400 animate-pulse"></span>
              ) : (
                <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
              )}
            </span>
            <span className="hidden sm:inline">
              {backendStatus === "online"
                ? `${stationCount > 0 ? stationCount : "250+"} High-Speed Chargers`
                : backendStatus === "checking"
                ? "Connecting..."
                : "FastAPI Backend Offline"}
            </span>
            <span className="sm:hidden">
              {backendStatus === "online" ? "Online" : "Offline"}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
