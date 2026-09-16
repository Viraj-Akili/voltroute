'use client';

import React, { useEffect, useRef, useState, useMemo } from 'react';
import { Map, useMap } from '@vis.gl/react-google-maps';
import { RouteResponse, ChargingStation, RouteStop } from '../lib/types';

// Subtle, clean dark mode styles for Google Maps
const darkMapStyles: google.maps.MapTypeStyle[] = [
  { elementType: 'geometry', stylers: [{ color: '#1e293b' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#0f172a' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#94a3b8' }] },
  {
    featureType: 'administrative.locality',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#cbd5e1' }],
  },
  {
    featureType: 'poi',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#64748b' }],
  },
  {
    featureType: 'poi.park',
    elementType: 'geometry',
    stylers: [{ color: '#14532d' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry',
    stylers: [{ color: '#334155' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry.stroke',
    stylers: [{ color: '#1e293b' }],
  },
  {
    featureType: 'road',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#94a3b8' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry',
    stylers: [{ color: '#475569' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry.stroke',
    stylers: [{ color: '#0f172a' }],
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{ color: '#0f172a' }],
  },
  {
    featureType: 'water',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#475569' }],
  },
];

interface MapComponentProps {
  theme: 'light' | 'dark';
  routeData: RouteResponse | null;
  allStations: ChargingStation[];
  showAllStations: boolean;
  selectedStation: ChargingStation | null;
  onSelectStation: (station: ChargingStation | null) => void;
  highlightedStopIndex: number | null;
  apiKeyMissing?: boolean;
}

export default function MapComponent({
  theme,
  routeData,
  allStations,
  showAllStations,
  selectedStation,
  onSelectStation,
  highlightedStopIndex,
  apiKeyMissing,
}: MapComponentProps) {
  const map = useMap();
  const polylineRef = useRef<google.maps.Polyline | null>(null);
  const markersRef = useRef<{ type: string; marker: google.maps.Marker }[]>([]);
  const infoWindowRef = useRef<google.maps.InfoWindow | null>(null);
  const markerPositionsRef = useRef<Record<string, google.maps.LatLngLiteral[]>>({
    charging: [],
    recommended: [],
    start: [],
    destination: [],
  });

  // Toggles for legend categories
  const [visibleLayers, setVisibleLayers] = useState({
    charging: true,
    recommended: true,
    start: true,
    destination: true,
  });

  // Default Center: Vellore, Tamil Nadu, India
  const defaultCenter = useMemo(() => ({ lat: 12.9165, lng: 79.1325 }), []);

  // Update theme styles on map
  useEffect(() => {
    if (!map) return;
    map.setOptions({
      styles: theme === 'dark' ? darkMapStyles : null,
    });
  }, [map, theme]);

  // Render Polylines and Markers
  useEffect(() => {
    if (!map || !window.google?.maps) return;

    // 1. Clear existing markers
    markersRef.current.forEach((item) => item.marker.setMap(null));
    markersRef.current = [];

    // 2. Clear existing polyline
    if (polylineRef.current) {
      polylineRef.current.setMap(null);
      polylineRef.current = null;
    }

    // 3. Clear InfoWindow
    if (infoWindowRef.current) {
      infoWindowRef.current.close();
    }
    infoWindowRef.current = new window.google.maps.InfoWindow();

    const bounds = new window.google.maps.LatLngBounds();
    let hasPointsToFit = false;
    markerPositionsRef.current = { charging: [], recommended: [], start: [], destination: [] };

    // A. Draw Route Polyline if available
    const coords = routeData?.route_geometry || (routeData as any)?.geometry?.coordinates;
    if (coords && coords.length > 0) {
      const path: google.maps.LatLngLiteral[] = coords.map((coord: any) => ({
        lat: Number(coord[0]),
        lng: Number(coord[1]),
      }));

      polylineRef.current = new window.google.maps.Polyline({
        path,
        geodesic: true,
        strokeColor: '#059669', // Restrained emerald green
        strokeOpacity: 0.95,
        strokeWeight: 5,
        map,
      });

      path.forEach((pt: google.maps.LatLngLiteral) => {
        bounds.extend(pt);
        hasPointsToFit = true;
      });
    }

    // B. Draw Start Marker (🔵 Blue)
    if (routeData?.origin && visibleLayers.start) {
      const originPos = { lat: routeData.origin.latitude, lng: routeData.origin.longitude };
      markerPositionsRef.current.start.push(originPos);
      bounds.extend(originPos);
      hasPointsToFit = true;

      const originMarker = new window.google.maps.Marker({
        position: originPos,
        map,
        title: `Start: ${routeData.origin.name}`,
        icon: {
          path: window.google.maps.SymbolPath.CIRCLE,
          scale: 9,
          fillColor: '#2563eb', // Blue
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2.5,
        },
      });

      originMarker.addListener('click', () => {
        infoWindowRef.current?.setContent(`
          <div style="font-family: inherit; padding: 6px 8px; color: #0f172a; max-width: 220px;">
            <div style="font-size: 11px; font-weight: 700; color: #2563eb; text-transform: uppercase;">🔵 Start</div>
            <div style="font-size: 13px; font-weight: 700; margin-top: 2px;">${routeData.origin.name}</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Departure point with initial battery.</div>
          </div>
        `);
        infoWindowRef.current?.open(map, originMarker);
      });
      markersRef.current.push({ type: 'start', marker: originMarker });
    }

    // C. Draw Destination Marker (🔴 Red)
    if (routeData?.destination && visibleLayers.destination) {
      const destPos = { lat: routeData.destination.latitude, lng: routeData.destination.longitude };
      markerPositionsRef.current.destination.push(destPos);
      bounds.extend(destPos);
      hasPointsToFit = true;

      const destMarker = new window.google.maps.Marker({
        position: destPos,
        map,
        title: `Destination: ${routeData.destination.name}`,
        icon: {
          path: window.google.maps.SymbolPath.CIRCLE,
          scale: 9,
          fillColor: '#dc2626', // Red
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2.5,
        },
      });

      destMarker.addListener('click', () => {
        infoWindowRef.current?.setContent(`
          <div style="font-family: inherit; padding: 6px 8px; color: #0f172a; max-width: 220px;">
            <div style="font-size: 11px; font-weight: 700; color: #dc2626; text-transform: uppercase;">🔴 Destination</div>
            <div style="font-size: 13px; font-weight: 700; margin-top: 2px;">${routeData.destination.name}</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Estimated arrival with ~${routeData.summary.final_battery_pct.toFixed(0)}% battery.</div>
          </div>
        `);
        infoWindowRef.current?.open(map, destMarker);
      });
      markersRef.current.push({ type: 'destination', marker: destMarker });
    }

    // D. Draw Recommended Stops (🟢 Green Markers)
    if (routeData?.stops && routeData.stops.length > 0 && visibleLayers.recommended) {
      routeData.stops.forEach((stop: RouteStop, idx: number) => {
        const stopPos = { lat: stop.station.latitude, lng: stop.station.longitude };
        markerPositionsRef.current.recommended.push(stopPos);
        bounds.extend(stopPos);
        hasPointsToFit = true;

        const isHighlighted = highlightedStopIndex === idx;

        const stopMarker = new window.google.maps.Marker({
          position: stopPos,
          map,
          title: `Recommended stop: ${stop.station.name}`,
          zIndex: 100,
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            scale: isHighlighted ? 12 : 10,
            fillColor: '#059669', // Emerald green
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: isHighlighted ? 3 : 2,
          },
        });

        stopMarker.addListener('click', () => {
          onSelectStation(stop.station);
          infoWindowRef.current?.setContent(`
            <div style="font-family: inherit; padding: 8px 10px; color: #0f172a; max-width: 250px;">
              <div style="font-size: 11px; font-weight: 700; color: #059669; text-transform: uppercase; margin-bottom: 2px;">
                🟢 Recommended stop
              </div>
              <div style="font-size: 13px; font-weight: 700; color: #0f172a;">${stop.station.name}</div>
              
              <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0; font-size: 11px; line-height: 1.6; color: #334155;">
                <div>Arrival battery: <strong>${stop.arrival_soc_pct.toFixed(0)}%</strong></div>
                <div>Charge target: <strong>${stop.departure_soc_pct.toFixed(0)}%</strong></div>
                <div>Estimated charging time: <strong>${stop.charge_duration_min.toFixed(0)} min</strong></div>
                <div>Estimated cost: <strong>₹${Math.round(stop.estimated_cost_usd)}</strong></div>
              </div>

              <div style="margin-top: 10px;">
                <a 
                  href="https://www.google.com/maps/dir/?api=1&destination=${stop.station.latitude},${stop.station.longitude}" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style="display: block; text-align: center; background: #059669; color: #ffffff; font-size: 12px; font-weight: 700; padding: 7px 10px; border-radius: 8px; text-decoration: none;"
                >
                  Navigate
                </a>
              </div>
            </div>
          `);
          infoWindowRef.current?.open(map, stopMarker);
        });

        markersRef.current.push({ type: 'recommended', marker: stopMarker });
      });
    }

    // E. Draw General Charging Points (🟡 Yellow Markers)
    if (showAllStations && allStations.length > 0 && visibleLayers.charging) {
      const stopIds = new Set(routeData?.stops?.map((s) => s.station.id) || []);

      // Filter to stations relevant to the current route corridor (max 25 stations)
      let candidateStations = allStations.filter((s) => !stopIds.has(s.id));

      if (routeData?.origin && routeData?.destination) {
        const originLat = routeData.origin.latitude;
        const originLng = routeData.origin.longitude;
        const destLat = routeData.destination.latitude;
        const destLng = routeData.destination.longitude;

        const minLat = Math.min(originLat, destLat) - 0.5;
        const maxLat = Math.max(originLat, destLat) + 0.5;
        const minLng = Math.min(originLng, destLng) - 0.5;
        const maxLng = Math.max(originLng, destLng) + 0.5;

        candidateStations = candidateStations.filter(
          (s) =>
            s.latitude >= minLat &&
            s.latitude <= maxLat &&
            s.longitude >= minLng &&
            s.longitude <= maxLng
        );
      }

      // Limit to max 25 stations to avoid cluttering the map
      candidateStations.slice(0, 25).forEach((station) => {
        const stationPos = { lat: station.latitude, lng: station.longitude };
        markerPositionsRef.current.charging.push(stationPos);

        const stationMarker = new window.google.maps.Marker({
          position: stationPos,
          map,
          title: `Charging point: ${station.name}`,
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            scale: 6,
            fillColor: '#d97706', // Amber / Yellow
            fillOpacity: 0.95,
            strokeColor: '#ffffff',
            strokeWeight: 1.5,
          },
        });

        stationMarker.addListener('click', () => {
          onSelectStation(station);
          infoWindowRef.current?.setContent(`
            <div style="font-family: inherit; padding: 8px 10px; color: #0f172a; max-width: 240px;">
              <div style="font-size: 10px; font-weight: 700; color: #d97706; text-transform: uppercase;">
                🟡 Charging point
              </div>
              <div style="font-size: 13px; font-weight: 700; margin-top: 2px;">${station.name}</div>
              <div style="font-size: 11px; color: #64748b; margin-top: 2px;">${station.operator}</div>
              
              <div style="margin-top: 6px; font-size: 11px; color: #334155; line-height: 1.5;">
                ${station.power_kw ? `<div>Power: <strong>${station.power_kw} kW</strong></div>` : ''}
                ${station.city ? `<div>Location: <strong>${station.city}</strong></div>` : ''}
              </div>

              <div style="margin-top: 10px;">
                <a 
                  href="https://www.google.com/maps/dir/?api=1&destination=${station.latitude},${station.longitude}" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style="display: block; text-align: center; background: #d97706; color: #ffffff; font-size: 11px; font-weight: 700; padding: 6px 8px; border-radius: 6px; text-decoration: none;"
                >
                  Open in Google Maps
                </a>
              </div>
            </div>
          `);
          infoWindowRef.current?.open(map, stationMarker);
        });

        markersRef.current.push({ type: 'charging', marker: stationMarker });
      });
    }

    // Auto fit bounds to visible points
    if (hasPointsToFit) {
      map.fitBounds(bounds, { top: 60, right: 60, bottom: 60, left: 60 });
    }
  }, [map, routeData, allStations, showAllStations, highlightedStopIndex, visibleLayers, onSelectStation]);

  // Interactive Legend click: focus or toggle group
  const handleLegendClick = (group: 'charging' | 'recommended' | 'start' | 'destination') => {
    if (!map) return;
    const points = markerPositionsRef.current[group] || [];
    if (points.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      points.forEach((point) => bounds.extend(point));
      map.fitBounds(bounds, { top: 80, right: 80, bottom: 80, left: 80 });
    }
  };

  const toggleLayer = (group: 'charging' | 'recommended' | 'start' | 'destination') => {
    setVisibleLayers((prev) => ({ ...prev, [group]: !prev[group] }));
  };

  return (
    <div className="relative w-full h-full">
      <Map
        defaultCenter={defaultCenter}
        defaultZoom={8}
        mapId="DEMO_MAP_ID"
        gestureHandling="greedy"
        disableDefaultUI={false}
        className="w-full h-full"
      />

      {apiKeyMissing && (
        <div className="absolute bottom-4 left-4 z-10 max-w-xs rounded-xl border border-amber-300 bg-amber-50/95 px-3 py-2 text-xs text-amber-900 shadow-md">
          Add a Google Maps key with Maps JavaScript and Places enabled to activate global place search.
        </div>
      )}

      {/* Interactive Map Legend */}
      <div className="absolute top-3 right-3 z-10 flex flex-wrap justify-end gap-1.5 max-w-[calc(100%-2rem)]">
        <button
          type="button"
          onClick={() => handleLegendClick('charging')}
          title="Click to focus corridor charging points"
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white/95 dark:bg-slate-900/95 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
        >
          <span className="w-2 h-2 rounded-full bg-amber-500 inline-block" />
          <span>Charging points</span>
        </button>

        <button
          type="button"
          onClick={() => handleLegendClick('recommended')}
          title="Click to focus recommended stops"
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white/95 dark:bg-slate-900/95 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
        >
          <span className="w-2 h-2 rounded-full bg-emerald-600 inline-block" />
          <span>Recommended stops</span>
        </button>

        <button
          type="button"
          onClick={() => handleLegendClick('start')}
          title="Click to focus start point"
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white/95 dark:bg-slate-900/95 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
        >
          <span className="w-2 h-2 rounded-full bg-blue-500 inline-block" />
          <span>Start</span>
        </button>

        <button
          type="button"
          onClick={() => handleLegendClick('destination')}
          title="Click to focus destination"
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white/95 dark:bg-slate-900/95 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
        >
          <span className="w-2 h-2 rounded-full bg-red-500 inline-block" />
          <span>Destination</span>
        </button>
      </div>
    </div>
  );
}
