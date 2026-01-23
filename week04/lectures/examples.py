"""
Week 4: HTTP Requests & API Keys
Lecture Examples - Runnable Code

This file contains all the code examples from the Week 4 lecture.
Run this file to see the examples in action!

Usage:
    python examples.py

Note: Some examples make real API calls and require internet connection.
"""

import requests
import time
import json
import hashlib
from pathlib import Path


# =============================================================================
# Configuration
# =============================================================================

# IMPORTANT: Replace with your actual email for Nominatim requests
USER_AGENT = "CS101-Examples/1.0 (cs101@university.edu)"


# =============================================================================
# Example 1: Basic GET Request
# =============================================================================

def example_basic_request():
    """Make a simple GET request to httpbin.org."""
    print("\n" + "="*60)
    print("Example 1: Basic GET Request")
    print("="*60)

    # Make a GET request
    response = requests.get("https://httpbin.org/get")

    # Explore the response object
    print(f"Status Code: {response.status_code}")
    print(f"OK? {response.ok}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    print(f"Response size: {len(response.text)} characters")

    # Parse JSON
    data = response.json()
    print(f"Your IP: {data.get('origin', 'unknown')}")


# =============================================================================
# Example 2: Query Parameters
# =============================================================================

def example_query_params():
    """Demonstrate how to use query parameters."""
    print("\n" + "="*60)
    print("Example 2: Query Parameters")
    print("="*60)

    url = "https://httpbin.org/get"

    # Using params dict (recommended)
    params = {
        "city": "Taipei",
        "country": "Taiwan",
        "population": 2600000,
        "query": "coffee shop"  # Spaces are auto-encoded
    }

    response = requests.get(url, params=params)

    print(f"Constructed URL: {response.url}")
    print(f"\nParams sent:")
    for key, value in response.json()['args'].items():
        print(f"  {key}: {value}")


# =============================================================================
# Example 3: Custom Headers
# =============================================================================

def example_custom_headers():
    """Demonstrate how to send custom headers."""
    print("\n" + "="*60)
    print("Example 3: Custom Headers")
    print("="*60)

    url = "https://httpbin.org/headers"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "X-Custom-Header": "Hello from Python!",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)

    print("Headers received by server:")
    for key, value in response.json()['headers'].items():
        print(f"  {key}: {value}")


# =============================================================================
# Example 4: Simple Nominatim Geocoding
# =============================================================================

def example_nominatim_simple():
    """Make a simple geocoding request to Nominatim."""
    print("\n" + "="*60)
    print("Example 4: Simple Nominatim Geocoding")
    print("="*60)

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": "Taipei 101",
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    print(f"Searching for: {params['q']}")

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code == 200:
        results = response.json()
        if results:
            place = results[0]
            print(f"Found: {place['display_name'][:60]}...")
            print(f"Latitude: {place['lat']}")
            print(f"Longitude: {place['lon']}")
            print(f"Type: {place.get('type', 'N/A')}")
        else:
            print("No results found")
    else:
        print(f"Error: HTTP {response.status_code}")


# =============================================================================
# Example 5: Geocoding Function
# =============================================================================

def geocode(place_name: str) -> dict | None:
    """
    Convert a place name to coordinates using Nominatim.

    Args:
        place_name: Name of the place to search

    Returns:
        Dictionary with name, lat, lon or None if not found
    """
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            results = response.json()

            if results:
                place = results[0]
                return {
                    "name": place["display_name"],
                    "lat": float(place["lat"]),
                    "lon": float(place["lon"])
                }

        return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def example_geocode_function():
    """Demonstrate the geocode function."""
    print("\n" + "="*60)
    print("Example 5: Geocoding Function")
    print("="*60)

    places = [
        "National Taiwan University",
        "Shibuya Station Tokyo",
        "Eiffel Tower Paris"
    ]

    for i, place in enumerate(places):
        if i > 0:
            print("Waiting 1 second (rate limiting)...")
            time.sleep(1)

        print(f"\nGeocoding: {place}")
        result = geocode(place)

        if result:
            print(f"  Found: {result['name'][:50]}...")
            print(f"  Coordinates: ({result['lat']:.4f}, {result['lon']:.4f})")
        else:
            print("  Not found!")


# =============================================================================
# Example 6: Reverse Geocoding
# =============================================================================

def reverse_geocode(lat: float, lon: float) -> str | None:
    """
    Convert coordinates to an address using Nominatim.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Address string or None if not found
    """
    url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()
            return result.get("display_name")

        return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def example_reverse_geocode():
    """Demonstrate reverse geocoding."""
    print("\n" + "="*60)
    print("Example 6: Reverse Geocoding")
    print("="*60)

    # Famous locations
    locations = [
        (25.0339, 121.5645, "Taipei 101"),
        (35.6586, 139.7454, "Tokyo Tower"),
        (48.8584, 2.2945, "Eiffel Tower")
    ]

    for i, (lat, lon, expected) in enumerate(locations):
        if i > 0:
            print("Waiting 1 second (rate limiting)...")
            time.sleep(1)

        print(f"\nCoordinates: ({lat}, {lon})")
        print(f"Expected: {expected}")

        address = reverse_geocode(lat, lon)

        if address:
            print(f"Address: {address[:70]}...")
        else:
            print("Address not found!")


# =============================================================================
# Example 7: Error Handling
# =============================================================================

def example_error_handling():
    """Demonstrate comprehensive error handling."""
    print("\n" + "="*60)
    print("Example 7: Error Handling")
    print("="*60)

    test_cases = [
        ("https://httpbin.org/get", "Normal request"),
        ("https://httpbin.org/status/404", "404 Not Found"),
        ("https://httpbin.org/status/500", "500 Server Error"),
        ("https://invalid.domain.example/test", "Invalid domain"),
    ]

    for url, description in test_cases:
        print(f"\n{description}: {url}")

        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(f"  Success!")
            elif response.status_code == 404:
                print(f"  Not found (404)")
            elif response.status_code >= 500:
                print(f"  Server error ({response.status_code})")
            else:
                print(f"  HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            print("  Timeout!")

        except requests.exceptions.ConnectionError:
            print("  Connection failed!")

        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}")


# =============================================================================
# Example 8: Rate Limiter Class
# =============================================================================

class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self, calls_per_second: float = 1.0):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0

    def wait(self):
        """Wait if needed to respect rate limit."""
        now = time.time()
        elapsed = now - self.last_call

        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            print(f"  Rate limiting: waiting {sleep_time:.2f}s...")
            time.sleep(sleep_time)

        self.last_call = time.time()


def example_rate_limiter():
    """Demonstrate the RateLimiter class."""
    print("\n" + "="*60)
    print("Example 8: Rate Limiter")
    print("="*60)

    limiter = RateLimiter(calls_per_second=1)

    urls = [
        "https://httpbin.org/get?n=1",
        "https://httpbin.org/get?n=2",
        "https://httpbin.org/get?n=3"
    ]

    for url in urls:
        limiter.wait()
        print(f"Requesting: {url}")
        response = requests.get(url, timeout=5)
        print(f"  Status: {response.status_code}")


# =============================================================================
# Example 9: Nominatim Client with Rate Limiting
# =============================================================================

class NominatimClient:
    """Client for Nominatim API with built-in rate limiting."""

    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self, user_agent: str):
        self.headers = {"User-Agent": user_agent}
        self.rate_limiter = RateLimiter(calls_per_second=1)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search for places by name."""
        self.rate_limiter.wait()

        response = requests.get(
            f"{self.BASE_URL}/search",
            params={"q": query, "format": "json", "limit": limit},
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
        return []

    def reverse(self, lat: float, lon: float) -> dict | None:
        """Reverse geocode coordinates to address."""
        self.rate_limiter.wait()

        response = requests.get(
            f"{self.BASE_URL}/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
        return None


def example_nominatim_client():
    """Demonstrate the NominatimClient class."""
    print("\n" + "="*60)
    print("Example 9: Nominatim Client")
    print("="*60)

    client = NominatimClient(USER_AGENT)

    # Search
    print("\nSearching for 'Taipei Main Station'...")
    results = client.search("Taipei Main Station", limit=2)

    if results:
        for i, place in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"    Name: {place['display_name'][:50]}...")
            print(f"    Coords: ({place['lat']}, {place['lon']})")

    # Reverse
    print("\nReverse geocoding (25.0478, 121.5170)...")
    result = client.reverse(25.0478, 121.5170)

    if result:
        print(f"  Address: {result['display_name'][:60]}...")


# =============================================================================
# Example 10: Caching API Responses
# =============================================================================

class CachedNominatimClient:
    """Nominatim client with file-based caching."""

    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self, user_agent: str, cache_dir: str = ".cache"):
        self.headers = {"User-Agent": user_agent}
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.rate_limiter = RateLimiter(calls_per_second=1)

    def _cache_key(self, endpoint: str, params: dict) -> str:
        """Generate a unique cache key for a request."""
        key_data = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _get_cached(self, cache_key: str) -> dict | None:
        """Try to get cached response."""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            print(f"  Cache HIT: {cache_key[:8]}...")
            return json.loads(cache_file.read_text())

        print(f"  Cache MISS: {cache_key[:8]}...")
        return None

    def _save_cache(self, cache_key: str, data):
        """Save response to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_file.write_text(json.dumps(data, indent=2))

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search with caching."""
        params = {"q": query, "format": "json", "limit": limit}
        cache_key = self._cache_key("search", params)

        # Try cache first
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        # Make API call
        self.rate_limiter.wait()
        response = requests.get(
            f"{self.BASE_URL}/search",
            params=params,
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            self._save_cache(cache_key, data)
            return data

        return []


def example_caching():
    """Demonstrate caching API responses."""
    print("\n" + "="*60)
    print("Example 10: Caching API Responses")
    print("="*60)

    client = CachedNominatimClient(USER_AGENT, cache_dir=".week04_cache")

    # First call - hits API
    print("\nFirst call for 'Taipei Zoo':")
    results1 = client.search("Taipei Zoo")
    if results1:
        print(f"  Found: {results1[0]['display_name'][:50]}...")

    # Second call - uses cache (instant!)
    print("\nSecond call for 'Taipei Zoo' (should use cache):")
    results2 = client.search("Taipei Zoo")
    if results2:
        print(f"  Found: {results2[0]['display_name'][:50]}...")


# =============================================================================
# Main - Run All Examples
# =============================================================================

def main():
    """Run selected examples."""
    print("="*60)
    print("Week 4: HTTP Requests & API Keys - Examples")
    print("="*60)
    print(f"User-Agent: {USER_AGENT}")

    examples = [
        ("1", "Basic GET Request", example_basic_request),
        ("2", "Query Parameters", example_query_params),
        ("3", "Custom Headers", example_custom_headers),
        ("4", "Simple Nominatim", example_nominatim_simple),
        ("5", "Geocode Function", example_geocode_function),
        ("6", "Reverse Geocode", example_reverse_geocode),
        ("7", "Error Handling", example_error_handling),
        ("8", "Rate Limiter", example_rate_limiter),
        ("9", "Nominatim Client", example_nominatim_client),
        ("10", "Caching", example_caching),
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
                time.sleep(1)  # Pause between examples
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
