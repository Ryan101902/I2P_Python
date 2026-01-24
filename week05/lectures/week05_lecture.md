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

### Why This Matters

In real-world programming, you rarely work with clean, predictable data. APIs return messy, inconsistent responses. Networks fail. Users enter unexpected inputs. This week, we'll learn to write **defensive code** that handles these challenges gracefully.

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

### Think of it Like a Dictionary

- **Geocoding** is like looking up a word to find its definition
  - Input: "Taipei 101" (the word)
  - Output: (25.0339, 121.5645) (the definition)

- **Reverse Geocoding** is like looking up a definition to find the word
  - Input: (25.0339, 121.5645) (the definition)
  - Output: "Taipei 101, Xinyi Road..." (the word)

### Why is Geocoding Important?

Geocoding is **everywhere** in modern applications:

1. **Maps & Navigation**
   - When you type "Starbucks near me" in Google Maps
   - The app geocodes "Starbucks" to find coordinates of nearby locations

2. **Food Delivery Apps**
   - You enter "123 Main Street"
   - The app converts it to coordinates to show you on a map and calculate delivery routes

3. **Data Analysis & Visualization**
   - A company has 10,000 customer addresses
   - Geocoding converts them to coordinates for plotting on a heat map

4. **Location-Based Services**
   - "Find hospitals within 5km"
   - First geocode your location, then search for hospitals near those coordinates

5. **Logistics & Shipping**
   - Delivery companies geocode addresses to optimize routes
   - Calculate distances between warehouses and destinations

### The Geocoding Process (Behind the Scenes)

When you geocode "Taipei 101", the service:

1. **Parses** your query to understand what you're looking for
2. **Searches** a massive database of places and addresses
3. **Ranks** results by relevance (importance score)
4. **Returns** the best matches with coordinates

```
User Query: "Taipei 101"
    │
    ▼
┌─────────────────────┐
│  Query Parser       │  → Understands: building name, Taiwan
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Database Search    │  → Finds: 3 possible matches
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Ranking Algorithm  │  → Best match: Taipei 101 Tower (importance: 0.68)
└─────────────────────┘
    │
    ▼
Result: lat=25.0339, lon=121.5645
```

---

## 1.2 Nominatim: OpenStreetMap's Geocoder

**Nominatim** (Latin for "by name") is the search engine for OpenStreetMap data.

### What is OpenStreetMap?

OpenStreetMap (OSM) is like **Wikipedia for maps**:
- **Community-driven**: Volunteers worldwide add and update map data
- **Free and open**: Anyone can use the data
- **Comprehensive**: Contains streets, buildings, parks, businesses, and more
- **Global coverage**: Maps the entire world

### Why Use Nominatim?

| Feature | Description | Why It Matters |
|---------|-------------|----------------|
| **Free** | No cost for reasonable usage | Perfect for learning and small projects |
| **No API Key** | Just needs proper User-Agent | Easy to get started |
| **Global Coverage** | Entire world mapped | Works for any location |
| **Open Data** | Community-contributed | Transparent, improvable |
| **Multiple Formats** | JSON, XML, HTML | Flexible for different needs |

### Nominatim vs Commercial Geocoders

| Aspect | Nominatim | Google/Mapbox |
|--------|-----------|---------------|
| **Cost** | Free | Paid (after free tier) |
| **Setup** | User-Agent only | API key required |
| **Rate Limit** | 1 req/second | Higher limits |
| **Accuracy** | Good (varies by region) | Generally better |
| **Support** | Community | Professional |

**For learning**: Nominatim is perfect—it's free, easy to use, and teaches real-world API concepts.

### Nominatim Endpoints

An **endpoint** is a specific URL path that performs a particular function:

| Endpoint | Purpose | When to Use |
|----------|---------|-------------|
| `/search` | Geocoding (name → coords) | "Where is Taipei 101?" |
| `/reverse` | Reverse geocoding (coords → name) | "What's at 25.03, 121.56?" |
| `/lookup` | Look up by OSM ID | Get details for a specific place |
| `/status` | Check server status | Is the service running? |

We'll focus on `/search` and `/reverse` in this course.

---

## 1.3 The Search Endpoint in Detail

### Basic Request Structure

Let's break down a geocoding request step by step:

```python
import requests

# Step 1: Define the API endpoint URL
url = "https://nominatim.openstreetmap.org/search"

# Step 2: Define what we're searching for (query parameters)
params = {
    "q": "Taipei 101",      # The search query
    "format": "json"        # We want JSON response
}

# Step 3: Identify ourselves (REQUIRED by Nominatim)
headers = {
    "User-Agent": "CS101-Geocoder/1.0 (cs101@university.edu)"
}

# Step 4: Make the request
response = requests.get(url, params=params, headers=headers, timeout=10)

# Step 5: Parse the JSON response
results = response.json()

# Step 6: Use the results
if results:
    place = results[0]
    print(f"Found: {place['display_name']}")
    print(f"Coordinates: ({place['lat']}, {place['lon']})")
```

### Understanding Each Step

**Step 1 - The URL**: This is the "address" of the API endpoint. Think of it like a phone number for a specific service.

**Step 2 - Query Parameters**: These tell the API what you want:
- `q` = "query" = what you're searching for
- `format` = what format you want the response in

**Step 3 - Headers**: Metadata about your request. The User-Agent identifies who you are (required by Nominatim to prevent abuse).

**Step 4 - The Request**: `requests.get()` sends your request to the server and waits for a response. The `timeout=10` means "give up after 10 seconds".

**Step 5 - Parse JSON**: Convert the response text into Python data structures (lists and dictionaries).

**Step 6 - Use Results**: Check if we got results and extract the data we need.

### All Search Parameters

Nominatim accepts many parameters to customize your search:

#### Basic Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | Free-form search query | `"Taipei 101"` |
| `format` | string | Output format | `"json"`, `"jsonv2"`, `"xml"` |
| `limit` | int | Maximum results (1-50) | `5` |

#### Detail Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `addressdetails` | 0/1 | Include address breakdown | `1` |
| `extratags` | 0/1 | Include additional OSM tags | `1` |
| `namedetails` | 0/1 | Include all name variants | `1` |

#### Geographic Filtering

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `countrycodes` | string | Limit to countries (ISO codes) | `"tw,jp"` |
| `viewbox` | string | Bounding box preference | `"lon1,lat1,lon2,lat2"` |
| `bounded` | 0/1 | Strict viewbox limit | `1` |

### Example: Search with Multiple Parameters

```python
params = {
    "q": "coffee shop",
    "format": "json",
    "limit": 5,                    # Get up to 5 results
    "countrycodes": "tw",          # Only Taiwan
    "addressdetails": 1,           # Include address breakdown
    "viewbox": "121.5,25.0,121.6,25.1",  # Taipei area
    "bounded": 1                   # Strict - only within viewbox
}
```

**What this does**:
- Searches for "coffee shop"
- Returns up to 5 results
- Only in Taiwan
- Only within the Taipei area bounding box
- Includes detailed address information

### Structured Search (Alternative)

Instead of a free-form query (`q`), you can search by address components:

```python
# Free-form (less precise)
params = {"q": "7 Section 5 Xinyi Road Taipei Taiwan", "format": "json"}

# Structured (more precise)
params = {
    "street": "7 Section 5 Xinyi Road",
    "city": "Taipei",
    "country": "Taiwan",
    "format": "json"
}
```

**When to use structured search**:
- When you have clean, separated address components
- When you need more precise results
- When free-form search gives unexpected results

---

## 1.4 Understanding the Response Structure

When you make a search request, Nominatim returns a **list of place objects**. Let's examine the response in detail:

### Sample Response

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
    }
]
```

### Key Fields Explained

Let's understand what each field means:

#### Identification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `place_id` | int | Unique ID in Nominatim's database | `297611768` |
| `osm_id` | int | ID in OpenStreetMap database | `55284753` |
| `osm_type` | string | Type in OSM | `"way"` |

**Understanding `osm_type`**:
- `"node"` = A single point (e.g., a café, ATM)
- `"way"` = A line or polygon (e.g., a road, building outline)
- `"relation"` = A complex structure (e.g., a transit route, administrative boundary)

Taipei 101 is a `"way"` because it's represented as a building outline (polygon).

#### Location Fields

| Field | Type | Description | Note |
|-------|------|-------------|------|
| `lat` | **string** | Latitude | **Must convert to float!** |
| `lon` | **string** | Longitude | **Must convert to float!** |
| `boundingbox` | list | Geographic extent | [south, north, west, east] |

**Critical Warning**: `lat` and `lon` are **strings**, not numbers!

```python
# WRONG - lat is a string!
result["lat"] + 1  # TypeError: can only concatenate str to str

# CORRECT - convert to float first
float(result["lat"]) + 1  # Works: 26.0339639
```

#### Classification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `class` | string | Broad category | `"tourism"`, `"amenity"`, `"highway"` |
| `type` | string | Specific type | `"attraction"`, `"restaurant"`, `"bus_stop"` |
| `addresstype` | string | How it fits in an address | `"tourism"`, `"road"` |

**Common class/type combinations**:
- `tourism:attraction` - Tourist attractions
- `amenity:restaurant` - Restaurants
- `amenity:cafe` - Cafes
- `highway:bus_stop` - Bus stops
- `building:yes` - Generic buildings

#### Ranking Fields

| Field | Type | Description | Range |
|-------|------|-------------|-------|
| `importance` | float | How notable/famous | 0.0 to 1.0 |
| `place_rank` | int | Granularity level | 1-30 |

**Understanding `importance`**:
- Higher = more famous/notable
- Eiffel Tower: ~0.8
- Taipei 101: ~0.68
- Local coffee shop: ~0.2

**Understanding `place_rank`**:
- Lower = larger/more important administratively
- Country: ~4
- City: ~16
- Building: ~30

#### Display Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Short name |
| `display_name` | string | Full formatted address |

```python
result["name"]         # "台北101"
result["display_name"] # "台北101, 7, Section 5, Xinyi Road, Xinyi District, Taipei, 110, Taiwan"
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

**Think about**:
- What if the list is empty?
- What if `lat` or `lon` is missing?
- What type are `lat` and `lon`?

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

# First, check if we have any results
if response_data:
    # Get the first result
    place = response_data[0]

    # 1. Display name - simple dictionary access
    name = place["display_name"]
    print(f"Name: {name}")

    # 2. Coordinates - must convert strings to floats!
    lat = float(place["lat"])
    lon = float(place["lon"])
    coords = (lat, lon)
    print(f"Coordinates: {coords}")

    # 3. Class and type combined
    category = f"{place['class']}:{place['type']}"
    print(f"Category: {category}")
else:
    print("No results found!")

# Output:
# Name: Taipei Main Station, Zhongzheng District, Taipei, Taiwan
# Coordinates: (25.0478, 121.517)
# Category: railway:station
```

**Key points**:
1. Always check if `response_data` is not empty before accessing `[0]`
2. Convert `lat` and `lon` from strings to floats
3. Use f-strings to combine values

</details>

---

## 1.6 Address Details Response

When you add `addressdetails=1` to your request:

```python
params = {
    "q": "Taipei 101",
    "format": "json",
    "addressdetails": 1  # Include address breakdown
}
```

The response includes a nested `address` object with structured information:

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

### Understanding the Address Object

The `address` object contains **components** of the address, but the keys vary depending on the place type:

**For a tourist attraction (Taipei 101)**:
```json
{
    "tourism": "台北101",        // The name, keyed by class
    "house_number": "7",
    "road": "Section 5, Xinyi Road",
    "suburb": "Xinyi District",  // District/neighborhood
    "city": "Taipei",
    "country": "Taiwan"
}
```

**For a small village**:
```json
{
    "village": "Some Village",   // No "city" - uses "village"
    "county": "Some County",
    "country": "Taiwan"
    // No road, no suburb!
}
```

**This inconsistency is a major challenge** we'll address in Hour 2.

### Parsing Nested Address Data

Here's a function that handles the nested structure:

```python
def parse_address(result: dict) -> dict:
    """
    Extract structured address from Nominatim result.

    Args:
        result: A single Nominatim result dictionary

    Returns:
        Dictionary with standardized address fields
    """
    # Step 1: Get the address object (or empty dict if missing)
    address = result.get("address", {})

    # Step 2: Extract each component with fallbacks
    return {
        # Name could be under different keys depending on place type
        "name": result.get("name", address.get("tourism", "Unknown")),

        # Street information
        "street": address.get("road", ""),
        "number": address.get("house_number", ""),

        # Area - try multiple possible keys
        "district": address.get("suburb", address.get("district", "")),

        # City - might be "city", "town", or "village"
        "city": address.get("city", address.get("town", "")),

        # Country info
        "country": address.get("country", ""),
        "postcode": address.get("postcode", "")
    }
```

**Key technique**: Use `.get()` with fallback values to handle missing keys.

---

# ☕ 5-Minute Break

Stand up, stretch, rest your eyes!

---

# Hour 2: Parsing Complex Nested JSON

## 2.1 The Challenge of Real-World JSON

In Week 3, we worked with clean, predictable JSON files that we created ourselves. Real API responses are much messier:

### The Problems You'll Encounter

1. **Missing Fields**: Some responses have fields, others don't
2. **Inconsistent Types**: Sometimes a field is a string, sometimes null
3. **Varying Structures**: Different results have different shapes
4. **Deeply Nested Data**: Data buried many levels deep
5. **Empty Responses**: Sometimes the API returns nothing

### Example: Inconsistent Responses

Here are two real Nominatim responses showing how different they can be:

```python
# Response for "Taipei 101" - a major landmark
{
    "name": "台北101",
    "display_name": "台北101, 7, Section 5, Xinyi Road, Xinyi District, Taipei, Taiwan",
    "address": {
        "tourism": "台北101",
        "house_number": "7",
        "road": "Section 5, Xinyi Road",
        "suburb": "Xinyi District",
        "city": "Taipei",
        "postcode": "110",
        "country": "Taiwan",
        "country_code": "tw"
    },
    "importance": 0.68
}

# Response for a small village - much sparser
{
    "name": "Some Village",
    "display_name": "Some Village, Some County, Taiwan",
    "address": {
        "village": "Some Village",
        "county": "Some County",
        "country": "Taiwan",
        "country_code": "tw"
    }
    # Notice: no road, no city, no postcode, no importance!
}
```

### What Happens If We Don't Handle This?

```python
# Code that assumes all fields exist
def get_city(result):
    return result["address"]["city"]

# Works for Taipei 101
city = get_city(taipei_101_result)  # "Taipei"

# CRASHES for village
city = get_city(village_result)     # KeyError: 'city'
```

**Our goal**: Write code that works for **all** responses, not just the "nice" ones.

---

## 2.2 Safe Dictionary Access

### The Problem with Direct Access

Direct dictionary access (`dict["key"]`) crashes if the key doesn't exist:

```python
result = {"name": "Taipei 101"}

# This works
name = result["name"]  # "Taipei 101"

# This CRASHES
city = result["city"]  # KeyError: 'city'

# Nested access - even more dangerous
city = result["address"]["city"]  # KeyError: 'address'
```

### Solution 1: The `.get()` Method

The `.get()` method returns `None` (or a default value) if the key doesn't exist:

```python
result = {"name": "Taipei 101"}

# Basic .get() - returns None if missing
city = result.get("city")
print(city)  # None

# .get() with default value
city = result.get("city", "Unknown")
print(city)  # "Unknown"

# Chained .get() for nested access
# First get "address" (or empty dict), then get "city" from that
address = result.get("address", {})
city = address.get("city", "Unknown")
print(city)  # "Unknown"
```

**Why `{}` as the default for nested dicts?**

```python
# If we use None as default:
address = result.get("address")  # None
city = address.get("city")       # AttributeError: 'NoneType' has no attribute 'get'

# If we use {} as default:
address = result.get("address", {})  # {}
city = address.get("city", "Unknown")  # "Unknown" - works!
```

### Solution 2: Check Before Access

Use `in` operator or `if` statements to check first:

```python
result = {"name": "Taipei 101", "address": {"city": "Taipei"}}

# Check if key exists
if "address" in result:
    address = result["address"]
    if "city" in address:
        city = address["city"]
    else:
        city = "Unknown"
else:
    city = "Unknown"

# Check if list is not empty
results = []
if results:  # Empty list is "falsy"
    first = results[0]
else:
    first = None
```

**This works but gets verbose** for deeply nested data.

### Solution 3: Try/Except

Wrap risky code in try/except blocks:

```python
result = {"name": "Taipei 101"}

try:
    city = result["address"]["city"]
except KeyError:
    city = "Unknown"
except TypeError:  # Handles case where result["address"] is None
    city = "Unknown"
```

**When to use each approach**:

| Approach | Use When |
|----------|----------|
| `.get()` | Simple, one-level access |
| `if/in` | You need to do different things based on presence |
| `try/except` | Deep nesting or when errors are expected |

---

## 2.3 Building a Safe Data Extractor

Let's create a **utility function** that safely extracts data from nested structures:

```python
def safe_get(data: dict, *keys, default=None):
    """
    Safely get a nested value from a dictionary.

    This function traverses a nested dictionary structure using
    the provided keys, returning a default value if any key
    is missing or if we encounter None.

    Args:
        data: The dictionary to search
        *keys: The keys to traverse (variable number of arguments)
        default: Value to return if path doesn't exist

    Returns:
        The value at the path, or default if not found

    Examples:
        >>> data = {"address": {"city": "Taipei"}}
        >>> safe_get(data, "address", "city")
        'Taipei'
        >>> safe_get(data, "address", "country", default="Unknown")
        'Unknown'
        >>> safe_get(data, "missing", "path")
        None
    """
    current = data  # Start at the root

    # Traverse each key in the path
    for key in keys:
        if isinstance(current, dict):
            # If current is a dict, use .get() to safely access
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int):
            # If current is a list and key is an integer, try index access
            try:
                current = current[key]
            except IndexError:
                return default
        else:
            # current is neither dict nor list (or key type mismatch)
            return default

        # If we hit None at any point, return default
        if current is None:
            return default

    return current
```

### How `safe_get` Works (Step by Step)

Let's trace through an example:

```python
data = {
    "result": {
        "address": {
            "city": "Taipei"
        }
    }
}

# Call: safe_get(data, "result", "address", "city")

# Step 1: current = data (the whole dict)
# Step 2: key = "result"
#         current = data.get("result") = {"address": {"city": "Taipei"}}
# Step 3: key = "address"
#         current = current.get("address") = {"city": "Taipei"}
# Step 4: key = "city"
#         current = current.get("city") = "Taipei"
# Step 5: Return "Taipei"
```

Now with a missing key:

```python
# Call: safe_get(data, "result", "address", "country", default="Unknown")

# Step 1: current = data
# Step 2: key = "result"
#         current = {"address": {"city": "Taipei"}}
# Step 3: key = "address"
#         current = {"city": "Taipei"}
# Step 4: key = "country"
#         current = {"city": "Taipei"}.get("country") = None
# Step 5: current is None, so return default = "Unknown"
```

### Using `safe_get` in Practice

```python
# Raw Nominatim response
result = {
    "lat": "25.0339",
    "lon": "121.5645",
    "display_name": "Taipei 101, Taipei, Taiwan",
    "address": {
        "tourism": "台北101",
        "city": "Taipei"
    }
}

# Safe data extraction
name = safe_get(result, "name", default=safe_get(result, "display_name", default="Unknown"))
city = safe_get(result, "address", "city", default="Unknown")
country = safe_get(result, "address", "country", default="Unknown")
postcode = safe_get(result, "address", "postcode", default="N/A")

print(f"Name: {name}")       # "Taipei 101, Taipei, Taiwan" (fell back to display_name)
print(f"City: {city}")       # "Taipei"
print(f"Country: {country}") # "Unknown"
print(f"Postcode: {postcode}") # "N/A"
```

---

## 2.4 Parsing Nominatim Results Robustly

Now let's build a complete, robust parser for Nominatim results:

```python
from typing import TypedDict

class GeocodedPlace(TypedDict):
    """
    Type definition for a geocoded place.

    TypedDict provides documentation and IDE hints about
    what fields our parsed result will have.
    """
    name: str
    lat: float
    lon: float
    display_name: str
    place_type: str
    importance: float
    address: dict


def parse_nominatim_result(result: dict) -> GeocodedPlace:
    """
    Parse a single Nominatim result into a clean, consistent structure.

    This function handles:
    - Missing fields (uses sensible defaults)
    - Type conversion (lat/lon strings to floats)
    - Data normalization (consistent field names)

    Args:
        result: Raw result dictionary from Nominatim API

    Returns:
        Cleaned GeocodedPlace dictionary with consistent structure
    """
    # Handle coordinates - they come as strings!
    # Use try/except to handle malformed data
    try:
        lat = float(result.get("lat", 0))
        lon = float(result.get("lon", 0))
    except (ValueError, TypeError):
        # float() failed - use default coordinates
        lat, lon = 0.0, 0.0

    # Handle importance score
    try:
        importance = float(result.get("importance", 0))
    except (ValueError, TypeError):
        importance = 0.0

    # Build the clean result dictionary
    return {
        # Name: prefer "name" field, fall back to display_name
        "name": result.get("name", result.get("display_name", "Unknown")),

        # Coordinates (now as floats)
        "lat": lat,
        "lon": lon,

        # Full address string
        "display_name": result.get("display_name", ""),

        # Classification - combine class and type
        "place_type": f"{result.get('class', '')}:{result.get('type', '')}",

        # Ranking
        "importance": importance,

        # Raw address object for further processing
        "address": result.get("address", {})
    }


def parse_nominatim_response(response_data: list) -> list[GeocodedPlace]:
    """
    Parse a complete Nominatim response (list of results).

    Args:
        response_data: List of results from Nominatim API

    Returns:
        List of cleaned GeocodedPlace dictionaries
    """
    # Handle empty response
    if not response_data:
        return []

    # Parse each result
    return [parse_nominatim_result(r) for r in response_data]
```

### Why This Design?

1. **Separation of concerns**: One function for single results, one for the list
2. **Defensive**: Every field access has a fallback
3. **Type conversion**: Strings become proper floats
4. **Consistent output**: Same fields regardless of input variations
5. **Documented**: TypedDict shows exactly what we return

---

## 2.5 Mini-Exercise 2: Handle Missing Data

Write a function that formats an address from a Nominatim result, handling all possible missing fields:

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
        "Unknown location"  (nothing available)
    """
    # Your code here
    pass
```

**Test cases to handle:**

```python
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
    },
    # No address field at all
    {}
]
```

<details>
<summary>Solution</summary>

```python
def format_address(result: dict) -> str:
    """
    Format an address from Nominatim result.
    Handles missing fields gracefully.
    """
    # Step 1: Get the address object (empty dict if missing)
    address = result.get("address", {})

    # Step 2: Build the street part
    street_parts = []
    if address.get("house_number"):
        street_parts.append(address["house_number"])
    if address.get("road"):
        street_parts.append(address["road"])
    street = " ".join(street_parts)  # Combine with space

    # Step 3: Collect all address parts
    parts = []

    # Add street if we have it
    if street:
        parts.append(street)

    # District - try multiple possible keys
    # (Nominatim uses different keys in different regions)
    district = (address.get("suburb") or
                address.get("district") or
                address.get("neighbourhood") or
                address.get("quarter"))
    if district:
        parts.append(district)

    # City - also has multiple possible keys
    city = (address.get("city") or
            address.get("town") or
            address.get("village") or
            address.get("municipality") or
            address.get("county"))
    if city:
        parts.append(city)

    # State/Province (common in US, Australia)
    state = address.get("state")
    if state:
        parts.append(state)

    # Country (almost always present)
    if address.get("country"):
        parts.append(address["country"])

    # Step 4: Join parts or return default
    if parts:
        return ", ".join(parts)
    else:
        return "Unknown location"


# Test
for i, case in enumerate(test_cases):
    print(f"Case {i + 1}: {format_address(case)}")

# Output:
# Case 1: 7 Section 5 Xinyi Road, Xinyi District, Taipei, Taiwan
# Case 2: Shibuya, Tokyo, Japan
# Case 3: Taiwan
# Case 4: Unknown location
# Case 5: Unknown location
```

**Key techniques used:**
1. `result.get("address", {})` - Safe access with empty dict default
2. `address.get("key")` - Returns None if missing
3. `or` chaining - Try multiple keys, use first non-empty
4. Build list then join - Easier than string concatenation

</details>

---

## 2.6 Working with Bounding Boxes

Nominatim returns bounding boxes as a list of strings:

```json
"boundingbox": ["25.0329", "25.0349", "121.5634", "121.5654"]
```

Format: `[south, north, west, east]`

This represents the rectangular area that contains the place:

```
                 North (25.0349)
                    ────────
                    │      │
      West          │      │         East
    (121.5634)      │      │      (121.5654)
                    │      │
                    ────────
                 South (25.0329)
```

### Why Bounding Boxes Matter

1. **Zoom level**: Larger box = zoom out more on the map
2. **Area calculations**: Estimate the size of a place
3. **Containment checks**: Is a point inside this area?

### Parsing Bounding Boxes

```python
def parse_bounding_box(bbox: list) -> dict | None:
    """
    Parse a Nominatim bounding box.

    Args:
        bbox: List of [south, north, west, east] as strings

    Returns:
        Dictionary with float coordinates, or None if invalid
    """
    # Validate input
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
    """
    Estimate the area of a bounding box in km².

    Note: This is an approximation. At the equator, 1 degree ≈ 111 km.
    As you move toward the poles, longitude degrees get smaller.
    """
    import math

    lat_diff = bbox["north"] - bbox["south"]
    lon_diff = bbox["east"] - bbox["west"]

    # 1 degree latitude ≈ 111 km everywhere
    lat_km = lat_diff * 111

    # 1 degree longitude ≈ 111 * cos(latitude) km
    mid_lat = (bbox["north"] + bbox["south"]) / 2
    lon_km = lon_diff * 111 * math.cos(math.radians(mid_lat))

    return lat_km * lon_km


# Example usage
result = {
    "boundingbox": ["25.0329", "25.0349", "121.5634", "121.5654"]
}

bbox = parse_bounding_box(result["boundingbox"])
if bbox:
    center = bbox_center(bbox)
    area = bbox_area_km2(bbox)
    print(f"Center: {center}")
    print(f"Area: {area:.4f} km²")
```

---

# ☕ 10-Minute Break

Stretch, grab water, check your phone!

---

# Hour 3: Error Handling and Building a CLI Tool

## 3.1 Why Error Handling Matters

In the previous hour, we learned to handle **missing data**. Now we'll handle **runtime errors** - things that go wrong when our code executes:

- Network connection fails
- API returns an error
- User enters invalid input
- File doesn't exist
- Server is overloaded

**Without error handling**: Your program crashes and the user sees a scary traceback.

**With error handling**: Your program recovers gracefully and shows a helpful message.

---

## 3.2 Python Error Handling Fundamentals

### The `try/except` Statement

```python
try:
    # Code that might fail
    result = risky_operation()
except SomeError:
    # Code to handle the error
    print("Something went wrong")
```

**How it works:**
1. Python tries to execute the code in the `try` block
2. If an error occurs, Python stops and looks for a matching `except` block
3. If found, it executes that block instead of crashing
4. If not found, the program crashes as usual

### Simple Example

```python
# Without error handling - crashes on invalid input
number = int(input("Enter a number: "))  # If user types "abc" -> ValueError

# With error handling - gracefully handles invalid input
try:
    number = int(input("Enter a number: "))
    print(f"You entered: {number}")
except ValueError:
    print("That's not a valid number!")
```

### Catching Multiple Exceptions

You can handle different errors differently:

```python
try:
    data = response.json()
    value = data["key"]

except json.JSONDecodeError:
    # The response wasn't valid JSON
    print("Invalid JSON response")

except KeyError:
    # The JSON was valid but missing our key
    print("Key not found in response")

except Exception as e:
    # Catch-all for any other error
    print(f"Unexpected error: {e}")
```

**Order matters!** Python checks `except` blocks top to bottom.

### The Exception Hierarchy

Python exceptions form a hierarchy. More specific exceptions inherit from general ones:

```
Exception (base class)
├── ValueError (invalid value)
├── TypeError (wrong type)
├── KeyError (missing dict key)
├── IndexError (list index out of range)
├── requests.exceptions.RequestException (base for requests errors)
│   ├── requests.exceptions.Timeout
│   ├── requests.exceptions.ConnectionError
│   └── requests.exceptions.HTTPError
└── ... many more
```

**Best practice**: Catch specific exceptions, not just `Exception`.

```python
# BAD - catches everything, hides bugs
try:
    something()
except Exception:
    pass  # Silently ignore all errors

# GOOD - catches only what we expect
try:
    something()
except ValueError:
    handle_value_error()
except KeyError:
    handle_missing_key()
```

### The Full `try/except/else/finally` Structure

```python
try:
    # Code that might fail
    file = open("data.json")
    data = json.load(file)

except FileNotFoundError:
    # Handle missing file
    print("File not found")
    data = {}

except json.JSONDecodeError:
    # Handle invalid JSON
    print("Invalid JSON in file")
    data = {}

else:
    # Only runs if NO exception occurred
    # Good place for code that depends on success
    print(f"Successfully loaded {len(data)} items")

finally:
    # ALWAYS runs, even if there was an exception
    # Good place for cleanup (closing files, connections)
    if 'file' in locals():
        file.close()
        print("File closed")
```

**When to use each block:**

| Block | When it runs | Use for |
|-------|--------------|---------|
| `try` | Always attempted | Code that might fail |
| `except` | Only on matching error | Error handling |
| `else` | Only if no error | Success-dependent code |
| `finally` | Always, after try/except | Cleanup (close files, etc.) |

---

## 3.3 Common API-Related Exceptions

### Network Exceptions (from `requests`)

```python
import requests

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError for 4xx/5xx

except requests.exceptions.Timeout:
    # The server took too long to respond
    print("Request timed out - server might be slow")

except requests.exceptions.ConnectionError:
    # Couldn't connect at all (no internet, wrong URL, etc.)
    print("Connection failed - check your internet")

except requests.exceptions.HTTPError as e:
    # Server returned an error status (4xx or 5xx)
    print(f"HTTP error: {e.response.status_code}")
    if e.response.status_code == 403:
        print("Forbidden - check your User-Agent header")
    elif e.response.status_code == 429:
        print("Rate limited - slow down!")

except requests.exceptions.RequestException as e:
    # Base class catches all requests errors
    print(f"Request failed: {e}")
```

### Data Parsing Exceptions

```python
try:
    # Parse the JSON response
    data = response.json()

    # Access nested data
    result = data[0]
    lat = float(result["lat"])
    name = result["address"]["city"]

except json.JSONDecodeError:
    # Response body wasn't valid JSON
    print("Server returned invalid JSON")

except IndexError:
    # Tried to access data[0] but list was empty
    print("No results found")

except KeyError as e:
    # Dictionary was missing a key
    print(f"Response missing expected field: {e}")

except TypeError:
    # Tried to access something that was None
    # e.g., result["address"] returned None, then ["city"] fails
    print("Unexpected data structure")

except ValueError:
    # float() conversion failed
    # e.g., float("not a number")
    print("Invalid coordinate format")
```

---

## 3.4 Designing Custom Exception Classes

For larger applications, create custom exceptions that describe your domain:

```python
class GeocodingError(Exception):
    """
    Base exception for all geocoding-related errors.

    By creating a hierarchy of exceptions, calling code can:
    - Catch all geocoding errors with `except GeocodingError`
    - Catch specific errors with `except NotFoundError`
    """
    pass


class NetworkError(GeocodingError):
    """
    Raised when a network request fails.

    Examples:
    - Connection timeout
    - DNS resolution failure
    - Server returned 5xx error
    """
    pass


class RateLimitError(GeocodingError):
    """
    Raised when we've made too many requests.

    Nominatim allows 1 request per second.
    If exceeded, server returns 429 status.
    """
    pass


class NotFoundError(GeocodingError):
    """
    Raised when the place cannot be found.

    The API worked but returned no results.
    """
    pass


class ParseError(GeocodingError):
    """
    Raised when we can't parse the API response.

    The response structure was unexpected.
    """
    pass
```

### Using Custom Exceptions

```python
def geocode(query: str) -> dict:
    """
    Geocode a place name to coordinates.

    Args:
        query: Place name to search for

    Returns:
        Dictionary with name, lat, lon

    Raises:
        NetworkError: If the API request fails
        RateLimitError: If rate limit exceeded
        NotFoundError: If place not found
        ParseError: If response can't be parsed
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

    try:
        # Make the request
        response = requests.get(url, params=params, headers=headers, timeout=10)

        # Check for rate limiting (429 status)
        if response.status_code == 429:
            raise RateLimitError("Too many requests. Please wait.")

        # Check for other HTTP errors
        if response.status_code != 200:
            raise NetworkError(f"HTTP {response.status_code}")

        # Parse response
        data = response.json()

        # Check for empty results
        if not data:
            raise NotFoundError(f"No results for: {query}")

        # Extract and return data
        result = data[0]
        return {
            "name": result.get("name", query),
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result.get("display_name", "")
        }

    except requests.exceptions.Timeout:
        raise NetworkError("Request timed out")

    except requests.exceptions.ConnectionError:
        raise NetworkError("Connection failed")

    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Request failed: {e}")

    except (KeyError, IndexError, ValueError) as e:
        raise ParseError(f"Failed to parse response: {e}")


# Using the function with error handling
try:
    result = geocode("Taipei 101")
    print(f"Found: {result['name']} at ({result['lat']}, {result['lon']})")

except NotFoundError:
    print("Place not found. Try a different search term.")

except RateLimitError:
    print("Too many requests. Wait a moment and try again.")

except NetworkError as e:
    print(f"Network problem: {e}")

except GeocodingError as e:
    # Catch-all for any geocoding error we didn't specifically handle
    print(f"Geocoding failed: {e}")
```

### Benefits of Custom Exceptions

1. **Clarity**: `NotFoundError` is clearer than `ValueError`
2. **Hierarchy**: Can catch all geocoding errors or specific ones
3. **Documentation**: Docstrings explain when each is raised
4. **Separation**: Network errors vs data errors vs business logic errors

---

## 3.5 Mini-Exercise 3: Error Handling Practice

Add proper error handling to this function:

```python
import requests

def get_coordinates(place_name: str) -> tuple[float, float]:
    """
    Get coordinates for a place name.

    Should handle:
    - Network errors (timeout, connection failure)
    - Empty results
    - Missing or invalid lat/lon

    Returns:
        Tuple of (latitude, longitude)

    Raises:
        ValueError: If place not found or data invalid
        ConnectionError: If network request fails
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    # Currently has no error handling!
    response = requests.get(url, params=params, headers=headers, timeout=10)
    data = response.json()
    result = data[0]
    lat = float(result["lat"])
    lon = float(result["lon"])
    return (lat, lon)
```

**Errors to handle:**
1. Network timeout
2. Connection failure
3. HTTP error status
4. Empty results (no places found)
5. Missing lat/lon fields
6. Invalid lat/lon values (can't convert to float)

<details>
<summary>Solution</summary>

```python
import requests

def get_coordinates(place_name: str) -> tuple[float, float]:
    """
    Get coordinates for a place name with robust error handling.
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (test@example.com)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    try:
        # Make the request with timeout
        response = requests.get(
            url, params=params, headers=headers, timeout=10
        )

        # Check HTTP status code
        if response.status_code != 200:
            raise ConnectionError(f"HTTP error: {response.status_code}")

        # Parse JSON response
        data = response.json()

        # Check for empty results
        if not data:
            raise ValueError(f"No results found for: {place_name}")

        # Get first result
        result = data[0]

        # Check that lat/lon exist
        if "lat" not in result or "lon" not in result:
            raise ValueError("Response missing coordinates")

        # Convert to floats (might fail if values are malformed)
        lat = float(result["lat"])
        lon = float(result["lon"])

        return (lat, lon)

    except requests.exceptions.Timeout:
        # Server didn't respond in time
        raise ConnectionError("Request timed out")

    except requests.exceptions.ConnectionError:
        # Couldn't establish connection
        raise ConnectionError("Network connection failed")

    except requests.exceptions.RequestException as e:
        # Any other requests error
        raise ConnectionError(f"Request failed: {e}")

    except json.JSONDecodeError:
        # Response wasn't valid JSON
        raise ValueError("Server returned invalid response")

    except (KeyError, IndexError) as e:
        # Data structure wasn't as expected
        raise ValueError(f"Unexpected response format: {e}")


# Test the function
import time

test_queries = [
    "Taipei 101",              # Should work
    "xyzzy12345notaplace",     # Should raise ValueError (not found)
]

for query in test_queries:
    print(f"\nSearching for: {query}")
    try:
        coords = get_coordinates(query)
        print(f"  Found: {coords}")
    except ValueError as e:
        print(f"  Not found: {e}")
    except ConnectionError as e:
        print(f"  Network error: {e}")

    time.sleep(1)  # Rate limiting
```

</details>

---

## 3.6 Building the Complete CLI Geocoder

Now let's put everything together into a complete, production-quality CLI tool:

```python
#!/usr/bin/env python3
"""
Geocoder CLI - Convert place names to coordinates.

A complete command-line geocoding tool demonstrating:
- API integration with Nominatim
- Robust error handling
- Response caching
- Interactive and batch modes

Usage:
    python geocoder_cli.py                    # Interactive mode
    python geocoder_cli.py "Taipei 101"       # Quick geocode
    python geocoder_cli.py --reverse 25.03 121.56  # Reverse geocode
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
    """Network-related errors (timeout, connection, HTTP errors)."""
    pass


class NotFoundError(GeocoderError):
    """Place not found in the database."""
    pass


# =============================================================================
# Cache Functions
# =============================================================================
# Caching avoids repeated API calls for the same query.
# This is polite (reduces server load) and fast (instant results).

def load_cache() -> dict:
    """
    Load the cache from disk.

    Returns empty dict if file doesn't exist or is corrupted.
    """
    cache_path = Path(CONFIG["cache_file"])
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(cache: dict):
    """
    Save the cache to disk.

    Silently fails if write fails (cache is not critical).
    """
    cache_path = Path(CONFIG["cache_file"])
    try:
        cache_path.write_text(json.dumps(cache, indent=2))
    except IOError:
        pass  # Cache save failure is not critical


def get_cached(query: str) -> dict | None:
    """Get a cached result for a query (case-insensitive)."""
    cache = load_cache()
    return cache.get(query.lower())


def set_cached(query: str, result: dict):
    """Cache a result (case-insensitive key)."""
    cache = load_cache()
    cache[query.lower()] = result
    save_cache(cache)


# =============================================================================
# Geocoding Functions
# =============================================================================

def geocode(query: str, use_cache: bool = True) -> dict:
    """
    Convert a place name to coordinates.

    This is the main geocoding function. It:
    1. Checks the cache first (if enabled)
    2. Makes an API request to Nominatim
    3. Parses and validates the response
    4. Caches the result (if enabled)

    Args:
        query: Place name to search for
        use_cache: Whether to check/update cache

    Returns:
        Dictionary with:
        - name: Short name of the place
        - lat: Latitude (float)
        - lon: Longitude (float)
        - display_name: Full formatted address
        - type: Place classification
        - cached: Whether result came from cache

    Raises:
        NotFoundError: If no results found
        NetworkError: If API request fails
        GeocoderError: If response can't be parsed
    """
    # Step 1: Check cache
    if use_cache:
        cached = get_cached(query)
        if cached:
            cached["cached"] = True
            return cached

    # Step 2: Build and make API request
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

        # Step 3: Handle HTTP errors
        if response.status_code == 429:
            raise NetworkError("Rate limit exceeded. Wait and try again.")

        if response.status_code != 200:
            raise NetworkError(f"HTTP {response.status_code}")

        # Step 4: Parse response
        data = response.json()

        if not data:
            raise NotFoundError(f"No results for: {query}")

        # Step 5: Extract and validate data
        result = data[0]
        parsed = {
            "name": result.get("name", query),
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "display_name": result.get("display_name", ""),
            "type": f"{result.get('class', '')}:{result.get('type', '')}",
            "cached": False
        }

        # Step 6: Cache the result
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
        Dictionary with:
        - display_name: Full formatted address
        - address: Structured address components
        - lat, lon: The input coordinates

    Raises:
        NotFoundError: If location not in database
        NetworkError: If API request fails
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
# Display Functions
# =============================================================================

def print_result(result: dict):
    """Pretty print a forward geocoding result."""
    print()
    print(f"  Name: {result.get('name', 'N/A')}")
    print(f"  Coordinates: ({result['lat']:.6f}, {result['lon']:.6f})")
    print(f"  Full address: {result.get('display_name', 'N/A')}")
    if result.get("type") and result["type"] != ":":
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
        for key, value in list(address.items())[:10]:  # Limit to 10 items
            print(f"    {key}: {value}")
    print()


# =============================================================================
# CLI Interface
# =============================================================================

def interactive_mode():
    """
    Run the geocoder in interactive mode.

    Provides a REPL (Read-Eval-Print Loop) for geocoding.
    """
    print("\n" + "="*50)
    print("  Geocoder CLI - Interactive Mode")
    print("="*50)
    print("\nCommands:")
    print("  <place name>          - Search for a place")
    print("  reverse <lat> <lon>   - Reverse geocode")
    print("  quit                  - Exit")
    print()

    last_request = 0  # For rate limiting

    while True:
        # Get user input
        try:
            user_input = input("geocoder> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        # Skip empty input
        if not user_input:
            continue

        # Handle quit command
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Rate limiting: ensure at least 1 second between API calls
        elapsed = time.time() - last_request
        if elapsed < 1 and last_request > 0:
            time.sleep(1 - elapsed)

        # Handle reverse geocoding
        if user_input.lower().startswith("reverse "):
            parts = user_input.split()
            if len(parts) != 3:
                print("Usage: reverse <lat> <lon>")
                print("Example: reverse 25.0339 121.5645")
                continue

            try:
                lat = float(parts[1])
                lon = float(parts[2])
                result = reverse_geocode(lat, lon)
                print_reverse_result(result)
                last_request = time.time()
            except ValueError:
                print("Invalid coordinates. Example: reverse 25.0339 121.5645")
            except GeocoderError as e:
                print(f"Error: {e}")
            continue

        # Handle forward geocoding (default)
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
    """
    Main entry point.

    Handles command-line arguments or starts interactive mode.
    """
    if len(sys.argv) > 1:
        # Command-line mode
        if sys.argv[1] == "--reverse" and len(sys.argv) == 4:
            # Reverse geocoding
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
        elif sys.argv[1] in ("--help", "-h"):
            print(__doc__)
        else:
            # Forward geocoding
            query = " ".join(sys.argv[1:])
            try:
                result = geocode(query)
                print_result(result)
            except GeocoderError as e:
                print(f"Error: {e}")
                sys.exit(1)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
```

---

## 3.7 Best Practices Summary

### Error Handling Best Practices

| Practice | Why | Example |
|----------|-----|---------|
| **Be Specific** | Different errors need different handling | `except ValueError` not `except Exception` |
| **Fail Fast** | Catch errors early | Validate inputs at function start |
| **Provide Context** | Help debugging | `raise ValueError(f"Invalid lat: {lat}")` |
| **Don't Silence Errors** | Hidden errors cause bugs | Log errors, don't just `pass` |
| **Use Custom Exceptions** | Clear, domain-specific | `NotFoundError`, `RateLimitError` |

### API Integration Best Practices

| Practice | Why | Implementation |
|----------|-----|----------------|
| **Set Timeouts** | Don't hang forever | `timeout=10` |
| **Respect Rate Limits** | Avoid getting banned | `time.sleep(1)` between requests |
| **Cache Results** | Reduce load, speed up | File or memory cache |
| **Validate Responses** | Don't trust API blindly | Check status codes and data |
| **Handle All Errors** | Graceful degradation | Network, parsing, and logic errors |

### Data Parsing Best Practices

| Practice | Why | Example |
|----------|-----|---------|
| **Use `.get()`** | Avoid KeyError | `result.get("key", default)` |
| **Convert Types** | APIs return strings | `float(result["lat"])` |
| **Validate Data** | Catch bad data early | Check for required fields |
| **Handle Missing** | Data is incomplete | Fallback values |

---

## 3.8 Homework Assignments

### Assignment 1: Batch Geocoder (Basic)
Create a script that:
1. Reads place names from a text file (one per line)
2. Geocodes each place with rate limiting
3. Writes results to a JSON file
4. Handles errors gracefully (skip failed places, don't crash)
5. Reports summary at the end (X succeeded, Y failed)

### Assignment 2: Address Formatter (Intermediate)
Create a function that formats addresses according to country conventions:
- Taiwan: "District, City, Country"
- USA: "Street, City, State ZIP"
- Japan: "Prefecture City District"

The function should detect the country and format accordingly.

### Assignment 3: Geocoder with Retry (Advanced)
Enhance the geocoder to:
1. Retry failed requests up to 3 times with exponential backoff
2. Try alternative queries if exact match fails:
   - Remove punctuation
   - Try just the first 3 words
3. Cache both successes and failures (to avoid retrying known failures)

---

## Additional Resources

### Documentation
- [Nominatim API Documentation](https://nominatim.org/release-docs/latest/api/Overview/)
- [OpenStreetMap Wiki - Nominatim](https://wiki.openstreetmap.org/wiki/Nominatim)
- [Python Requests - Error Handling](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)

### Alternative Geocoding Services
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding) (paid)
- [Mapbox Geocoding](https://docs.mapbox.com/api/search/geocoding/) (freemium)
- [HERE Geocoding](https://developer.here.com/documentation/geocoding-search-api/) (freemium)
- [Geopy](https://geopy.readthedocs.io/) (Python library supporting multiple services)

### Practice Resources
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Practice parsing nested JSON
- [httpbin.org](https://httpbin.org/) - Test error handling with fake errors

---

## Next Week Preview

**Week 6: Searching for Places (Lazy Loading)**
- Query parameters and pagination
- Python generators and the `yield` keyword
- Lazy evaluation for memory efficiency
- Building a paginated search interface

---

*End of Week 5 Lecture*
