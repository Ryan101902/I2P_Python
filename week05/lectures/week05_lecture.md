# Week 5: The Nominatim API (Geocoding)

## Lecture Overview (3 Hours)

**Phase 2: The API & The Cloud** — "Fetching the World"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand geocoding and reverse geocoding concepts
2. Parse complex nested JSON responses from real APIs
3. Use Python's error handling system effectively
4. Build a complete CLI geocoding tool
5. Handle edge cases and unexpected data gracefully
6. Implement robust data extraction patterns

### Prerequisites
- Week 4: HTTP Requests & API Keys
- Understanding of the `requests` library
- Basic JSON parsing knowledge

---

# Hour 1: Deep Dive into Nominatim

## 1.1 What is Geocoding?

**Geocoding** is the process of converting human-readable addresses or place names into geographic coordinates (latitude and longitude).

```
┌─────────────────────────┐     Geocoding      ┌─────────────────────┐
│    "Taipei 101"         │ ──────────────────> │ (25.0339, 121.5645) │
│    (Place Name)         │                     │   (Coordinates)     │
└─────────────────────────┘                     └─────────────────────┘

┌─────────────────────────┐  Reverse Geocoding  ┌─────────────────────┐
│  (25.0339, 121.5645)    │ ──────────────────> │ "Taipei 101, Xinyi  │
│    (Coordinates)        │                     │  Road, Taipei..."   │
└─────────────────────────┘                     └─────────────────────┘
```

### Why is Geocoding Important?

1. **Maps & Navigation**: Convert "Starbucks near me" to actual locations
2. **Data Analysis**: Plot addresses on maps for visualization
3. **Location Services**: Find nearby restaurants, hospitals, etc.
4. **Logistics**: Calculate delivery routes from addresses

---

## 1.2 Nominatim: OpenStreetMap's Geocoder

**Nominatim** (Latin for "by name") is the search engine for OpenStreetMap data.

### Key Features

| Feature | Description |
|---------|-------------|
| **Free** | No cost for reasonable usage |
| **Global** | Covers the entire world |
| **Open Data** | Based on community-contributed OpenStreetMap |
| **No API Key** | Just requires proper User-Agent |
| **Multiple Formats** | JSON, XML, HTML output |

### Nominatim Endpoints

| Endpoint | Purpose | Example Use |
|----------|---------|-------------|
| `/search` | Geocoding (name → coords) | Find "Taipei 101" |
| `/reverse` | Reverse geocoding (coords → name) | What's at (25.03, 121.56)? |
| `/lookup` | Look up by OSM ID | Get details for a specific place |
| `/status` | Check server status | Is the service running? |

---

## 1.3 The Search Endpoint in Detail

### Basic Request

```python
import requests

url = "https://nominatim.openstreetmap.org/search"

params = {
    "q": "Taipei 101",
    "format": "json"
}

headers = {
    "User-Agent": "CS101-Geocoder/1.0 (cs101@university.edu)"
}

response = requests.get(url, params=params, headers=headers, timeout=10)
results = response.json()
```

### All Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | Free-form search query | `"Taipei 101"` |
| `format` | string | Output format | `"json"`, `"jsonv2"`, `"xml"` |
| `limit` | int | Maximum results (1-50) | `5` |
| `addressdetails` | 0/1 | Include address breakdown | `1` |
| `extratags` | 0/1 | Include additional OSM tags | `1` |
| `namedetails` | 0/1 | Include all name variants | `1` |
| `countrycodes` | string | Limit to countries (ISO codes) | `"tw,jp"` |
| `viewbox` | string | Bounding box preference | `"lon1,lat1,lon2,lat2"` |
| `bounded` | 0/1 | Strict viewbox limit | `1` |
| `polygon_geojson` | 0/1 | Include boundary geometry | `1` |
| `dedupe` | 0/1 | Remove duplicates | `1` |

### Structured Search (Alternative)

Instead of free-form `q`, you can use structured parameters:

```python
params = {
    "street": "Section 5, Xinyi Road",
    "city": "Taipei",
    "country": "Taiwan",
    "format": "json"
}
```

| Parameter | Description |
|-----------|-------------|
| `street` | Street address |
| `city` | City name |
| `county` | County/district |
| `state` | State/province |
| `country` | Country name |
| `postalcode` | ZIP/postal code |

---

## 1.4 Understanding the Response Structure

A Nominatim search returns a **list of place objects**:

```json
[
    {
        "place_id": 297611768,
        "licence": "Data © OpenStreetMap contributors...",
        "osm_type": "way",
        "osm_id": 55284753,
        "lat": "25.0339639",
        "lon": "121.5644722",
        "class": "tourism",
        "type": "attraction",
        "place_rank": 30,
        "importance": 0.6864891756640247,
        "addresstype": "tourism",
        "name": "台北101",
        "display_name": "台北101, 7, Section 5, Xinyi Road, Xinyi District, Taipei, 110, Taiwan",
        "boundingbox": ["25.0329639", "25.0349639", "121.5634722", "121.5654722"]
    },
    ...
]
```

### Key Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `place_id` | int | Unique ID in Nominatim database |
| `osm_type` | string | OpenStreetMap type: "node", "way", "relation" |
| `osm_id` | int | ID in OpenStreetMap database |
| `lat` | string | Latitude (as string!) |
| `lon` | string | Longitude (as string!) |
| `class` | string | OSM classification (tourism, amenity, etc.) |
| `type` | string | Specific type (attraction, restaurant, etc.) |
| `importance` | float | Relevance score (0-1) |
| `display_name` | string | Full formatted address |
| `boundingbox` | list | Geographic bounding box [s, n, w, e] |

### Important: Lat/Lon Are Strings!

```python
# WRONG - will fail if you try math operations
lat = result["lat"]  # "25.0339639" (string)

# CORRECT - convert to float
lat = float(result["lat"])  # 25.0339639 (float)
```

---

## 1.5 Mini-Exercise 1: Parse a Response

Given this response, extract the place name, coordinates, and type:

```python
response_data = [
    {
        "place_id": 123456,
        "lat": "25.0478",
        "lon": "121.5170",
        "display_name": "Taipei Main Station, Zhongzheng District, Taipei, Taiwan",
        "type": "station",
        "class": "railway",
        "importance": 0.75
    }
]

# Extract:
# 1. The display name
# 2. Coordinates as floats in a tuple
# 3. The type and class combined as "class:type"
```

<details>
<summary>Solution</summary>

```python
response_data = [
    {
        "place_id": 123456,
        "lat": "25.0478",
        "lon": "121.5170",
        "display_name": "Taipei Main Station, Zhongzheng District, Taipei, Taiwan",
        "type": "station",
        "class": "railway",
        "importance": 0.75
    }
]

# Check if we have results
if response_data:
    place = response_data[0]

    # 1. Display name
    name = place["display_name"]
    print(f"Name: {name}")

    # 2. Coordinates as tuple of floats
    coords = (float(place["lat"]), float(place["lon"]))
    print(f"Coordinates: {coords}")

    # 3. Class and type
    category = f"{place['class']}:{place['type']}"
    print(f"Category: {category}")
else:
    print("No results!")

# Output:
# Name: Taipei Main Station, Zhongzheng District, Taipei, Taiwan
# Coordinates: (25.0478, 121.517)
# Category: railway:station
```

</details>

---

## 1.6 Address Details Response

When you add `addressdetails=1`:

```python
params = {
    "q": "Taipei 101",
    "format": "json",
    "addressdetails": 1
}
```

The response includes a nested `address` object:

```json
{
    "lat": "25.0339639",
    "lon": "121.5644722",
    "display_name": "台北101, 7, Section 5, Xinyi Road, ...",
    "address": {
        "tourism": "台北101",
        "house_number": "7",
        "road": "Section 5, Xinyi Road",
        "suburb": "Xinyi District",
        "city": "Taipei",
        "postcode": "110",
        "country": "Taiwan",
        "country_code": "tw"
    }
}
```

### Parsing Nested Address

```python
def parse_address(result: dict) -> dict:
    """Extract structured address from Nominatim result."""
    address = result.get("address", {})

    return {
        "name": result.get("name", address.get("tourism", "Unknown")),
        "street": address.get("road", ""),
        "number": address.get("house_number", ""),
        "district": address.get("suburb", address.get("district", "")),
        "city": address.get("city", address.get("town", "")),
        "country": address.get("country", ""),
        "postcode": address.get("postcode", "")
    }
```

---

# ☕ 5-Minute Break

Stand up, stretch, rest your eyes!

---

# Hour 2: Parsing Complex Nested JSON

## 2.1 The Challenge of Real-World JSON

Real API responses are messy:
- Fields may be **missing**
- Data types may be **inconsistent**
- Structures may be **deeply nested**
- Values may be **null or empty**

### Example: Inconsistent Responses

```python
# Response for "Taipei 101" (detailed)
{
    "name": "台北101",
    "address": {
        "tourism": "台北101",
        "road": "Section 5, Xinyi Road",
        "city": "Taipei"
    }
}

# Response for a small village (sparse)
{
    "name": "Some Village",
    "address": {
        "village": "Some Village",
        "country": "Taiwan"
    }
    # No road, no city!
}
```

---

## 2.2 Safe Dictionary Access

### The Problem with Direct Access

```python
# This will crash if "address" is missing!
city = result["address"]["city"]

# This will crash if result is an empty list!
first = results[0]
```

### Solution 1: The `.get()` Method

```python
# Returns None if key doesn't exist
city = result.get("address")

# Returns default value if key doesn't exist
city = result.get("city", "Unknown")

# Chained .get() for nested access
address = result.get("address", {})
city = address.get("city", "Unknown")
```

### Solution 2: Check Before Access

```python
# Check if key exists
if "address" in result:
    address = result["address"]
    if "city" in address:
        city = address["city"]

# Check if list is not empty
if results:
    first = results[0]
```

### Solution 3: Try/Except

```python
try:
    city = result["address"]["city"]
except KeyError:
    city = "Unknown"
except TypeError:  # If result["address"] is None
    city = "Unknown"
```

---

## 2.3 Building a Safe Data Extractor

Let's create a function that safely extracts data from nested structures:

```python
def safe_get(data: dict, *keys, default=None):
    """
    Safely get a nested value from a dictionary.

    Args:
        data: The dictionary to search
        *keys: The keys to traverse
        default: Value to return if path doesn't exist

    Returns:
        The value at the path, or default if not found

    Example:
        safe_get(result, "address", "city", default="Unknown")
    """
    current = data

    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int):
            try:
                current = current[key]
            except IndexError:
                return default
        else:
            return default

        if current is None:
            return default

    return current


# Usage
result = {
    "address": {
        "city": "Taipei",
        "district": "Xinyi"
    }
}

city = safe_get(result, "address", "city", default="Unknown")
print(city)  # "Taipei"

# Missing key returns default
state = safe_get(result, "address", "state", default="N/A")
print(state)  # "N/A"
```

---

## 2.4 Parsing Nominatim Results Robustly

Here's a complete, robust parser for Nominatim results:

```python
from typing import TypedDict, Optional

class GeocodedPlace(TypedDict):
    """Type definition for a geocoded place."""
    name: str
    lat: float
    lon: float
    display_name: str
    place_type: str
    importance: float
    address: dict


def parse_nominatim_result(result: dict) -> GeocodedPlace:
    """
    Parse a single Nominatim result into a clean structure.

    Args:
        result: Raw result from Nominatim API

    Returns:
        Cleaned GeocodedPlace dictionary
    """
    # Extract coordinates (convert strings to floats)
    try:
        lat = float(result.get("lat", 0))
        lon = float(result.get("lon", 0))
    except (ValueError, TypeError):
        lat, lon = 0.0, 0.0

    # Extract importance (with fallback)
    try:
        importance = float(result.get("importance", 0))
    except (ValueError, TypeError):
        importance = 0.0

    # Build clean result
    return {
        "name": result.get("name", result.get("display_name", "Unknown")),
        "lat": lat,
        "lon": lon,
        "display_name": result.get("display_name", ""),
        "place_type": f"{result.get('class', '')}:{result.get('type', '')}",
        "importance": importance,
        "address": result.get("address", {})
    }


def parse_nominatim_response(response_data: list) -> list[GeocodedPlace]:
    """
    Parse a full Nominatim response.

    Args:
        response_data: List of results from Nominatim

    Returns:
        List of cleaned GeocodedPlace dictionaries
    """
    if not response_data:
        return []

    return [parse_nominatim_result(r) for r in response_data]
```

---

## 2.5 Mini-Exercise 2: Handle Missing Data

Write a function that extracts a formatted address from a Nominatim result, handling all possible missing fields:

```python
def format_address(result: dict) -> str:
    """
    Format an address from Nominatim result.

    Should handle missing fields gracefully.
    Format: "street number, district, city, country"
    Skip empty parts.

    Examples:
        "7 Section 5 Xinyi Road, Xinyi, Taipei, Taiwan"
        "Shibuya, Tokyo, Japan"  (no street)
        "Taiwan"  (only country)
    """
    # Your code here
    pass


# Test with various results
test_cases = [
    # Complete address
    {
        "address": {
            "house_number": "7",
            "road": "Section 5 Xinyi Road",
            "suburb": "Xinyi District",
            "city": "Taipei",
            "country": "Taiwan"
        }
    },
    # Missing street
    {
        "address": {
            "suburb": "Shibuya",
            "city": "Tokyo",
            "country": "Japan"
        }
    },
    # Only country
    {
        "address": {
            "country": "Taiwan"
        }
    },
    # Empty address
    {
        "address": {}
    }
]

for case in test_cases:
    print(format_address(case))
```

<details>
<summary>Solution</summary>

```python
def format_address(result: dict) -> str:
    """
    Format an address from Nominatim result.
    """
    address = result.get("address", {})

    # Build street part
    street_parts = []
    if address.get("house_number"):
        street_parts.append(address["house_number"])
    if address.get("road"):
        street_parts.append(address["road"])
    street = " ".join(street_parts)

    # Collect all parts
    parts = []

    if street:
        parts.append(street)

    # Try different keys for district
    district = (address.get("suburb") or
                address.get("district") or
                address.get("neighbourhood"))
    if district:
        parts.append(district)

    # Try different keys for city
    city = (address.get("city") or
            address.get("town") or
            address.get("village") or
            address.get("municipality"))
    if city:
        parts.append(city)

    if address.get("country"):
        parts.append(address["country"])

    # Join with commas, or return "Unknown" if empty
    return ", ".join(parts) if parts else "Unknown location"


# Test
for case in test_cases:
    print(format_address(case))

# Output:
# 7 Section 5 Xinyi Road, Xinyi District, Taipei, Taiwan
# Shibuya, Tokyo, Japan
# Taiwan
# Unknown location
```

</details>

---

## 2.6 Working with Bounding Boxes

Nominatim returns bounding boxes as a list of strings:

```json
"boundingbox": ["25.0329", "25.0349", "121.5634", "121.5654"]
```

Format: `[south, north, west, east]`

```python
def parse_bounding_box(bbox: list) -> dict | None:
    """
    Parse a Nominatim bounding box.

    Args:
        bbox: List of [south, north, west, east] as strings

    Returns:
        Dictionary with float coordinates or None if invalid
    """
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
    """Calculate the center point of a bounding box."""
    lat = (bbox["south"] + bbox["north"]) / 2
    lon = (bbox["west"] + bbox["east"]) / 2
    return (lat, lon)


def bbox_area_km2(bbox: dict) -> float:
    """Estimate the area of a bounding box in km²."""
    # Approximate conversion at mid-latitudes
    lat_diff = bbox["north"] - bbox["south"]
    lon_diff = bbox["east"] - bbox["west"]

    # 1 degree lat ≈ 111 km
    # 1 degree lon ≈ 111 * cos(lat) km
    import math
    mid_lat = (bbox["north"] + bbox["south"]) / 2
    lat_km = lat_diff * 111
    lon_km = lon_diff * 111 * math.cos(math.radians(mid_lat))

    return lat_km * lon_km


# Example usage
result = {
    "boundingbox": ["25.0329", "25.0349", "121.5634", "121.5654"]
}

bbox = parse_bounding_box(result["boundingbox"])
if bbox:
    print(f"Center: {bbox_center(bbox)}")
    print(f"Area: {bbox_area_km2(bbox):.4f} km²")
```

---

# ☕ 10-Minute Break

Stretch, grab water, check your phone!

---

# Hour 3: Error Handling and Building a CLI Tool

## 3.1 Python Error Handling Fundamentals

### The `try/except` Statement

```python
try:
    # Code that might fail
    result = risky_operation()
except SomeError:
    # Handle the error
    print("Something went wrong")
```

### Catching Multiple Exceptions

```python
try:
    data = response.json()
    value = data["key"]
except json.JSONDecodeError:
    print("Invalid JSON")
except KeyError:
    print("Key not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### The Full `try/except/else/finally` Structure

```python
try:
    # Risky code
    file = open("data.json")
    data = json.load(file)
except FileNotFoundError:
    print("File not found")
    data = {}
except json.JSONDecodeError:
    print("Invalid JSON")
    data = {}
else:
    # Only runs if NO exception occurred
    print(f"Loaded {len(data)} items")
finally:
    # ALWAYS runs, even if there was an exception
    if 'file' in locals():
        file.close()
```

---

## 3.2 Common API-Related Exceptions

### Network Exceptions (from `requests`)

```python
import requests

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError for 4xx/5xx

except requests.exceptions.Timeout:
    # Server didn't respond in time
    print("Request timed out")

except requests.exceptions.ConnectionError:
    # Network problem (DNS failure, refused connection, etc.)
    print("Connection failed")

except requests.exceptions.HTTPError as e:
    # Server returned an error status (4xx, 5xx)
    print(f"HTTP error: {e.response.status_code}")

except requests.exceptions.RequestException as e:
    # Base class for all requests exceptions
    print(f"Request failed: {e}")
```

### Data Parsing Exceptions

```python
import json

try:
    # Parse JSON
    data = response.json()

    # Access nested data
    result = data[0]
    lat = float(result["lat"])
    name = result["address"]["city"]

except json.JSONDecodeError:
    # Response wasn't valid JSON
    print("Invalid JSON response")

except IndexError:
    # List was empty or index out of range
    print("No results found")

except KeyError as e:
    # Dictionary key doesn't exist
    print(f"Missing field: {e}")

except TypeError:
    # Wrong type (e.g., trying to index None)
    print("Unexpected data type")

except ValueError:
    # Conversion failed (e.g., float("not a number"))
    print("Invalid value format")
```

---

## 3.3 Designing Error Classes

For complex applications, create custom exception classes:

```python
class GeocodingError(Exception):
    """Base exception for geocoding errors."""
    pass


class NetworkError(GeocodingError):
    """Network-related errors."""
    pass


class RateLimitError(GeocodingError):
    """Rate limit exceeded."""
    pass


class NotFoundError(GeocodingError):
    """Place not found."""
    pass


class ParseError(GeocodingError):
    """Error parsing response."""
    pass


# Usage
def geocode(query: str) -> dict:
    """Geocode a place name."""
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 429:
            raise RateLimitError("Too many requests. Please wait.")

        if response.status_code != 200:
            raise NetworkError(f"HTTP {response.status_code}")

        data = response.json()

        if not data:
            raise NotFoundError(f"No results for: {query}")

        return parse_result(data[0])

    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Request failed: {e}")

    except (KeyError, IndexError, ValueError) as e:
        raise ParseError(f"Failed to parse response: {e}")


# Using the function
try:
    result = geocode("Taipei 101")
    print(result)
except NotFoundError:
    print("Place not found. Try a different search term.")
except RateLimitError:
    print("Too many requests. Wait a moment and try again.")
except NetworkError:
    print("Network problem. Check your internet connection.")
except GeocodingError as e:
    print(f"Geocoding failed: {e}")
```

---

## 3.4 Mini-Exercise 3: Error Handling Practice

Add proper error handling to this function:

```python
import requests

def get_coordinates(place_name: str) -> tuple[float, float]:
    """
    Get coordinates for a place name.

    Should handle:
    - Network errors
    - Empty results
    - Missing/invalid lat/lon

    Returns:
        Tuple of (latitude, longitude)

    Raises:
        ValueError: If place not found or invalid data
        ConnectionError: If network fails
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    # Add error handling here
    response = requests.get(url, params=params, headers=headers, timeout=10)
    data = response.json()
    result = data[0]
    lat = float(result["lat"])
    lon = float(result["lon"])
    return (lat, lon)
```

<details>
<summary>Solution</summary>

```python
import requests

def get_coordinates(place_name: str) -> tuple[float, float]:
    """
    Get coordinates for a place name.
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=10
        )

        # Check HTTP status
        if response.status_code != 200:
            raise ConnectionError(f"HTTP {response.status_code}")

        # Parse JSON
        data = response.json()

        # Check for results
        if not data:
            raise ValueError(f"No results found for: {place_name}")

        result = data[0]

        # Extract and convert coordinates
        if "lat" not in result or "lon" not in result:
            raise ValueError("Response missing coordinates")

        lat = float(result["lat"])
        lon = float(result["lon"])

        return (lat, lon)

    except requests.exceptions.Timeout:
        raise ConnectionError("Request timed out")

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Network connection failed")

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Request failed: {e}")

    except (KeyError, IndexError) as e:
        raise ValueError(f"Invalid response format: {e}")

    except (TypeError, ValueError) as e:
        if "could not convert" in str(e).lower():
            raise ValueError(f"Invalid coordinate format: {e}")
        raise


# Test
try:
    coords = get_coordinates("Taipei 101")
    print(f"Coordinates: {coords}")
except ValueError as e:
    print(f"Error: {e}")
except ConnectionError as e:
    print(f"Network error: {e}")
```

</details>

---

## 3.5 Building the Complete CLI Geocoder

Now let's build a complete, production-quality CLI geocoder:

```python
#!/usr/bin/env python3
"""
Geocoder CLI - Convert place names to coordinates.

Usage:
    python geocoder_cli.py
    python geocoder_cli.py "Taipei 101"
    python geocoder_cli.py --reverse 25.0339 121.5645
"""

import requests
import sys
import time
import json
from pathlib import Path


# =============================================================================
# Configuration
# =============================================================================

CONFIG = {
    "user_agent": "CS101-Geocoder/1.0 (cs101@university.edu)",
    "base_url": "https://nominatim.openstreetmap.org",
    "timeout": 10,
    "cache_file": ".geocache.json"
}


# =============================================================================
# Custom Exceptions
# =============================================================================

class GeocoderError(Exception):
    """Base exception for geocoder errors."""
    pass


class NetworkError(GeocoderError):
    """Network-related errors."""
    pass


class NotFoundError(GeocoderError):
    """Place not found."""
    pass


# =============================================================================
# Cache Functions
# =============================================================================

def load_cache() -> dict:
    """Load cache from file."""
    cache_path = Path(CONFIG["cache_file"])
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(cache: dict):
    """Save cache to file."""
    cache_path = Path(CONFIG["cache_file"])
    try:
        cache_path.write_text(json.dumps(cache, indent=2))
    except IOError:
        pass  # Cache save failure is not critical


def get_cached(query: str) -> dict | None:
    """Get cached result for a query."""
    cache = load_cache()
    return cache.get(query.lower())


def set_cached(query: str, result: dict):
    """Cache a result."""
    cache = load_cache()
    cache[query.lower()] = result
    save_cache(cache)


# =============================================================================
# Geocoding Functions
# =============================================================================

def geocode(query: str, use_cache: bool = True) -> dict:
    """
    Convert a place name to coordinates.

    Args:
        query: Place name to search
        use_cache: Whether to use cached results

    Returns:
        Dictionary with name, lat, lon, display_name

    Raises:
        NotFoundError: If place not found
        NetworkError: If network request fails
    """
    # Check cache first
    if use_cache:
        cached = get_cached(query)
        if cached:
            cached["cached"] = True
            return cached

    # Make API request
    url = f"{CONFIG['base_url']}/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    headers = {"User-Agent": CONFIG["user_agent"]}

    try:
        response = requests.get(
            url, params=params, headers=headers,
            timeout=CONFIG["timeout"]
        )

        if response.status_code == 429:
            raise NetworkError("Rate limit exceeded. Wait and try again.")

        if response.status_code != 200:
            raise NetworkError(f"HTTP {response.status_code}")

        data = response.json()

        if not data:
            raise NotFoundError(f"No results for: {query}")

        # Parse result
        result = data[0]
        parsed = {
            "name": result.get("name", query),
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result.get("display_name", ""),
            "type": f"{result.get('class', '')}:{result.get('type', '')}",
            "cached": False
        }

        # Cache the result
        if use_cache:
            set_cached(query, parsed)

        return parsed

    except requests.exceptions.Timeout:
        raise NetworkError("Request timed out")
    except requests.exceptions.ConnectionError:
        raise NetworkError("Connection failed")
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Request failed: {e}")
    except (KeyError, ValueError, TypeError) as e:
        raise GeocoderError(f"Failed to parse response: {e}")


def reverse_geocode(lat: float, lon: float) -> dict:
    """
    Convert coordinates to an address.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Dictionary with address information

    Raises:
        NotFoundError: If location not found
        NetworkError: If network request fails
    """
    url = f"{CONFIG['base_url']}/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1
    }
    headers = {"User-Agent": CONFIG["user_agent"]}

    try:
        response = requests.get(
            url, params=params, headers=headers,
            timeout=CONFIG["timeout"]
        )

        if response.status_code != 200:
            raise NetworkError(f"HTTP {response.status_code}")

        data = response.json()

        if "error" in data:
            raise NotFoundError(data["error"])

        return {
            "display_name": data.get("display_name", "Unknown"),
            "address": data.get("address", {}),
            "lat": lat,
            "lon": lon
        }

    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Request failed: {e}")


# =============================================================================
# CLI Interface
# =============================================================================

def print_result(result: dict):
    """Pretty print a geocoding result."""
    print()
    print(f"  Name: {result.get('name', 'N/A')}")
    print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")
    print(f"  Full address: {result.get('display_name', 'N/A')}")
    if result.get("type"):
        print(f"  Type: {result['type']}")
    if result.get("cached"):
        print("  (from cache)")
    print()


def print_reverse_result(result: dict):
    """Pretty print a reverse geocoding result."""
    print()
    print(f"  Address: {result['display_name']}")
    print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")

    address = result.get("address", {})
    if address:
        print("  Components:")
        for key, value in address.items():
            print(f"    {key}: {value}")
    print()


def interactive_mode():
    """Run the geocoder in interactive mode."""
    print("\n=== Geocoder CLI ===")
    print("Commands:")
    print("  <place name>     - Search for a place")
    print("  reverse <lat> <lon> - Reverse geocode")
    print("  quit             - Exit")
    print()

    last_request = 0

    while True:
        try:
            user_input = input("geocoder> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Rate limiting
        elapsed = time.time() - last_request
        if elapsed < 1:
            time.sleep(1 - elapsed)

        # Handle reverse geocoding
        if user_input.lower().startswith("reverse "):
            parts = user_input.split()
            if len(parts) != 3:
                print("Usage: reverse <lat> <lon>")
                continue

            try:
                lat = float(parts[1])
                lon = float(parts[2])
                result = reverse_geocode(lat, lon)
                print_reverse_result(result)
                last_request = time.time()
            except ValueError:
                print("Invalid coordinates. Use: reverse 25.0339 121.5645")
            except GeocoderError as e:
                print(f"Error: {e}")
            continue

        # Handle forward geocoding
        try:
            result = geocode(user_input)
            print_result(result)
            last_request = time.time()
        except NotFoundError as e:
            print(f"Not found: {e}")
        except NetworkError as e:
            print(f"Network error: {e}")
        except GeocoderError as e:
            print(f"Error: {e}")


def main():
    """Main entry point."""
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reverse" and len(sys.argv) == 4:
            try:
                lat = float(sys.argv[2])
                lon = float(sys.argv[3])
                result = reverse_geocode(lat, lon)
                print_reverse_result(result)
            except ValueError:
                print("Invalid coordinates")
                sys.exit(1)
            except GeocoderError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            query = " ".join(sys.argv[1:])
            try:
                result = geocode(query)
                print_result(result)
            except GeocoderError as e:
                print(f"Error: {e}")
                sys.exit(1)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
```

---

## 3.6 Mini-Exercise 4: Extend the CLI

Add these features to the CLI:

1. A `search` command that returns multiple results
2. A `--json` flag to output results as JSON

```python
# Example usage:
# geocoder> search taipei station
# 1. Taipei Main Station, ...
# 2. Taipei City Hall Station, ...
# 3. ...

# $ python geocoder_cli.py --json "Taipei 101"
# {"name": "Taipei 101", "lat": 25.0339, "lon": 121.5645, ...}
```

<details>
<summary>Solution Hints</summary>

```python
# For search command, modify geocode() to accept a limit parameter:

def geocode(query: str, limit: int = 1, use_cache: bool = True) -> list[dict]:
    """Modified to return multiple results."""
    params = {
        "q": query,
        "format": "json",
        "limit": limit,  # Changed from hardcoded 1
        "addressdetails": 1
    }
    # ... rest of the function

    # Parse ALL results, not just the first
    results = []
    for item in data[:limit]:
        parsed = {
            "name": item.get("name", query),
            "lat": float(item["lat"]),
            "lon": float(item["lon"]),
            # ...
        }
        results.append(parsed)

    return results


# For --json flag, check sys.argv and use json.dumps():

def main():
    json_output = "--json" in sys.argv
    if json_output:
        sys.argv.remove("--json")

    # ... do geocoding ...

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)
```

</details>

---

## 3.7 Best Practices Summary

### Error Handling Best Practices

1. **Be Specific**: Catch specific exceptions, not bare `except:`
2. **Fail Fast**: Validate inputs early
3. **Provide Context**: Include useful information in error messages
4. **Don't Silence Errors**: Log or report errors, don't ignore them
5. **Use Custom Exceptions**: Create domain-specific exception classes

### API Integration Best Practices

1. **Always Set Timeouts**: Never let requests hang forever
2. **Respect Rate Limits**: Add delays between requests
3. **Cache Results**: Don't repeat identical requests
4. **Validate Responses**: Check status codes and data structure
5. **Handle All Error Cases**: Network, parsing, and data errors

### Data Parsing Best Practices

1. **Use `.get()` with Defaults**: Avoid KeyError crashes
2. **Convert Types Explicitly**: Don't assume strings are numbers
3. **Validate Before Use**: Check that data exists and is valid
4. **Handle Missing Data**: Provide sensible defaults or skip

---

## 3.8 Homework Assignments

### Assignment 1: Batch Geocoder (Basic)
Create a script that:
1. Reads place names from a text file (one per line)
2. Geocodes each place with rate limiting
3. Writes results to a JSON file
4. Handles errors gracefully (skip failed places, don't crash)

### Assignment 2: Address Formatter (Intermediate)
Create a function that:
1. Takes a Nominatim result with `addressdetails`
2. Formats it according to the country's conventions:
   - Taiwan: "District, City, Country"
   - USA: "Street, City, State ZIP"
   - Japan: "Prefecture City District"
3. Handles missing fields gracefully

### Assignment 3: Geocoder with Fallback (Advanced)
Enhance the geocoder to:
1. Try exact match first
2. If no results, try removing punctuation
3. If still no results, try just the first few words
4. Cache all attempts to avoid repeated failures

---

## Additional Resources

### Documentation
- [Nominatim API Documentation](https://nominatim.org/release-docs/latest/api/Overview/)
- [OpenStreetMap Wiki - Nominatim](https://wiki.openstreetmap.org/wiki/Nominatim)
- [Python Requests - Error Handling](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)

### Alternative Geocoding Services
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding) (paid)
- [Mapbox Geocoding](https://docs.mapbox.com/api/search/geocoding/) (freemium)
- [HERE Geocoding](https://developer.here.com/documentation/geocoding-search-api/) (freemium)

### Practice
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Practice parsing nested JSON
- [httpbin.org](https://httpbin.org/) - Test error handling

---

## Next Week Preview

**Week 6: Searching for Places (Lazy Loading)**
- Query parameters and pagination
- Python generators and `yield`
- Lazy evaluation for memory efficiency
- Building a paginated search interface

---

*End of Week 5 Lecture*
