"use client";

import React, { useEffect, useRef, useState } from "react";
import {
  RouteResponse,
  ResolvedLocation,
  ChargingStop,
  StationResponse,
} from "../lib/types";
import {
  Maximize2,
  Layers,
  Zap,
  MapPin,
  Flag,
  Navigation,
  Compass,
} from "lucide-react";

interface MapComponentProps {
  routeData: RouteResponse | null;
  allCorridorStations?: StationResponse[];
  selectedStopIndex?: number | null;
  onSelectStop?: (stopIndex: number) => void;
}

export const MapComponent: React.FC<MapComponentProps> = ({
  routeData,
  allCorridorStations = [],
  selectedStopIndex,
  onSelectStop,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const layersGroupRef = useRef<any>(null);
  const [mapStyle, setMapStyle] = useState<"voyager" | "dark" | "osm">("voyager");
  const [tileLayerRef, setTileLayerRef] = useState<any>(null);

  // Initialize Map
  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapInstanceRef.current) return; // already initialized

    // Dynamic Leaflet import
    import("leaflet").then((L) => {
      // Fix default leaflet icons
      delete (L.Icon.Default.prototype as any)._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
      });

      // Default center: United States
      const map = L.map(mapContainerRef.current!, {
        center: [37.0902, -95.7129],
        zoom: 4,
        zoomControl: false,
      });

      // Add custom zoom control to top-right
      L.control.zoom({ position: "topright" }).addTo(map);

      // Tile Layer URL
      const tileUrl =
        mapStyle === "dark"
          ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          : mapStyle === "voyager"
          ? "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

      const tiles = L.tileLayer(tileUrl, {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
        maxZoom: 19,
      }).addTo(map);

      setTileLayerRef(tiles);

      // Feature group for markers & polylines
      const group = L.featureGroup().addTo(map);
      layersGroupRef.current = group;
      mapInstanceRef.current = map;
    });

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Update Tile Layer when style changes
  useEffect(() => {
    if (!mapInstanceRef.current) return;
    import("leaflet").then((L) => {
      const map = mapInstanceRef.current;
      map.eachLayer((layer: any) => {
        if (layer instanceof L.TileLayer) {
          map.removeLayer(layer);
        }
      });

      const tileUrl =
        mapStyle === "dark"
          ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          : mapStyle === "voyager"
          ? "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

      L.tileLayer(tileUrl, {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(map);
    });
  }, [mapStyle]);

  // Update Route Polyline & Markers when routeData changes
  useEffect(() => {
    if (!mapInstanceRef.current || !layersGroupRef.current) return;

    import("leaflet").then((L) => {
      const map = mapInstanceRef.current;
      const group = layersGroupRef.current;
      group.clearLayers();

      if (!routeData) {
        // Default overview if no route yet
        map.setView([37.0902, -95.7129], 4);
        return;
      }

      const { origin, destination, route_geometry, stops, candidate_stations } = routeData;

      // 1. Draw Other Candidate Stations along the corridor (dimmed dots)
      if (candidate_stations && candidate_stations.length > 0) {
        const stopStationIds = new Set(stops.map((st) => st.station.id));

        candidate_stations.forEach((cand) => {
          if (stopStationIds.has(cand.id)) return; // Skip planned stops (handled separately)

          const candIcon = L.divIcon({
            className: "custom-candidate-icon",
            html: `
              <div style="
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: #1e293b;
                border: 2px solid #64748b;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.5);
                cursor: pointer;
              ">
                <div style="width: 4px; height: 4px; border-radius: 50%; background: #94a3b8;"></div>
              </div>
            `,
            iconSize: [14, 14],
            iconAnchor: [7, 7],
          });

          const marker = L.marker([cand.latitude, cand.longitude], {
            icon: candIcon,
            title: cand.name,
          });

          marker.bindPopup(`
            <div style="font-family: sans-serif; min-width: 180px; padding: 2px;">
              <span style="font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Available Fast Charger</span>
              <h4 style="font-size: 13px; font-weight: 700; color: #ffffff; margin: 2px 0;">${cand.name}</h4>
              <p style="font-size: 11px; color: #94a3b8; margin: 0;">${cand.operator} • <strong style="color: #38bdf8;">${cand.power_kw} kW</strong></p>
              <p style="font-size: 11px; color: #cbd5e1; margin-top: 4px;">Detour: <strong>${cand.detour_km ?? 0} km</strong> from route</p>
            </div>
          `);

          group.addLayer(marker);
        });
      }

      // 2. Draw Route Polyline
      if (route_geometry && route_geometry.length > 1) {
        // Outer Glow line
        const glowLine = L.polyline(route_geometry, {
          color: "#06b6d4",
          weight: 7,
          opacity: 0.35,
          lineCap: "round",
          lineJoin: "round",
        });
        group.addLayer(glowLine);

        // Core line
        const mainLine = L.polyline(route_geometry, {
          color: "#10b981",
          weight: 4,
          opacity: 0.95,
          lineCap: "round",
          lineJoin: "round",
        });
        group.addLayer(mainLine);
      }

      // 3. Origin Marker
      const originIcon = L.divIcon({
        className: "custom-origin-icon",
        html: `
          <div style="
            position: relative;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
          ">
            <div style="
              position: absolute;
              width: 100%;
              height: 100%;
              border-radius: 50%;
              background: rgba(16, 185, 129, 0.3);
              animation: pulse 2s infinite;
            "></div>
            <div style="
              width: 24px;
              height: 24px;
              border-radius: 50%;
              background: #0f172a;
              border: 3px solid #10b981;
              display: flex;
              align-items: center;
              justify-content: center;
              box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
            ">
              <div style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></div>
            </div>
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
      });

      const originMarker = L.marker([origin.latitude, origin.longitude], {
        icon: originIcon,
        zIndexOffset: 1000,
      }).bindPopup(`
        <div style="font-family: sans-serif; min-width: 160px;">
          <span style="font-size: 10px; color: #10b981; font-weight: 800; text-transform: uppercase;">Origin</span>
          <h4 style="font-size: 13px; font-weight: 700; color: #fff; margin: 2px 0;">${origin.name}</h4>
          <p style="font-size: 11px; color: #94a3b8; margin: 0;">Start Battery: <strong>${routeData.summary.initial_battery_pct}%</strong></p>
        </div>
      `);
      group.addLayer(originMarker);

      // 4. Destination Marker
      const destIcon = L.divIcon({
        className: "custom-dest-icon",
        html: `
          <div style="
            position: relative;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
          ">
            <div style="
              width: 24px;
              height: 24px;
              border-radius: 50%;
              background: #0f172a;
              border: 3px solid #f43f5e;
              display: flex;
              align-items: center;
              justify-content: center;
              box-shadow: 0 0 12px rgba(244, 63, 94, 0.6);
            ">
              <div style="width: 8px; height: 8px; border-radius: 50%; background: #f43f5e;"></div>
            </div>
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
      });

      const destMarker = L.marker([destination.latitude, destination.longitude], {
        icon: destIcon,
        zIndexOffset: 1000,
      }).bindPopup(`
        <div style="font-family: sans-serif; min-width: 160px;">
          <span style="font-size: 10px; color: #f43f5e; font-weight: 800; text-transform: uppercase;">Final Destination</span>
          <h4 style="font-size: 13px; font-weight: 700; color: #fff; margin: 2px 0;">${destination.name}</h4>
          <p style="font-size: 11px; color: #94a3b8; margin: 0;">Arrival Battery: <strong style="color: #10b981;">${routeData.summary.final_battery_pct}%</strong></p>
        </div>
      `);
      group.addLayer(destMarker);

      // 5. Charging Stop Markers
      stops.forEach((stop) => {
        const isSelected = selectedStopIndex === stop.stop_index;
        const stopIcon = L.divIcon({
          className: "custom-stop-icon",
          html: `
            <div style="
              position: relative;
              width: 34px;
              height: 34px;
              display: flex;
              align-items: center;
              justify-content: center;
              cursor: pointer;
            ">
              <div style="
                position: absolute;
                inset: 0;
                border-radius: 50%;
                background: ${isSelected ? "rgba(6, 182, 212, 0.5)" : "rgba(16, 185, 129, 0.35)"};
                animation: pulse 1.5s infinite;
              "></div>
              <div style="
                width: 28px;
                height: 28px;
                border-radius: 50%;
                background: #0f172a;
                border: 2px solid ${isSelected ? "#38bdf8" : "#00f59b"};
                display: flex;
                align-items: center;
                justify-content: center;
                color: #ffffff;
                font-size: 11px;
                font-weight: 800;
                box-shadow: 0 0 14px ${isSelected ? "rgba(56, 189, 248, 0.8)" : "rgba(0, 245, 155, 0.6)"};
              ">
                ⚡${stop.stop_index}
              </div>
            </div>
          `,
          iconSize: [34, 34],
          iconAnchor: [17, 17],
        });

        const stopMarker = L.marker(
          [stop.station.latitude, stop.station.longitude],
          {
            icon: stopIcon,
            zIndexOffset: 1200,
          }
        );

        stopMarker.bindPopup(`
          <div style="font-family: sans-serif; min-width: 220px; padding: 2px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
              <span style="font-size: 10px; background: rgba(6, 182, 212, 0.2); color: #38bdf8; font-weight: 800; padding: 2px 6px; border-radius: 4px;">Stop #${stop.stop_index}</span>
              <span style="font-size: 10px; background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 800; padding: 2px 6px; border-radius: 4px;">${stop.station.power_kw} kW</span>
            </div>
            <h4 style="font-size: 13px; font-weight: 700; color: #ffffff; margin: 2px 0;">${stop.station.name}</h4>
            <p style="font-size: 11px; color: #94a3b8; margin: 0 0 6px 0;">${stop.station.operator} • ${stop.station.city}, ${stop.station.state}</p>
            
            <div style="background: rgba(15, 23, 42, 0.8); border-radius: 6px; padding: 6px; font-size: 11px; margin-bottom: 6px;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span style="color: #94a3b8;">Charge Duration:</span>
                <strong style="color: #00f59b;">${stop.charge_duration_min} min</strong>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span style="color: #94a3b8;">Battery Level:</span>
                <strong><span style="color: #fbbf24;">${stop.arrival_soc_pct}%</span> → <span style="color: #00f59b;">${stop.departure_soc_pct}%</span></strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: #94a3b8;">Energy & Cost:</span>
                <strong>+${stop.energy_added_kwh} kWh ($${stop.estimated_cost_usd.toFixed(2)})</strong>
              </div>
            </div>

            <p style="font-size: 10px; color: #64748b; margin: 0;">Plugs: ${stop.station.connector_types.join(", ")}</p>
          </div>
        `);

        stopMarker.on("click", () => {
          if (onSelectStop) onSelectStop(stop.stop_index);
        });

        group.addLayer(stopMarker);
      });

      // Fit map bounds to encompass full route with padding
      if (group.getLayers().length > 0) {
        map.fitBounds(group.getBounds(), {
          padding: [50, 50],
          maxZoom: 14,
        });
      }
    });
  }, [routeData, selectedStopIndex]);

  // Recenter map button handler
  const handleRecenter = () => {
    if (!mapInstanceRef.current || !layersGroupRef.current) return;
    const group = layersGroupRef.current;
    if (group.getLayers().length > 0) {
      mapInstanceRef.current.fitBounds(group.getBounds(), {
        padding: [50, 50],
        maxZoom: 14,
      });
    }
  };

  return (
    <div className="relative w-full h-full min-h-[420px] lg:min-h-[580px] rounded-2xl overflow-hidden glass-panel border border-white/10 shadow-card-glass">
      {/* Map Container */}
      <div ref={mapContainerRef} className="w-full h-full" />

      {/* Floating Map Controls */}
      <div className="absolute top-4 left-4 z-[400] flex items-center space-x-2">
        {/* Style Selector */}
        <div className="flex items-center bg-space-900/90 backdrop-blur-md rounded-xl p-1 border border-white/10 shadow-lg text-xs">
          <button
            onClick={() => setMapStyle("voyager")}
            className={`px-2.5 py-1 rounded-lg font-semibold transition-all ${
              mapStyle === "voyager"
                ? "bg-volt-500 text-space-900 shadow-volt-glow font-bold"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Light
          </button>
          <button
            onClick={() => setMapStyle("dark")}
            className={`px-2.5 py-1 rounded-lg font-semibold transition-all ${
              mapStyle === "dark"
                ? "bg-volt-500 text-space-900 shadow-volt-glow font-bold"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Dark
          </button>
          <button
            onClick={() => setMapStyle("osm")}
            className={`px-2.5 py-1 rounded-lg font-semibold transition-all ${
              mapStyle === "osm"
                ? "bg-volt-500 text-space-900 shadow-volt-glow font-bold"
                : "text-slate-400 hover:text-white"
            }`}
          >
            OSM
          </button>
        </div>

        {/* Recenter Button */}
        <button
          onClick={handleRecenter}
          title="Fit Route to View"
          className="p-2 rounded-xl bg-space-900/90 backdrop-blur-md text-slate-300 hover:text-volt-400 border border-white/10 shadow-lg hover:border-volt-500/30 transition-all hover:scale-105 active:scale-95"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      {/* Map Legend Overlay */}
      <div className="absolute bottom-4 left-4 z-[400] hidden sm:flex items-center space-x-3 bg-space-900/90 backdrop-blur-md px-3.5 py-2 rounded-xl border border-white/10 text-xs shadow-lg">
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 rounded-full bg-volt-400 border border-space-900 inline-block shadow-volt-glow"></span>
          <span className="text-slate-300 font-medium">Start</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3.5 h-3.5 rounded-full bg-space-850 border border-volt-400 flex items-center justify-center text-[9px] font-black text-volt-300">
            ⚡
          </span>
          <span className="text-slate-300 font-medium">Stop</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 rounded-full bg-rose-400 border border-space-900 inline-block"></span>
          <span className="text-slate-300 font-medium">Destination</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-slate-600 border border-slate-400 inline-block"></span>
          <span className="text-slate-400 text-[11px]">Corridor Charger</span>
        </div>
      </div>
    </div>
  );
};
