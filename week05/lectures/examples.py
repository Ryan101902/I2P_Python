"""
Week 5: The Nominatim API (Geocoding)
Lecture Examples - Runnable Code

This file contains all the code examples from the Week 5 lecture.
Run this file to see the examples in action!

Usage:
    python examples.py

Note: Examples make real API calls and require internet connection.
"""

import requests
import time
import json
import hashlib
from pathlib import Path
from typing import TypedDict, Optional


# =============================================================================
# Configuration
# =============================================================================

USER_AGENT = "CS101-Examples/1.0 (cs101@university.edu)"
BASE_URL = "https://nominatim.openstreetmap.org"


# =============================================================================
# Example 1: Basic Nominatim Search
# =============================================================================

def example_basic_search():
    """Make a basic search request to Nominatim."""
    print("\n" + "="*60)
    print("Example 1: Basic Nominatim Search")
    print("="*60)

    url = f"{BASE_URL}/search"

    params = {
        "q": "Taipei 101",
        "format": "json",
        "limit": 1
    }

    headers = {"User-Agent": USER_AGENT}

    print(f"Searching for: {params['q']}")

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        results = response.json()
        if results:
            place = results[0]
            print(f"\nResult:")
            print(f"  Name: {place.get('name', 'N/A')}")
            print(f"  Display Name: {place['display_name'][:60]}...")
            print(f"  Latitude: {place['lat']} (type: {type(place['lat']).__name__})")
            print(f"  Longitude: {place['lon']} (type: {type(place['lon']).__name__})")
            print(f"  Type: {place.get('class')}:{place.get('type')}")
            print(f"  Importance: {place.get('importance', 'N/A')}")
        else:
            print("No results found")
    else:
        print(f"Error: HTTP {response.status_code}")


# =============================================================================
# Example 2: Address Details
# =============================================================================

def example_address_details():
    """Get detailed address breakdown."""
    print("\n" + "="*60)
    print("Example 2: Address Details")
    print("="*60)

    url = f"{BASE_URL}/search"

    params = {
        "q": "National Taiwan University",
        "format": "json",
        "limit": 1,
        "addressdetails": 1  # Include address breakdown
    }

    headers = {"User-Agent": USER_AGENT}

    print(f"Searching for: {params['q']} (with address details)")

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        results = response.json()
        if results:
            place = results[0]
            address = place.get("address", {})

            print(f"\nAddress breakdown:")
            for key, value in address.items():
                print(f"  {key}: {value}")
        else:
            print("No results found")


# =============================================================================
# Example 3: Safe Dictionary Access
# =============================================================================

def example_safe_get():
    """Demonstrate safe dictionary access patterns."""
    print("\n" + "="*60)
    print("Example 3: Safe Dictionary Access")
    print("="*60)

    # Simulated API responses with varying completeness
    responses = [
        # Complete response
        {
            "name": "Taipei 101",
            "address": {
                "city": "Taipei",
                "district": "Xinyi",
                "country": "Taiwan"
            }
        },
        # Missing address
        {
            "name": "Some Place"
        },
        # Missing city
        {
            "name": "Rural Area",
            "address": {
                "village": "Small Village",
                "country": "Taiwan"
            }
        }
    ]

    def safe_get(data: dict, *keys, default=None):
        """Safely get nested value."""
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return default
            if current is None:
                return default
        return current

    print("\nExtracting city from various responses:\n")

    for i, resp in enumerate(responses, 1):
        # Unsafe way (would crash on missing data)
        # city = resp["address"]["city"]

        # Safe way
        city = safe_get(resp, "address", "city", default="Unknown")

        print(f"Response {i}: {resp.get('name', 'N/A')}")
        print(f"  City: {city}")
        print()


# =============================================================================
# Example 4: Parsing Nominatim Results
# =============================================================================

class GeocodedPlace(TypedDict):
    """Type definition for a geocoded place."""
    name: str
    lat: float
    lon: float
    display_name: str
    place_type: str
    importance: float


def parse_nominatim_result(result: dict) -> GeocodedPlace:
    """Parse a single Nominatim result into a clean structure."""
    try:
        lat = float(result.get("lat", 0))
        lon = float(result.get("lon", 0))
    except (ValueError, TypeError):
        lat, lon = 0.0, 0.0

    try:
        importance = float(result.get("importance", 0))
    except (ValueError, TypeError):
        importance = 0.0

    return {
        "name": result.get("name", result.get("display_name", "Unknown")),
        "lat": lat,
        "lon": lon,
        "display_name": result.get("display_name", ""),
        "place_type": f"{result.get('class', '')}:{result.get('type', '')}",
        "importance": importance
    }


def example_parse_results():
    """Demonstrate parsing Nominatim results."""
    print("\n" + "="*60)
    print("Example 4: Parsing Nominatim Results")
    print("="*60)

    # Make API call
    url = f"{BASE_URL}/search"
    params = {"q": "Shibuya Station Tokyo", "format": "json", "limit": 3}
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        raw_results = response.json()

        print(f"\nFound {len(raw_results)} results:")

        for i, raw in enumerate(raw_results, 1):
            parsed = parse_nominatim_result(raw)
            print(f"\n{i}. {parsed['name']}")
            print(f"   Coordinates: ({parsed['lat']:.6f}, {parsed['lon']:.6f})")
            print(f"   Type: {parsed['place_type']}")
            print(f"   Importance: {parsed['importance']:.4f}")


# =============================================================================
# Example 5: Bounding Box Parsing
# =============================================================================

def example_bounding_box():
    """Demonstrate bounding box parsing and calculations."""
    print("\n" + "="*60)
    print("Example 5: Bounding Box Parsing")
    print("="*60)

    def parse_bounding_box(bbox: list) -> dict | None:
        """Parse a Nominatim bounding box."""
        if not bbox or len(bbox) != 4:
            return None
        try:
            return {
                "south": float(bbox[0]),
                "north": float(bbox[1]),
                "west": float(bbox[2]),
                "east": float(bbox[3])
            }
        except (ValueError, TypeError):
            return None

    def bbox_center(bbox: dict) -> tuple[float, float]:
        """Calculate center of bounding box."""
        lat = (bbox["south"] + bbox["north"]) / 2
        lon = (bbox["west"] + bbox["east"]) / 2
        return (lat, lon)

    # Make API call
    url = f"{BASE_URL}/search"
    params = {"q": "Central Park New York", "format": "json", "limit": 1}
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        results = response.json()
        if results:
            place = results[0]
            raw_bbox = place.get("boundingbox")

            print(f"\nPlace: {place.get('name', 'N/A')}")
            print(f"Raw bounding box: {raw_bbox}")

            bbox = parse_bounding_box(raw_bbox)
            if bbox:
                print(f"\nParsed bounding box:")
                print(f"  South: {bbox['south']:.6f}")
                print(f"  North: {bbox['north']:.6f}")
                print(f"  West: {bbox['west']:.6f}")
                print(f"  East: {bbox['east']:.6f}")

                center = bbox_center(bbox)
                print(f"\nCenter point: ({center[0]:.6f}, {center[1]:.6f})")


# =============================================================================
# Example 6: Error Handling
# =============================================================================

def example_error_handling():
    """Demonstrate comprehensive error handling."""
    print("\n" + "="*60)
    print("Example 6: Error Handling")
    print("="*60)

    class GeocodingError(Exception):
        """Base exception."""
        pass

    class NetworkError(GeocodingError):
        """Network errors."""
        pass

    class NotFoundError(GeocodingError):
        """Place not found."""
        pass

    def safe_geocode(query: str) -> dict:
        """Geocode with comprehensive error handling."""
        url = f"{BASE_URL}/search"
        headers = {"User-Agent": USER_AGENT}
        params = {"q": query, "format": "json", "limit": 1}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 429:
                raise NetworkError("Rate limit exceeded")

            if response.status_code != 200:
                raise NetworkError(f"HTTP {response.status_code}")

            data = response.json()

            if not data:
                raise NotFoundError(f"No results for: {query}")

            result = data[0]
            return {
                "name": result.get("name", query),
                "lat": float(result["lat"]),
                "lon": float(result["lon"])
            }

        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Connection failed")
        except (KeyError, ValueError) as e:
            raise GeocodingError(f"Parse error: {e}")

    # Test cases
    test_queries = [
        "Taipei 101",           # Should succeed
        "xyzzy12345notaplace",  # Should raise NotFoundError
    ]

    for query in test_queries:
        print(f"\nGeocoding: '{query}'")
        try:
            result = safe_geocode(query)
            print(f"  Success: ({result['lat']:.4f}, {result['lon']:.4f})")
        except NotFoundError as e:
            print(f"  Not Found: {e}")
        except NetworkError as e:
            print(f"  Network Error: {e}")
        except GeocodingError as e:
            print(f"  Error: {e}")

        time.sleep(1)  # Rate limiting


# =============================================================================
# Example 7: Reverse Geocoding
# =============================================================================

def example_reverse_geocoding():
    """Demonstrate reverse geocoding."""
    print("\n" + "="*60)
    print("Example 7: Reverse Geocoding")
    print("="*60)

    def reverse_geocode(lat: float, lon: float) -> dict | None:
        """Convert coordinates to address."""
        url = f"{BASE_URL}/reverse"
        params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}
        headers = {"User-Agent": USER_AGENT}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    # Famous landmarks by coordinates
    locations = [
        (25.0339, 121.5645, "Taipei 101"),
        (48.8584, 2.2945, "Eiffel Tower"),
        (40.6892, -74.0445, "Statue of Liberty"),
    ]

    for lat, lon, expected in locations:
        print(f"\nCoordinates: ({lat}, {lon})")
        print(f"Expected: {expected}")

        result = reverse_geocode(lat, lon)

        if result:
            print(f"Found: {result.get('display_name', 'N/A')[:60]}...")
        else:
            print("Not found")

        time.sleep(1)  # Rate limiting


# =============================================================================
# Example 8: Complete Geocoder Class
# =============================================================================

class Geocoder:
    """Complete geocoding client."""

    def __init__(self, user_agent: str):
        self.headers = {"User-Agent": user_agent}
        self.last_request = 0

    def _rate_limit(self):
        """Ensure 1 second between requests."""
        elapsed = time.time() - self.last_request
        if elapsed < 1:
            time.sleep(1 - elapsed)
        self.last_request = time.time()

    def forward(self, query: str) -> dict | None:
        """Forward geocode."""
        self._rate_limit()

        url = f"{BASE_URL}/search"
        params = {"q": query, "format": "json", "limit": 1, "addressdetails": 1}

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    r = data[0]
                    return {
                        "name": r.get("name", query),
                        "lat": float(r["lat"]),
                        "lon": float(r["lon"]),
                        "display_name": r.get("display_name", ""),
                        "address": r.get("address", {})
                    }
        except (requests.RequestException, ValueError, KeyError):
            pass
        return None

    def reverse(self, lat: float, lon: float) -> dict | None:
        """Reverse geocode."""
        self._rate_limit()

        url = f"{BASE_URL}/reverse"
        params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "display_name" in data:
                    return {
                        "display_name": data["display_name"],
                        "address": data.get("address", {})
                    }
        except requests.RequestException:
            pass
        return None

    def batch(self, queries: list[str]) -> list[dict]:
        """Geocode multiple places."""
        results = []
        for query in queries:
            result = self.forward(query)
            if result:
                results.append(result)
        return results


def example_geocoder_class():
    """Demonstrate the Geocoder class."""
    print("\n" + "="*60)
    print("Example 8: Complete Geocoder Class")
    print("="*60)

    geocoder = Geocoder(USER_AGENT)

    # Forward geocoding
    print("\nForward geocoding 'Tokyo Tower':")
    result = geocoder.forward("Tokyo Tower")
    if result:
        print(f"  Name: {result['name']}")
        print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")

    # Reverse geocoding
    print("\nReverse geocoding (35.6586, 139.7454):")
    result = geocoder.reverse(35.6586, 139.7454)
    if result:
        print(f"  Address: {result['display_name'][:60]}...")

    # Batch geocoding
    print("\nBatch geocoding:")
    places = ["Sydney Opera House", "Big Ben London"]
    results = geocoder.batch(places)
    for r in results:
        print(f"  - {r['name']}: ({r['lat']:.4f}, {r['lon']:.4f})")


# =============================================================================
# Example 9: Address Formatting
# =============================================================================

def example_address_formatting():
    """Demonstrate address formatting from components."""
    print("\n" + "="*60)
    print("Example 9: Address Formatting")
    print("="*60)

    def format_address(result: dict) -> str:
        """Format address from components."""
        address = result.get("address", {})

        parts = []

        # Street
        street_parts = []
        if address.get("house_number"):
            street_parts.append(address["house_number"])
        if address.get("road"):
            street_parts.append(address["road"])
        if street_parts:
            parts.append(" ".join(street_parts))

        # District/neighborhood
        district = (address.get("suburb") or
                   address.get("district") or
                   address.get("neighbourhood"))
        if district:
            parts.append(district)

        # City
        city = (address.get("city") or
                address.get("town") or
                address.get("village"))
        if city:
            parts.append(city)

        # Country
        if address.get("country"):
            parts.append(address["country"])

        return ", ".join(parts) if parts else "Unknown location"

    # Get some results with address details
    geocoder = Geocoder(USER_AGENT)

    places = ["Louvre Museum Paris", "Brandenburg Gate Berlin"]

    for place in places:
        result = geocoder.forward(place)
        if result:
            formatted = format_address(result)
            print(f"\n{place}:")
            print(f"  Formatted: {formatted}")


# =============================================================================
# Example 10: Interactive CLI Geocoder
# =============================================================================

def example_cli_geocoder():
    """Simple interactive CLI demo."""
    print("\n" + "="*60)
    print("Example 10: Interactive CLI Geocoder (Demo)")
    print("="*60)

    geocoder = Geocoder(USER_AGENT)

    # Simulate some CLI interactions
    demo_queries = [
        "Colosseum Rome",
        "reverse 41.8902 12.4922",
    ]

    for query in demo_queries:
        print(f"\ngeocoder> {query}")

        if query.startswith("reverse "):
            parts = query.split()
            if len(parts) == 3:
                try:
                    lat, lon = float(parts[1]), float(parts[2])
                    result = geocoder.reverse(lat, lon)
                    if result:
                        print(f"  Address: {result['display_name'][:60]}...")
                except ValueError:
                    print("  Invalid coordinates")
        else:
            result = geocoder.forward(query)
            if result:
                print(f"  Name: {result['name']}")
                print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")
            else:
                print("  Not found")


# =============================================================================
# Main Menu
# =============================================================================

def main():
    """Run selected examples."""
    print("="*60)
    print("Week 5: The Nominatim API (Geocoding) - Examples")
    print("="*60)
    print(f"User-Agent: {USER_AGENT}")

    examples = [
        ("1", "Basic Nominatim Search", example_basic_search),
        ("2", "Address Details", example_address_details),
        ("3", "Safe Dictionary Access", example_safe_get),
        ("4", "Parsing Results", example_parse_results),
        ("5", "Bounding Box", example_bounding_box),
        ("6", "Error Handling", example_error_handling),
        ("7", "Reverse Geocoding", example_reverse_geocoding),
        ("8", "Geocoder Class", example_geocoder_class),
        ("9", "Address Formatting", example_address_formatting),
        ("10", "CLI Demo", example_cli_geocoder),
    ]

    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print("  a. Run all examples")
    print("  q. Quit")

    while True:
        choice = input("\nEnter example number (or 'a' for all, 'q' to quit): ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == 'a':
            for _, _, func in examples:
                func()
                time.sleep(1)
            break
        else:
            for num, name, func in examples:
                if choice == num:
                    func()
                    break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
