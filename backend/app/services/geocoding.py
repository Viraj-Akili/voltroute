import httpx
import logging
from typing import Optional, Tuple, Dict
from app.schemas.route import LocationInput, ResolvedLocation

logger = logging.getLogger(__name__)

# Predefined dictionary for instant, offline-friendly resolution of popular hubs & cities
KNOWN_LOCATIONS: Dict[str, Tuple[float, float, str]] = {
    # California
    "los angeles": (34.0522, -118.2437, "Los Angeles, California, US"),
    "los angeles, ca": (34.0522, -118.2437, "Los Angeles, California, US"),
    "la": (34.0522, -118.2437, "Los Angeles, California, US"),
    "san francisco": (37.7749, -122.4194, "San Francisco, California, US"),
    "san francisco, ca": (37.7749, -122.4194, "San Francisco, California, US"),
    "sf": (37.7749, -122.4194, "San Francisco, California, US"),
    "san diego": (32.7157, -117.1611, "San Diego, California, US"),
    "san diego, ca": (32.7157, -117.1611, "San Diego, California, US"),
    "san jose": (37.3382, -121.8863, "San Jose, California, US"),
    "san jose, ca": (37.3382, -121.8863, "San Jose, California, US"),
    "sacramento": (38.5816, -121.4944, "Sacramento, California, US"),
    "sacramento, ca": (38.5816, -121.4944, "Sacramento, California, US"),
    "fresno": (36.7468, -119.7726, "Fresno, California, US"),
    "bakersfield": (35.3733, -119.0187, "Bakersfield, California, US"),
    "kettleman city": (35.9868, -119.9575, "Kettleman City, California, US"),

    # Pacific Northwest
    "seattle": (47.6062, -122.3321, "Seattle, Washington, US"),
    "seattle, wa": (47.6062, -122.3321, "Seattle, Washington, US"),
    "portland": (45.5152, -122.6784, "Portland, Oregon, US"),
    "portland, or": (45.5152, -122.6784, "Portland, Oregon, US"),
    "vancouver": (49.2827, -123.1207, "Vancouver, BC, Canada"),

    # Southwest & Mountain
    "las vegas": (36.1699, -115.1398, "Las Vegas, Nevada, US"),
    "las vegas, nv": (36.1699, -115.1398, "Las Vegas, Nevada, US"),
    "reno": (39.5296, -119.8138, "Reno, Nevada, US"),
    "phoenix": (33.4484, -112.0740, "Phoenix, Arizona, US"),
    "phoenix, az": (33.4484, -112.0740, "Phoenix, Arizona, US"),
    "tucson": (32.2226, -110.9747, "Tucson, Arizona, US"),
    "salt lake city": (40.7608, -111.8910, "Salt Lake City, Utah, US"),
    "salt lake city, ut": (40.7608, -111.8910, "Salt Lake City, Utah, US"),
    "denver": (39.7392, -104.9903, "Denver, Colorado, US"),
    "denver, co": (39.7392, -104.9903, "Denver, Colorado, US"),

    # Texas & South
    "austin": (30.2672, -97.7431, "Austin, Texas, US"),
    "austin, tx": (30.2672, -97.7431, "Austin, Texas, US"),
    "dallas": (32.7767, -96.7970, "Dallas, Texas, US"),
    "dallas, tx": (32.7767, -96.7970, "Dallas, Texas, US"),
    "houston": (29.7604, -95.3698, "Houston, Texas, US"),
    "houston, tx": (29.7604, -95.3698, "Houston, Texas, US"),
    "san antonio": (29.4241, -98.4936, "San Antonio, Texas, US"),
    "san antonio, tx": (29.4241, -98.4936, "San Antonio, Texas, US"),

    # Midwest
    "chicago": (41.8781, -87.6298, "Chicago, Illinois, US"),
    "chicago, il": (41.8781, -87.6298, "Chicago, Illinois, US"),
    "detroit": (42.3314, -83.0458, "Detroit, Michigan, US"),
    "detroit, mi": (42.3314, -83.0458, "Detroit, Michigan, US"),
    "indianapolis": (39.7684, -86.1581, "Indianapolis, Indiana, US"),
    "kansas city": (39.0997, -94.5786, "Kansas City, Missouri, US"),
    "st. louis": (38.6270, -90.1994, "St. Louis, Missouri, US"),
    "columbus": (39.9612, -82.9988, "Columbus, Ohio, US"),

    # East Coast
    "new york": (40.7128, -74.0060, "New York, New York, US"),
    "new york, ny": (40.7128, -74.0060, "New York, New York, US"),
    "nyc": (40.7128, -74.0060, "New York, New York, US"),
    "boston": (42.3601, -71.0589, "Boston, Massachusetts, US"),
    "boston, ma": (42.3601, -71.0589, "Boston, Massachusetts, US"),
    "philadelphia": (39.9526, -75.1652, "Philadelphia, Pennsylvania, US"),
    "philadelphia, pa": (39.9526, -75.1652, "Philadelphia, Pennsylvania, US"),
    "washington": (38.9072, -77.0369, "Washington, District of Columbia, US"),
    "washington, dc": (38.9072, -77.0369, "Washington, District of Columbia, US"),
    "dc": (38.9072, -77.0369, "Washington, District of Columbia, US"),
    "baltimore": (39.2904, -76.6122, "Baltimore, Maryland, US"),
    "richmond": (37.5407, -77.4360, "Richmond, Virginia, US"),
    "atlanta": (33.7490, -84.3880, "Atlanta, Georgia, US"),
    "atlanta, ga": (33.7490, -84.3880, "Atlanta, Georgia, US"),
    "orlando": (28.5383, -81.3792, "Orlando, Florida, US"),
    "orlando, fl": (28.5383, -81.3792, "Orlando, Florida, US"),
    "miami": (25.7617, -80.1918, "Miami, Florida, US"),
    "miami, fl": (25.7617, -80.1918, "Miami, Florida, US"),

    # Europe / UK
    "london": (51.5074, -0.1278, "London, Greater London, United Kingdom"),
    "paris": (48.8566, 2.3522, "Paris, Île-de-France, France"),
    "amsterdam": (52.3676, 4.9041, "Amsterdam, North Holland, Netherlands"),
    "brussels": (50.8503, 4.3517, "Brussels, Belgium")
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

    # Default fallback to San Francisco if unresolved
    logger.warning(f"Could not geocode '{location_str}'. Using San Francisco as default.")
    return ResolvedLocation(
        name=location_str or "San Francisco, CA",
        latitude=37.7749,
        longitude=-122.4194,
        formatted_address="San Francisco, California, US (Default fallback)"
    )
