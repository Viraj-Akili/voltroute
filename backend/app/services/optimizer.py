import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.station import ChargingStation
from app.schemas.route import (
    RouteRequest, RouteResponse, TripSummary, ChargingStop,
    RouteLeg, BatteryProfilePoint, StationResponse, ResolvedLocation
)
from app.services.routing import (
    get_route_geometry_and_distance,
    find_station_projection_on_polyline,
    haversine_distance_km
)

logger = logging.getLogger(__name__)

def calculate_charge_duration_minutes(
    start_soc: float,
    target_soc: float,
    battery_capacity_kwh: float,
    station_power_kw: float,
    max_vehicle_power_kw: float = 250.0
) -> float:
    """
    Simulate realistic non-linear EV charging curve.
    Batteries charge fastest at low SOC (<50%), taper slightly between 50-80%,
    and taper heavily above 80% to protect cell chemistry.
    """
    if target_soc <= start_soc:
        return 0.0

    peak_kw = min(station_power_kw, max_vehicle_power_kw)
    total_time_hours = 0.0

    # Step through 5% increments
    current = start_soc
    while current < target_soc:
        next_step = min(target_soc, current + 5.0)
        step_kwh = ((next_step - current) / 100.0) * battery_capacity_kwh
        midpoint_soc = (current + next_step) / 2.0

        if midpoint_soc < 50.0:
            effective_kw = peak_kw * 0.95
        elif midpoint_soc < 80.0:
            effective_kw = peak_kw * 0.72
        else:
            effective_kw = peak_kw * 0.35

        effective_kw = max(15.0, effective_kw) # minimum floor
        total_time_hours += step_kwh / effective_kw
        current = next_step

    # Add 2 minutes connection/handshake overhead
    return max(5.0, round(total_time_hours * 60.0 + 2.0, 1))

async def optimize_ev_route(
    request: RouteRequest,
    origin: ResolvedLocation,
    destination: ResolvedLocation,
    db: Session,
    osrm_base_url: str = "https://router.project-osrm.org"
) -> RouteResponse:
    """
    Core EV routing and charging stop optimization algorithm.
    """
    # 1. Fetch road route geometry & distances
    route_data = await get_route_geometry_and_distance(
        origin.latitude, origin.longitude,
        destination.latitude, destination.longitude,
        osrm_base_url=osrm_base_url
    )

    total_distance_km = route_data["distance_km"]
    total_drive_time_min = route_data["duration_min"]
    polyline = route_data["polyline"]
    cum_distances = route_data["cumulative_distances"]

    # 2. EV Physics Parameters
    battery_capacity = request.battery_capacity_kwh
    consumption_rate_kwh_km = (request.vehicle_efficiency_wh_per_km / 1000.0) * 1.04 # 4% weather/elevation overhead
    max_range_km = battery_capacity / consumption_rate_kwh_km
    initial_soc = request.current_battery_pct
    min_stop_soc = request.min_stop_soc_pct
    target_dest_soc = request.target_dest_soc_pct
    max_charge_soc = request.max_charge_soc_pct

    # 3. Pull all candidate stations and project onto route corridor
    all_db_stations = db.query(ChargingStation).filter(ChargingStation.is_operational == True).all()
    
    corridor_candidates: List[Dict[str, Any]] = []
    for s in all_db_stations:
        # Filter connector compatibility if requested
        if request.preferred_connectors:
            station_connectors = [c.strip() for c in s.connector_types.split(",")]
            if not any(req_c in station_connectors for req_c in request.preferred_connectors):
                continue

        # Filter minimum power if requested
        if request.min_charger_power_kw and s.power_kw < request.min_charger_power_kw:
            continue

        detour_km, dist_along_km = find_station_projection_on_polyline(
            s.latitude, s.longitude, polyline, cum_distances
        )

        # Include if within 30km detour buffer of the route
        if detour_km <= 30.0 and 0.0 <= dist_along_km <= total_distance_km:
            s_dict = s.to_dict()
            s_dict["detour_km"] = round(detour_km, 1)
            s_dict["dist_along_km"] = round(dist_along_km, 1)
            corridor_candidates.append(s_dict)

    # Sort candidates by distance along route
    corridor_candidates.sort(key=lambda x: x["dist_along_km"])

    # 4. Determine if direct trip is possible without charging
    energy_needed_direct = total_distance_km * consumption_rate_kwh_km
    soc_drop_direct = (energy_needed_direct / battery_capacity) * 100.0
    arrival_soc_direct = initial_soc - soc_drop_direct

    stops: List[ChargingStop] = []
    legs: List[RouteLeg] = []
    battery_profile: List[BatteryProfilePoint] = []

    # Start point in profile
    battery_profile.append(BatteryProfilePoint(
        distance_km=0.0,
        soc_pct=round(initial_soc, 1),
        location_name=origin.name,
        event="start"
    ))

    current_dist = 0.0
    current_soc = initial_soc
    current_loc_name = origin.name
    total_charge_time_min = 0.0
    total_energy_charged_kwh = 0.0
    total_cost_usd = 0.0
    is_feasible = True
    status_message = "Optimal EV route computed successfully."

    # Direct non-stop trip
    if arrival_soc_direct >= target_dest_soc:
        # Simple single leg
        legs.append(RouteLeg(
            leg_index=1,
            from_name=origin.name,
            to_name=destination.name,
            distance_km=round(total_distance_km, 1),
            duration_min=round(total_drive_time_min, 1),
            energy_used_kwh=round(energy_needed_direct, 1),
            start_soc_pct=round(initial_soc, 1),
            end_soc_pct=round(arrival_soc_direct, 1),
            polyline=polyline
        ))

        # Sample intermediate points for battery profile
        num_samples = 15
        for i in range(1, num_samples):
            frac = i / float(num_samples)
            d = frac * total_distance_km
            soc = initial_soc - (d * consumption_rate_kwh_km / battery_capacity) * 100.0
            battery_profile.append(BatteryProfilePoint(
                distance_km=round(d, 1),
                soc_pct=round(max(0.0, soc), 1),
                location_name=f"En route ({round(d)} km)",
                event="driving"
            ))

        battery_profile.append(BatteryProfilePoint(
            distance_km=round(total_distance_km, 1),
            soc_pct=round(arrival_soc_direct, 1),
            location_name=destination.name,
            event="destination"
        ))

    else:
        # Trip requires 1 or more charging stops
        stop_index = 1
        prev_stop_dist = 0.0
        visited_station_ids = set()

        max_iterations = 10
        iteration = 0

        while current_dist < total_distance_km and iteration < max_iterations:
            iteration += 1
            dist_to_dest = total_distance_km - current_dist
            energy_to_dest = dist_to_dest * consumption_rate_kwh_km
            dest_arrival_soc = current_soc - (energy_to_dest / battery_capacity) * 100.0

            # If we can reach destination with safety buffer, finish trip!
            if dest_arrival_soc >= target_dest_soc:
                leg_duration = (dist_to_dest / max(1.0, total_distance_km)) * total_drive_time_min
                legs.append(RouteLeg(
                    leg_index=stop_index,
                    from_name=current_loc_name,
                    to_name=destination.name,
                    distance_km=round(dist_to_dest, 1),
                    duration_min=round(leg_duration, 1),
                    energy_used_kwh=round(energy_to_dest, 1),
                    start_soc_pct=round(current_soc, 1),
                    end_soc_pct=round(dest_arrival_soc, 1)
                ))

                # Intermediate points
                num_samples = 6
                for i in range(1, num_samples):
                    frac = i / float(num_samples)
                    d = current_dist + frac * dist_to_dest
                    soc = current_soc - ((d - current_dist) * consumption_rate_kwh_km / battery_capacity) * 100.0
                    battery_profile.append(BatteryProfilePoint(
                        distance_km=round(d, 1),
                        soc_pct=round(max(0.0, soc), 1),
                        location_name=f"En route ({round(d)} km)",
                        event="driving"
                    ))

                battery_profile.append(BatteryProfilePoint(
                    distance_km=round(total_distance_km, 1),
                    soc_pct=round(dest_arrival_soc, 1),
                    location_name=destination.name,
                    event="destination"
                ))
                current_soc = dest_arrival_soc
                current_dist = total_distance_km
                break

            # Need to select the next optimal charging stop
            # Safe driving limit before SOC drops below min_stop_soc
            max_safe_leg_dist = max(10.0, ((current_soc - min_stop_soc) / 100.0) * max_range_km)
            reachable_ceiling_dist = current_dist + max_safe_leg_dist

            # Find candidates situated in valid range
            candidates = [
                s for s in corridor_candidates
                if s["dist_along_km"] > current_dist + 20.0
                and s["dist_along_km"] <= reachable_ceiling_dist + 15.0 # allow slight margin
                and s["id"] not in visited_station_ids
            ]

            if not candidates:
                # Emergency fallback: find the closest station ahead regardless of margin
                candidates = [
                    s for s in corridor_candidates
                    if s["dist_along_km"] > current_dist + 10.0
                    and s["id"] not in visited_station_ids
                ]

            if not candidates:
                # No station found along corridor
                is_feasible = False
                status_message = f"Infeasible route: No compatible charging station found after {round(current_dist)} km."
                break

            # Score candidates
            best_candidate = None
            best_score = -float('inf')

            for cand in candidates:
                leg_dist = cand["dist_along_km"] - current_dist
                leg_energy = leg_dist * consumption_rate_kwh_km
                soc_at_cand = current_soc - (leg_energy / battery_capacity) * 100.0

                # Penalize severely if battery would drain below 3%
                if soc_at_cand < 3.0:
                    continue

                # Power score (higher kW is better)
                power_score = (cand["power_kw"] / 350.0) * 45.0
                
                # Depletion score (optimal arrival is 10-18% SOC for fast charging)
                ideal_arrival = min_stop_soc + 4.0
                depletion_score = max(0.0, 30.0 - abs(soc_at_cand - ideal_arrival) * 1.5)
                
                # Detour penalty
                detour_pen = cand.get("detour_km", 0.0) * 2.0

                # Distance progress score (prefer stopping further along route)
                progress_score = (leg_dist / max_safe_leg_dist) * 25.0

                score = power_score + depletion_score + progress_score - detour_pen
                if score > best_score:
                    best_score = score
                    best_candidate = cand

            if not best_candidate:
                best_candidate = candidates[0]

            visited_station_ids.add(best_candidate["id"])

            # Compute leg to this chosen station
            leg_dist = best_candidate["dist_along_km"] - current_dist
            leg_energy = leg_dist * consumption_rate_kwh_km
            arrival_soc = max(2.0, current_soc - (leg_energy / battery_capacity) * 100.0)
            leg_dur = (leg_dist / max(1.0, total_distance_km)) * total_drive_time_min

            legs.append(RouteLeg(
                leg_index=stop_index,
                from_name=current_loc_name,
                to_name=best_candidate["name"],
                distance_km=round(leg_dist, 1),
                duration_min=round(leg_dur, 1),
                energy_used_kwh=round(leg_energy, 1),
                start_soc_pct=round(current_soc, 1),
                end_soc_pct=round(arrival_soc, 1)
            ))

            # Intermediate profile points for this leg
            for i in range(1, 4):
                frac = i / 4.0
                d = current_dist + frac * leg_dist
                soc = current_soc - ((d - current_dist) * consumption_rate_kwh_km / battery_capacity) * 100.0
                battery_profile.append(BatteryProfilePoint(
                    distance_km=round(d, 1),
                    soc_pct=round(max(0.0, soc), 1),
                    location_name=f"En route ({round(d)} km)",
                    event="driving"
                ))

            # Arrival at charger
            battery_profile.append(BatteryProfilePoint(
                distance_km=round(best_candidate["dist_along_km"], 1),
                soc_pct=round(arrival_soc, 1),
                location_name=best_candidate["name"],
                event="arrival_at_charger"
            ))

            # Calculate charging needs at this stop
            # Check remaining distance to destination
            dist_remaining_to_dest = total_distance_km - best_candidate["dist_along_km"]
            energy_to_finish = dist_remaining_to_dest * consumption_rate_kwh_km
            soc_to_finish = (energy_to_finish / battery_capacity) * 100.0 + target_dest_soc

            if soc_to_finish <= max_charge_soc:
                departure_soc = min(95.0, round(soc_to_finish + 4.0, 1))
            else:
                departure_soc = max_charge_soc

            departure_soc = max(departure_soc, arrival_soc + 20.0)
            departure_soc = min(95.0, departure_soc)

            energy_added = ((departure_soc - arrival_soc) / 100.0) * battery_capacity
            charge_duration = calculate_charge_duration_minutes(
                start_soc=arrival_soc,
                target_soc=departure_soc,
                battery_capacity_kwh=battery_capacity,
                station_power_kw=best_candidate["power_kw"]
            )
            cost = energy_added * best_candidate.get("price_per_kwh", 0.36)

            total_charge_time_min += charge_duration
            total_energy_charged_kwh += energy_added
            total_cost_usd += cost

            # Station Response object
            station_resp = StationResponse(
                id=best_candidate["id"],
                name=best_candidate["name"],
                latitude=best_candidate["latitude"],
                longitude=best_candidate["longitude"],
                address=best_candidate.get("address"),
                city=best_candidate.get("city"),
                state=best_candidate.get("state"),
                country=best_candidate.get("country", "US"),
                operator=best_candidate["operator"],
                power_kw=best_candidate["power_kw"],
                total_ports=best_candidate.get("total_ports", 8),
                available_ports=best_candidate.get("available_ports", 6),
                connector_types=best_candidate.get("connector_types", ["CCS", "NACS"]),
                price_per_kwh=best_candidate.get("price_per_kwh", 0.36),
                amenities=best_candidate.get("amenities", ["Restrooms", "Dining"]),
                is_operational=best_candidate.get("is_operational", True),
                detour_km=best_candidate.get("detour_km", 0.0)
            )

            stops.append(ChargingStop(
                stop_index=stop_index,
                station=station_resp,
                arrival_soc_pct=round(arrival_soc, 1),
                departure_soc_pct=round(departure_soc, 1),
                energy_added_kwh=round(energy_added, 1),
                charge_duration_min=round(charge_duration, 1),
                estimated_cost_usd=round(cost, 2),
                distance_from_start_km=round(best_candidate["dist_along_km"], 1),
                distance_from_prev_stop_km=round(best_candidate["dist_along_km"] - prev_stop_dist, 1)
            ))

            # Charged point in battery profile
            battery_profile.append(BatteryProfilePoint(
                distance_km=round(best_candidate["dist_along_km"], 1),
                soc_pct=round(departure_soc, 1),
                location_name=best_candidate["name"],
                event="charged_at_charger"
            ))

            # Advance state
            prev_stop_dist = best_candidate["dist_along_km"]
            current_dist = best_candidate["dist_along_km"]
            current_soc = departure_soc
            current_loc_name = best_candidate["name"]
            stop_index += 1

    # 5. Compile Trip Summary
    total_energy_consumed = total_distance_km * consumption_rate_kwh_km
    total_trip_time_min = total_drive_time_min + total_charge_time_min
    co2_saved_kg = total_distance_km * 0.192 # avg 192g CO2/km for internal combustion engine car

    summary = TripSummary(
        total_distance_km=round(total_distance_km, 1),
        total_distance_miles=round(total_distance_km * 0.621371, 1),
        total_drive_time_min=round(total_drive_time_min, 1),
        total_charge_time_min=round(total_charge_time_min, 1),
        total_trip_time_min=round(total_trip_time_min, 1),
        initial_battery_pct=round(initial_soc, 1),
        final_battery_pct=round(current_soc, 1),
        total_energy_consumed_kwh=round(total_energy_consumed, 1),
        total_energy_charged_kwh=round(total_energy_charged_kwh, 1),
        total_charging_cost_usd=round(total_cost_usd, 2),
        co2_saved_kg=round(co2_saved_kg, 1),
        num_stops=len(stops),
        is_feasible=is_feasible,
        status_message=status_message
    )

    # Convert all corridor candidate stations into schema
    candidate_station_schemas: List[StationResponse] = []
    for c in corridor_candidates:
        candidate_station_schemas.append(StationResponse(
            id=c["id"],
            name=c["name"],
            latitude=c["latitude"],
            longitude=c["longitude"],
            address=c.get("address"),
            city=c.get("city"),
            state=c.get("state"),
            country=c.get("country", "US"),
            operator=c["operator"],
            power_kw=c["power_kw"],
            total_ports=c.get("total_ports", 8),
            available_ports=c.get("available_ports", 6),
            connector_types=c.get("connector_types", ["CCS", "NACS"]),
            price_per_kwh=c.get("price_per_kwh", 0.36),
            amenities=c.get("amenities", ["Restrooms", "Dining"]),
            is_operational=c.get("is_operational", True),
            detour_km=c.get("detour_km", 0.0)
        ))

    return RouteResponse(
        summary=summary,
        origin=origin,
        destination=destination,
        legs=legs,
        stops=stops,
        battery_profile=battery_profile,
        route_geometry=polyline,
        candidate_stations=candidate_station_schemas
    )
