import math
import httpx
import logging
from typing import List, Tuple, Dict, Any, Optional

logger = logging.getLogger(__name__)

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on the earth (in km).
    """
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def interpolate_points(lat1: float, lon1: float, lat2: float, lon2: float, num_points: int = 25) -> List[List[float]]:
    """
    Generate interpolated intermediate coordinates between two points.
    """
    coords = []
    for i in range(num_points + 1):
        fraction = i / float(num_points)
        lat = lat1 + fraction * (lat2 - lat1)
        lon = lon1 + fraction * (lon2 - lon1)
        coords.append([lat, lon])
    return coords

def project_point_to_segment(
    px: float, py: float,
    ax: float, ay: float,
    bx: float, by: float
) -> Tuple[float, float, float]:
    """
    Project point P onto segment AB. Returns (projected_lat, projected_lon, t) where t in [0, 1].
    Coordinates in degrees approximation for local segment.
    """
    dx = bx - ax
    dy = by - ay
    if dx == 0 and dy == 0:
        return ax, ay, 0.0

    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj_x = ax + t * dx
    proj_y = ay + t * dy
    return proj_x, proj_y, t

def find_station_projection_on_polyline(
    station_lat: float, station_lon: float,
    polyline: List[List[float]],
    cum_distances: List[float]
) -> Tuple[float, float]:
    """
    Find detour distance (km) and distance from route start (km) for a charging station.
    Returns (detour_km, distance_from_start_km).
    """
    min_detour = float('inf')
    best_dist_along = 0.0

    for i in range(len(polyline) - 1):
        p1 = polyline[i]
        p2 = polyline[i + 1]
        
        # Segment start & end
        lat1, lon1 = p1[0], p1[1]
        lat2, lon2 = p2[0], p2[1]

        proj_lat, proj_lon, t = project_point_to_segment(
            station_lat, station_lon,
            lat1, lon1, lat2, lon2
        )

        detour = haversine_distance_km(station_lat, station_lon, proj_lat, proj_lon)
        if detour < min_detour:
            min_detour = detour
            segment_len = haversine_distance_km(lat1, lon1, lat2, lon2)
            best_dist_along = cum_distances[i] + t * segment_len

    return min_detour, best_dist_along

async def get_route_geometry_and_distance(
    start_lat: float, start_lon: float,
    end_lat: float, end_lon: float,
    osrm_base_url: str = "https://router.project-osrm.org"
) -> Dict[str, Any]:
    """
    Query OSRM driving route, with robust fallback to Great-Circle interpolated route.
    Returns:
      - distance_km (float)
      - duration_min (float)
      - polyline (List[[lat, lon]])
      - cumulative_distances (List[float])
    """
    try:
        url = f"{osrm_base_url}/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "false"
        }
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("routes") and len(data["routes"]) > 0:
                    route = data["routes"][0]
                    dist_meters = route.get("distance", 0.0)
                    dur_seconds = route.get("duration", 0.0)
                    geojson_coords = route.get("geometry", {}).get("coordinates", [])

                    # GeoJSON is [lon, lat] -> convert to [lat, lon]
                    polyline = [[coord[1], coord[0]] for coord in geojson_coords]
                    if not polyline:
                        polyline = [[start_lat, start_lon], [end_lat, end_lon]]

                    # Compute cumulative distances along polyline
                    cum_dist = [0.0]
                    for i in range(1, len(polyline)):
                        seg_d = haversine_distance_km(
                            polyline[i-1][0], polyline[i-1][1],
                            polyline[i][0], polyline[i][1]
                        )
                        cum_dist.append(cum_dist[-1] + seg_d)

                    return {
                        "distance_km": round(dist_meters / 1000.0, 1),
                        "duration_min": round(dur_seconds / 60.0, 1),
                        "polyline": polyline,
                        "cumulative_distances": cum_dist,
                        "is_osrm": True
                    }
    except Exception as e:
        logger.warning(f"OSRM routing request failed: {e}. Falling back to geometric route.")

    # Geometric fallback with highway curvature factor 1.25x
    direct_dist = haversine_distance_km(start_lat, start_lon, end_lat, end_lon)
    est_road_dist = direct_dist * 1.22
    # Estimate highway driving speed ~100 km/h (62 mph)
    est_duration_min = (est_road_dist / 100.0) * 60.0

    polyline = interpolate_points(start_lat, start_lon, end_lat, end_lon, num_points=35)
    cum_dist = [0.0]
    for i in range(1, len(polyline)):
        seg_d = haversine_distance_km(
            polyline[i-1][0], polyline[i-1][1],
            polyline[i][0], polyline[i][1]
        ) * 1.22
        cum_dist.append(cum_dist[-1] + seg_d)

    return {
        "distance_km": round(est_road_dist, 1),
        "duration_min": round(est_duration_min, 1),
        "polyline": polyline,
        "cumulative_distances": cum_dist,
        "is_osrm": False
    }
