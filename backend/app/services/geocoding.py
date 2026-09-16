import httpx
import logging
from typing import Optional, Tuple, Dict
from app.schemas.route import LocationInput, ResolvedLocation

logger = logging.getLogger(__name__)

# Predefined dictionary for instant, offline-friendly resolution with primary focus on India (Vellore & Tamil Nadu)
KNOWN_LOCATIONS: Dict[str, Tuple[float, float, str]] = {
    # India - Tamil Nadu & South India Primary Corridors
    "vellore": (12.9165, 79.1325, "Vellore, Tamil Nadu, India"),
    "vellore, tamil nadu": (12.9165, 79.1325, "Vellore, Tamil Nadu, India"),
    "vellore, tn": (12.9165, 79.1325, "Vellore, Tamil Nadu, India"),
    "chennai": (13.0827, 80.2707, "Chennai, Tamil Nadu, India"),
    "chennai, tamil nadu": (13.0827, 80.2707, "Chennai, Tamil Nadu, India"),
    "madras": (13.0827, 80.2707, "Chennai, Tamil Nadu, India"),
    "bengaluru": (12.9716, 77.5946, "Bengaluru, Karnataka, India"),
    "bangalore": (12.9716, 77.5946, "Bengaluru, Karnataka, India"),
    "bengaluru, karnataka": (12.9716, 77.5946, "Bengaluru, Karnataka, India"),
    "tirupati": (13.6288, 79.4192, "Tirupati, Andhra Pradesh, India"),
    "tirupati, andhra pradesh": (13.6288, 79.4192, "Tirupati, Andhra Pradesh, India"),
    "pondicherry": (11.9416, 79.8083, "Puducherry, India"),
    "puducherry": (11.9416, 79.8083, "Puducherry, India"),
    "kanchipuram": (12.8342, 79.7036, "Kanchipuram, Tamil Nadu, India"),
    "sriperumbudur": (12.9667, 79.9500, "Sriperumbudur, Tamil Nadu, India"),
    "ranipet": (12.9272, 79.3328, "Ranipet, Tamil Nadu, India"),
    "ambur": (12.7904, 78.7166, "Ambur, Tamil Nadu, India"),
    "vaniyambadi": (12.6825, 78.6186, "Vaniyambadi, Tamil Nadu, India"),
    "krishnagiri": (12.5186, 78.2137, "Krishnagiri, Tamil Nadu, India"),
    "hosur": (12.7409, 77.8253, "Hosur, Tamil Nadu, India"),
    "chittoor": (13.2172, 79.1003, "Chittoor, Andhra Pradesh, India"),
    "coimbatore": (11.0168, 76.9558, "Coimbatore, Tamil Nadu, India"),
    "salem": (11.6643, 78.1460, "Salem, Tamil Nadu, India"),
    "madurai": (9.9252, 78.1198, "Madurai, Tamil Nadu, India"),
    "trichy": (10.7905, 78.7047, "Tiruchirappalli, Tamil Nadu, India"),
    "tiruchirappalli": (10.7905, 78.7047, "Tiruchirappalli, Tamil Nadu, India"),
    "hyderabad": (17.3850, 78.4867, "Hyderabad, Telangana, India"),
    "mumbai": (19.0760, 72.8777, "Mumbai, Maharashtra, India"),
    "pune": (18.5204, 73.8567, "Pune, Maharashtra, India"),
    "delhi": (28.6139, 77.2090, "New Delhi, Delhi, India"),
    "new delhi": (28.6139, 77.2090, "New Delhi, Delhi, India"),
    "kochi": (9.9312, 76.2673, "Kochi, Kerala, India"),

    # International Popular Locations (Maintained for backward compatibility)
    "los angeles": (34.0522, -118.2437, "Los Angeles, California, US"),
    "los angeles, ca": (34.0522, -118.2437, "Los Angeles, California, US"),
    "san francisco": (37.7749, -122.4194, "San Francisco, California, US"),
    "san francisco, ca": (37.7749, -122.4194, "San Francisco, California, US"),
    "seattle": (47.6062, -122.3321, "Seattle, Washington, US"),
    "portland": (45.5152, -122.6784, "Portland, Oregon, US"),
    "new york": (40.7128, -74.0060, "New York, New York, US"),
    "new york, ny": (40.7128, -74.0060, "New York, New York, US"),
    "boston": (42.3601, -71.0589, "Boston, Massachusetts, US"),
    "las vegas": (36.1699, -115.1398, "Las Vegas, Nevada, US"),
    "austin": (30.2672, -97.7431, "Austin, Texas, US"),
    "houston": (29.7604, -95.3698, "Houston, Texas, US"),
    "london": (51.5074, -0.1278, "London, Greater London, United Kingdom"),
    "paris": (48.8566, 2.3522, "Paris, Île-de-France, France")
}

async def geocode_location(location: str | LocationInput | Dict) -> ResolvedLocation:
    """
    Resolve text or object into coordinates and formatted name.
    """
    if isinstance(location, dict):
        if "lat" in location and "lon" in location and location["lat"] is not None:
            return ResolvedLocation(
                name=location.get("name", f"Location ({location['lat']:.4f}, {location['lon']:.4f})"),
                latitude=float(location["lat"]),
                longitude=float(location["lon"]),
                formatted_address=location.get("name")
            )
        location_str = location.get("name", "")
    elif isinstance(location, LocationInput):
        if location.lat is not None and location.lon is not None:
            return ResolvedLocation(
                name=location.name or f"Location ({location.lat:.4f}, {location.lon:.4f})",
                latitude=location.lat,
                longitude=location.lon,
                formatted_address=location.name
            )
        location_str = location.name or ""
    else:
        location_str = str(location).strip()

    # Check normalized fast cache
    norm_key = location_str.lower().strip()
    if norm_key in KNOWN_LOCATIONS:
        lat, lon, formatted = KNOWN_LOCATIONS[norm_key]
        return ResolvedLocation(
            name=location_str.title(),
            latitude=lat,
            longitude=lon,
            formatted_address=formatted
        )

    # Check for partial match in known locations
    for k, v in KNOWN_LOCATIONS.items():
        if norm_key == k or (len(norm_key) > 3 and norm_key in k):
            lat, lon, formatted = v
            return ResolvedLocation(
                name=location_str.title(),
                latitude=lat,
                longitude=lon,
                formatted_address=formatted
            )

    # Fallback to OpenStreetMap Nominatim
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location_str,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "VoltRoute-EVPlanner/1.0"
        }
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if data and len(data) > 0:
                    first = data[0]
                    return ResolvedLocation(
                        name=location_str,
                        latitude=float(first["lat"]),
                        longitude=float(first["lon"]),
                        formatted_address=first.get("display_name", location_str)
                    )
    except Exception as e:
        logger.warning(f"OSM Nominatim geocoding failed for '{location_str}': {e}")

    # Default fallback to Vellore, Tamil Nadu, India
    logger.warning(f"Could not geocode '{location_str}'. Using Vellore, Tamil Nadu as default.")
    return ResolvedLocation(
        name=location_str or "Vellore, Tamil Nadu",
        latitude=12.9165,
        longitude=79.1325,
        formatted_address="Vellore, Tamil Nadu, India"
    )
