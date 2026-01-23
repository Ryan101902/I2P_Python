# Week 4: HTTP Requests & API Keys

## Lecture Overview (3 Hours)

**Phase 2: The API & The Cloud** — "Fetching the World"

### Learning Objectives
By the end of this lecture, students will be able to:
1. Understand the HTTP request/response cycle
2. Use Python's `requests` library to fetch data from the web
3. Interpret HTTP status codes and handle errors appropriately
4. Configure proper headers (User-Agent) for API requests
5. Make successful calls to the Nominatim geocoding API
6. Implement rate limiting and API etiquette

### Prerequisites
- Week 3: JSON and File I/O
- Understanding of dictionaries and JSON parsing
- Python environment with `requests` installed

---

# Hour 1: Understanding HTTP and the Web

## 1.1 How the Internet Works (Simplified)

When you type a URL in your browser or make an API call in Python, you're participating in a **conversation** between two computers:

```
┌─────────────┐         Request          ┌─────────────┐
│             │ ───────────────────────> │             │
│   Client    │                          │   Server    │
│  (Your PC)  │ <─────────────────────── │  (Website)  │
│             │         Response         │             │
└─────────────┘                          └─────────────┘
```

### The Client-Server Model

- **Client**: The computer making the request (your laptop, phone, or Python script)
- **Server**: The computer that has the data you want (e.g., OpenStreetMap servers)

Think of it like ordering food at a restaurant:
1. You (client) look at the menu and place an order (request)
2. The kitchen (server) prepares your food
3. The waiter brings your food back (response)

---

## 1.2 What is HTTP?

**HTTP** = **H**yper**T**ext **T**ransfer **P**rotocol

It's the "language" that clients and servers use to communicate. Just like humans have rules for conversation (greetings, questions, answers), computers have HTTP.

### HTTP Methods (Verbs)

| Method | Purpose | Restaurant Analogy |
|--------|---------|-------------------|
| **GET** | Retrieve data | "Can I see the menu?" |
| **POST** | Send/create data | "I'd like to order this" |
| **PUT** | Update data | "Please change my order" |
| **DELETE** | Remove data | "Cancel my order" |

For this course, we'll primarily use **GET** — fetching location data from APIs.

---

## 1.3 Anatomy of a URL

Let's break down a Nominatim API URL:

```
https://nominatim.openstreetmap.org/search?q=Taipei+101&format=json
└─┬─┘  └───────────┬───────────────┘└──┬──┘└──────────┬───────────┘
  │                │                   │              │
Protocol        Host/Domain         Path      Query Parameters
```

### Components:

| Component | Example | Purpose |
|-----------|---------|---------|
| Protocol | `https://` | Secure connection |
| Host | `nominatim.openstreetmap.org` | Server address |
| Path | `/search` | Specific endpoint/action |
| Query Params | `?q=Taipei+101&format=json` | Options for the request |

### Query Parameters Explained

Query parameters are like filling out a form:
- Start with `?`
- Key-value pairs: `key=value`
- Multiple params joined with `&`

```
?q=Taipei+101&format=json&limit=5
 │            │           │
 │            │           └── limit: only 5 results
 │            └── format: return JSON (not HTML)
 └── q (query): what we're searching for
```

---

## 1.4 HTTP Headers

Headers are **metadata** about the request or response. Think of them as the "envelope" around your letter:

```
┌────────────────────────────────────┐
│ Headers (the envelope)             │
│ ┌────────────────────────────────┐ │
│ │ Body (the letter content)      │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

### Common Request Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `User-Agent` | Identifies the client | `"MyApp/1.0 (email@example.com)"` |
| `Accept` | Preferred response format | `"application/json"` |
| `Authorization` | API key or token | `"Bearer abc123"` |
| `Content-Type` | Format of sent data | `"application/json"` |

### Common Response Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Format of response | `"application/json"` |
| `Content-Length` | Size of response | `"1234"` |
| `X-RateLimit-Remaining` | API calls left | `"95"` |

---

## 1.5 HTTP Status Codes

When a server responds, it includes a **status code** — a 3-digit number indicating what happened:

### Status Code Categories

| Range | Category | Meaning |
|-------|----------|---------|
| 1xx | Informational | Request received, continuing |
| 2xx | Success | Request completed successfully |
| 3xx | Redirection | Go somewhere else |
| 4xx | Client Error | Your fault |
| 5xx | Server Error | Server's fault |

### Essential Status Codes for API Work

```python
# Success Codes (2xx)
200  # OK - Everything worked!
201  # Created - New resource created (POST success)
204  # No Content - Success, but nothing to return

# Redirection (3xx)
301  # Moved Permanently - URL changed forever
302  # Found - Temporary redirect

# Client Errors (4xx)
400  # Bad Request - Malformed request
401  # Unauthorized - Need to authenticate
403  # Forbidden - Not allowed (often missing User-Agent)
404  # Not Found - Resource doesn't exist
429  # Too Many Requests - Rate limit exceeded!

# Server Errors (5xx)
500  # Internal Server Error - Server crashed
502  # Bad Gateway - Server communication issue
503  # Service Unavailable - Server overloaded/maintenance
```

### The Most Important Ones for This Course

```
200 → ✓ Success! Parse the response
403 → ✗ Missing User-Agent header
404 → ✗ Wrong URL or endpoint
429 → ⚠ Slow down! You're making too many requests
```

---

## 1.6 Mini-Exercise 1: Identify the Parts

Look at this URL and identify each component:

```
https://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid=abc123&units=metric
```

**Questions:**
1. What is the protocol?
2. What is the host?
3. What is the path?
4. What query parameters are being passed?

<details>
<summary>Solution</summary>

1. Protocol: `https://`
2. Host: `api.openweathermap.org`
3. Path: `/data/2.5/weather`
4. Query Parameters:
   - `q=Tokyo` (city name)
   - `appid=abc123` (API key)
   - `units=metric` (temperature in Celsius)

</details>

---

# ☕ 5-Minute Break

Stand up, stretch, rest your eyes!

---

# Hour 2: The `requests` Library

## 2.1 Installing and Importing `requests`

The `requests` library makes HTTP calls simple and "Pythonic":

```bash
# In terminal (already done in SETUP.md)
pip install requests
```

```python
# In Python
import requests
```

### Why `requests` Instead of Built-in `urllib`?

Python has a built-in `urllib` module, but `requests` is much easier to use:

```python
# Using urllib (complicated)
import urllib.request
import urllib.parse
import json

url = "https://api.example.com/data"
params = urllib.parse.urlencode({"q": "test"})
req = urllib.request.Request(f"{url}?{params}")
req.add_header("User-Agent", "MyApp/1.0")
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

# Using requests (simple!)
import requests

response = requests.get(
    "https://api.example.com/data",
    params={"q": "test"},
    headers={"User-Agent": "MyApp/1.0"}
)
data = response.json()
```

---

## 2.2 Making Your First Request

Let's start with a simple GET request:

```python
import requests

# Make a GET request
response = requests.get("https://httpbin.org/get")

# What did we get back?
print(f"Status Code: {response.status_code}")
print(f"Content Type: {response.headers['Content-Type']}")
print(f"Response Body: {response.text[:200]}...")
```

Output:
```
Status Code: 200
Content Type: application/json
Response Body: {
  "args": {},
  "headers": {
    "Accept": "*/*",
    ...
```

### The Response Object

When you call `requests.get()`, you get a `Response` object with many useful attributes:

```python
response = requests.get("https://httpbin.org/get")

# Status information
response.status_code      # 200
response.ok               # True (status < 400)
response.reason           # "OK"

# Response content
response.text             # Raw text content (string)
response.content          # Raw bytes content
response.json()           # Parse JSON (returns dict/list)

# Headers
response.headers          # Response headers (dict-like)

# Request information
response.url              # Final URL (after redirects)
response.elapsed          # How long the request took
```

---

## 2.3 Adding Query Parameters

Instead of building URLs manually, let `requests` handle it:

```python
import requests

# DON'T do this (manual URL building)
url = "https://nominatim.openstreetmap.org/search?q=Taipei+101&format=json"

# DO this (use params argument)
url = "https://nominatim.openstreetmap.org/search"
params = {
    "q": "Taipei 101",      # requests handles URL encoding
    "format": "json",
    "limit": 5
}

response = requests.get(url, params=params)
print(response.url)  # Shows the constructed URL
```

### Why Use `params`?

1. **Automatic URL encoding**: Spaces become `%20` or `+`
2. **Cleaner code**: Easy to read and modify
3. **No mistakes**: No forgetting `?` or `&`

```python
# These special characters get encoded automatically
params = {
    "q": "café & restaurant",  # Becomes: caf%C3%A9+%26+restaurant
    "city": "New York"         # Becomes: New+York
}
```

---

## 2.4 Adding Headers

Headers are passed as a dictionary:

```python
import requests

headers = {
    "User-Agent": "CS101-Navigator/1.0 (student@university.edu)",
    "Accept": "application/json"
}

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "National Taiwan University", "format": "json"},
    headers=headers
)

print(response.status_code)  # 200 with proper headers
```

### The User-Agent Header

This is **critical** for OpenStreetMap APIs!

```python
# ❌ BAD - Will get blocked (403 Forbidden)
response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "Taipei", "format": "json"}
)
# Response: 403 Forbidden

# ✓ GOOD - Proper identification
headers = {
    "User-Agent": "MyProjectName/1.0 (myemail@example.com)"
}
response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "Taipei", "format": "json"},
    headers=headers
)
# Response: 200 OK
```

### User-Agent Best Practices

```python
# Format: AppName/Version (Contact Email)
headers = {
    "User-Agent": "SmartCityNavigator/1.0 (cs101@university.edu)"
}

# Include:
# - Your project/app name
# - Version number
# - Contact email (so OSM can reach you if there's an issue)
```

---

## 2.5 Mini-Exercise 2: Your First API Call

Write a script that:
1. Makes a request to `https://httpbin.org/headers`
2. Includes a custom User-Agent header
3. Prints the status code and response

```python
import requests

# Your code here:
# 1. Define headers with User-Agent
# 2. Make the GET request
# 3. Print the results
```

<details>
<summary>Solution</summary>

```python
import requests

# Define headers
headers = {
    "User-Agent": "CS101-Test/1.0 (student@example.com)"
}

# Make the request
response = requests.get(
    "https://httpbin.org/headers",
    headers=headers
)

# Print results
print(f"Status Code: {response.status_code}")
print(f"Response:")
print(response.json())
```

Output:
```
Status Code: 200
Response:
{'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'CS101-Test/1.0 (student@example.com)'}}
```

</details>

---

## 2.6 Handling JSON Responses

Most APIs return JSON. The `requests` library makes parsing easy:

```python
import requests

headers = {"User-Agent": "CS101/1.0 (test@example.com)"}

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "Taipei 101", "format": "json"},
    headers=headers
)

# Check if successful
if response.status_code == 200:
    # Parse JSON response
    places = response.json()  # Returns a list of dicts

    if places:
        first_result = places[0]
        print(f"Name: {first_result['display_name']}")
        print(f"Latitude: {first_result['lat']}")
        print(f"Longitude: {first_result['lon']}")
    else:
        print("No results found")
else:
    print(f"Error: {response.status_code}")
```

### Structure of Nominatim Response

```json
[
    {
        "place_id": 12345,
        "lat": "25.0339639",
        "lon": "121.5644722",
        "display_name": "Taipei 101, 7, Section 5, Xinyi Road, Taipei, Taiwan",
        "type": "attraction",
        "importance": 0.7
    },
    ...
]
```

---

## 2.7 Timeouts and Connection Issues

Networks are unreliable. Always set a timeout:

```python
import requests

try:
    # Timeout after 10 seconds
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": "Taipei", "format": "json"},
        headers={"User-Agent": "CS101/1.0 (test@example.com)"},
        timeout=10  # seconds
    )
    print(response.json())

except requests.exceptions.Timeout:
    print("Request timed out! Server might be slow.")

except requests.exceptions.ConnectionError:
    print("Connection failed! Check your internet.")

except requests.exceptions.RequestException as e:
    print(f"Something went wrong: {e}")
```

### Common Exceptions

| Exception | Cause |
|-----------|-------|
| `Timeout` | Server didn't respond in time |
| `ConnectionError` | Network/DNS issues |
| `HTTPError` | 4xx or 5xx status code |
| `TooManyRedirects` | Too many redirects |
| `RequestException` | Base class for all exceptions |

---

# ☕ 10-Minute Break

Stretch, grab water, check your phone!

---

# Hour 3: Working with the Nominatim API

## 3.1 What is Nominatim?

**Nominatim** is OpenStreetMap's geocoding service:
- **Geocoding**: Convert addresses/place names → coordinates
- **Reverse Geocoding**: Convert coordinates → addresses

```
"Taipei 101" → (25.0339, 121.5644)  # Geocoding
(25.0339, 121.5644) → "Taipei 101, Xinyi District..."  # Reverse
```

### Why Use Nominatim?

1. **Free**: No cost for reasonable usage
2. **Open Data**: Based on OpenStreetMap
3. **No API Key Required**: Just needs proper User-Agent
4. **Global Coverage**: Works worldwide

---

## 3.2 Nominatim Usage Policy

OpenStreetMap is a community project. Respect their resources:

### Rules You Must Follow

1. **Maximum 1 request per second** (rate limiting)
2. **Include valid User-Agent** with contact email
3. **Cache results** when possible
4. **No bulk geocoding** (use dedicated services for that)

```python
import time
import requests

# Good practice: wait between requests
for place in places_to_search:
    response = requests.get(...)
    time.sleep(1)  # Wait 1 second before next request
```

### What Happens If You Don't Follow Rules?

```
First violation:  403 Forbidden (temporary block)
Repeated abuse:   Your IP gets permanently banned
```

---

## 3.3 The Search Endpoint (Geocoding)

Convert place names to coordinates:

```python
import requests
import time

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
        "limit": 1  # Only get the best match
    }

    headers = {
        "User-Agent": "CS101-SmartNavigator/1.0 (cs101@university.edu)"
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


# Usage
result = geocode("National Taiwan University")
if result:
    print(f"Found: {result['name']}")
    print(f"Coordinates: ({result['lat']}, {result['lon']})")
else:
    print("Place not found")

time.sleep(1)  # Respect rate limit before next call
```

---

## 3.4 Search Parameters

Nominatim accepts many useful parameters:

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `q` | Search query | `"Taipei 101"` |
| `format` | Response format | `"json"` or `"jsonv2"` |
| `limit` | Max results | `5` |
| `countrycodes` | Limit to countries | `"tw,jp"` |
| `viewbox` | Limit to bounding box | `"lon1,lat1,lon2,lat2"` |
| `bounded` | Strict viewbox | `1` |
| `addressdetails` | Include address breakdown | `1` |

### Example: Search in Taiwan Only

```python
params = {
    "q": "Main Station",
    "format": "json",
    "countrycodes": "tw",    # Only Taiwan
    "limit": 5,
    "addressdetails": 1      # Get detailed address
}
```

### Example: Search Within Taipei

```python
# Bounding box for Taipei
# Format: left,bottom,right,top (lon1,lat1,lon2,lat2)
params = {
    "q": "coffee shop",
    "format": "json",
    "viewbox": "121.45,24.95,121.65,25.15",  # Taipei area
    "bounded": 1,  # Strict - only within viewbox
    "limit": 10
}
```

---

## 3.5 The Reverse Endpoint (Reverse Geocoding)

Convert coordinates to an address:

```python
import requests

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
        "User-Agent": "CS101-SmartNavigator/1.0 (cs101@university.edu)"
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


# Usage
address = reverse_geocode(25.0339, 121.5645)
print(f"Address: {address}")
# Output: "Taipei 101, 7, Section 5, Xinyi Road, Xinyi District, Taipei, Taiwan"
```

---

## 3.6 Mini-Exercise 3: Build a Geocoder

Create a function that takes a list of place names and returns their coordinates:

```python
import requests
import time

def geocode_places(place_names: list[str]) -> list[dict]:
    """
    Geocode multiple places.

    Args:
        place_names: List of place names to geocode

    Returns:
        List of dicts with name, lat, lon (only successful geocodes)
    """
    # Your code here
    pass


# Test with these places
places = [
    "Taipei 101",
    "National Palace Museum",
    "Jiufen Old Street"
]

results = geocode_places(places)
for place in results:
    print(f"{place['name'][:50]}... -> ({place['lat']:.4f}, {place['lon']:.4f})")
```

<details>
<summary>Solution</summary>

```python
import requests
import time

def geocode_places(place_names: list[str]) -> list[dict]:
    """
    Geocode multiple places with rate limiting.
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "CS101-SmartNavigator/1.0 (cs101@university.edu)"
    }

    results = []

    for i, name in enumerate(place_names):
        # Rate limiting: wait 1 second between requests
        if i > 0:
            time.sleep(1)

        try:
            response = requests.get(
                url,
                params={"q": name, "format": "json", "limit": 1},
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data:
                    results.append({
                        "name": data[0]["display_name"],
                        "lat": float(data[0]["lat"]),
                        "lon": float(data[0]["lon"])
                    })
                    print(f"✓ Found: {name}")
                else:
                    print(f"✗ Not found: {name}")
            else:
                print(f"✗ Error {response.status_code}: {name}")

        except requests.RequestException as e:
            print(f"✗ Request failed for {name}: {e}")

    return results


# Test
places = [
    "Taipei 101",
    "National Palace Museum",
    "Jiufen Old Street"
]

results = geocode_places(places)
print("\n--- Results ---")
for place in results:
    print(f"{place['name'][:50]}... -> ({place['lat']:.4f}, {place['lon']:.4f})")
```

</details>

---

## 3.7 Rate Limiting Implementation

A proper rate limiter ensures you don't exceed API limits:

```python
import time
import requests

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
            print(f"Rate limiting: waiting {sleep_time:.2f}s...")
            time.sleep(sleep_time)

        self.last_call = time.time()


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


# Usage
client = NominatimClient("CS101-Navigator/1.0 (cs101@university.edu)")

# These calls automatically respect rate limits
result1 = client.search("Taipei Main Station")
result2 = client.search("Taipei 101")  # Waits 1 second automatically
result3 = client.reverse(25.0339, 121.5645)  # Waits 1 second automatically
```

---

## 3.8 Caching API Responses

Don't make the same request twice! Cache your results:

```python
import json
import hashlib
from pathlib import Path

class CachedNominatimClient:
    """Nominatim client with file-based caching."""

    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self, user_agent: str, cache_dir: str = ".cache"):
        self.headers = {"User-Agent": user_agent}
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _cache_key(self, endpoint: str, params: dict) -> str:
        """Generate a unique cache key for a request."""
        # Create a hash of the request
        key_data = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _get_cached(self, cache_key: str) -> dict | None:
        """Try to get cached response."""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            print(f"Cache hit for {cache_key[:8]}...")
            return json.loads(cache_file.read_text())

        return None

    def _save_cache(self, cache_key: str, data: dict):
        """Save response to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_file.write_text(json.dumps(data, indent=2))
        print(f"Cached response as {cache_key[:8]}...")

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Search with caching."""
        params = {"q": query, "format": "json", "limit": limit}
        cache_key = self._cache_key("search", params)

        # Try cache first
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        # Make API call
        time.sleep(1)  # Rate limit
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


# Usage
import time

client = CachedNominatimClient("CS101/1.0 (test@example.com)")

# First call: hits API
result1 = client.search("Taipei 101")

# Second call: uses cache (instant, no API call)
result2 = client.search("Taipei 101")
```

---

## 3.9 Error Handling Best Practices

A robust geocoder handles all error cases:

```python
import requests
import time

class GeocodingError(Exception):
    """Custom exception for geocoding errors."""
    pass


def robust_geocode(place_name: str, max_retries: int = 3) -> dict:
    """
    Geocode with comprehensive error handling.

    Args:
        place_name: Place to geocode
        max_retries: Number of retries for transient errors

    Returns:
        Dict with name, lat, lon

    Raises:
        GeocodingError: If geocoding fails after all retries
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "CS101/1.0 (cs101@university.edu)"}
    params = {"q": place_name, "format": "json", "limit": 1}

    for attempt in range(max_retries):
        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=10
            )

            # Handle specific status codes
            if response.status_code == 200:
                results = response.json()
                if results:
                    return {
                        "name": results[0]["display_name"],
                        "lat": float(results[0]["lat"]),
                        "lon": float(results[0]["lon"])
                    }
                raise GeocodingError(f"No results found for: {place_name}")

            elif response.status_code == 403:
                raise GeocodingError("Forbidden: Check your User-Agent header")

            elif response.status_code == 429:
                # Rate limited - wait and retry
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            elif response.status_code >= 500:
                # Server error - wait and retry
                wait_time = 2 ** attempt
                print(f"Server error. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            else:
                raise GeocodingError(f"HTTP {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"Timeout. Retrying ({attempt + 1}/{max_retries})...")
                time.sleep(1)
                continue
            raise GeocodingError("Request timed out after all retries")

        except requests.exceptions.ConnectionError:
            raise GeocodingError("Network connection failed")

    raise GeocodingError(f"Failed after {max_retries} retries")


# Usage with error handling
try:
    result = robust_geocode("Taipei 101")
    print(f"Found: {result['name']}")
except GeocodingError as e:
    print(f"Geocoding failed: {e}")
```

---

## 3.10 Mini-Exercise 4: Complete Geocoder CLI

Build a command-line geocoding tool:

```python
import requests
import time
import json

def geocoder_cli():
    """Interactive geocoding CLI."""

    print("=== Geocoder CLI ===")
    print("Enter a place name to get coordinates.")
    print("Type 'quit' to exit.\n")

    headers = {"User-Agent": "CS101-Geocoder/1.0 (cs101@university.edu)"}

    while True:
        place = input("Enter place name: ").strip()

        if place.lower() == 'quit':
            print("Goodbye!")
            break

        if not place:
            print("Please enter a place name.\n")
            continue

        # Your code here:
        # 1. Make API call to Nominatim
        # 2. Handle errors
        # 3. Display results nicely
        # 4. Respect rate limits

        pass


if __name__ == "__main__":
    geocoder_cli()
```

<details>
<summary>Solution</summary>

```python
import requests
import time
import json

def geocoder_cli():
    """Interactive geocoding CLI."""

    print("=== Geocoder CLI ===")
    print("Enter a place name to get coordinates.")
    print("Type 'quit' to exit.\n")

    headers = {"User-Agent": "CS101-Geocoder/1.0 (cs101@university.edu)"}
    url = "https://nominatim.openstreetmap.org/search"

    last_request_time = 0

    while True:
        place = input("Enter place name: ").strip()

        if place.lower() == 'quit':
            print("Goodbye!")
            break

        if not place:
            print("Please enter a place name.\n")
            continue

        # Rate limiting
        elapsed = time.time() - last_request_time
        if elapsed < 1:
            time.sleep(1 - elapsed)

        try:
            response = requests.get(
                url,
                params={"q": place, "format": "json", "limit": 3},
                headers=headers,
                timeout=10
            )
            last_request_time = time.time()

            if response.status_code == 200:
                results = response.json()

                if results:
                    print(f"\nFound {len(results)} result(s):\n")
                    for i, r in enumerate(results, 1):
                        print(f"{i}. {r['display_name'][:60]}...")
                        print(f"   Coordinates: ({r['lat']}, {r['lon']})")
                        print(f"   Type: {r.get('type', 'N/A')}\n")
                else:
                    print(f"\nNo results found for '{place}'.\n")

            elif response.status_code == 403:
                print("\nError: Forbidden. Check User-Agent header.\n")

            elif response.status_code == 429:
                print("\nRate limited! Please wait a moment.\n")
                time.sleep(2)

            else:
                print(f"\nError: HTTP {response.status_code}\n")

        except requests.exceptions.Timeout:
            print("\nRequest timed out. Try again.\n")

        except requests.exceptions.ConnectionError:
            print("\nConnection error. Check your internet.\n")


if __name__ == "__main__":
    geocoder_cli()
```

</details>

---

## 3.11 Summary: Key Takeaways

### HTTP Fundamentals
- HTTP is a request/response protocol
- URLs have structure: protocol, host, path, query params
- Status codes tell you what happened (200=OK, 4xx=your fault, 5xx=server fault)

### The `requests` Library
```python
import requests

response = requests.get(
    url,
    params={"key": "value"},      # Query parameters
    headers={"User-Agent": "..."},  # Headers
    timeout=10                      # Always set timeout!
)

if response.status_code == 200:
    data = response.json()
```

### Nominatim API
- Free geocoding service from OpenStreetMap
- **Requires** valid User-Agent header
- **Maximum** 1 request per second
- Two main endpoints: `/search` and `/reverse`

### Best Practices
1. Always include User-Agent header
2. Always set request timeouts
3. Handle all error cases
4. Implement rate limiting
5. Cache responses when possible

---

## 3.12 Homework Assignments

### Assignment 1: Place Lookup Tool (Basic)
Create a script that reads place names from a file and saves their coordinates to another file.

**Input:** `places.txt` (one place per line)
```
Taipei 101
National Palace Museum
Jiufen
```

**Output:** `coordinates.json`
```json
[
    {"name": "Taipei 101", "lat": 25.0339, "lon": 121.5645},
    ...
]
```

### Assignment 2: Distance Calculator (Intermediate)
Build on Assignment 1:
1. Read two place names from user input
2. Geocode both places
3. Calculate the Haversine distance between them
4. Display the result

### Assignment 3: Nearby Places Finder (Advanced)
Create a CLI that:
1. Takes a place name as input
2. Geocodes it
3. Searches for nearby restaurants/cafes (using `viewbox` parameter)
4. Displays the results sorted by distance
5. Saves results to a JSON file

---

## Additional Resources

### Official Documentation
- [Nominatim API Docs](https://nominatim.org/release-docs/latest/api/Overview/)
- [Python Requests Docs](https://docs.python-requests.org/)
- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)

### Practice APIs
- [httpbin.org](https://httpbin.org/) - Test HTTP requests
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Fake REST API

### HTTP References
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

---

## Next Week Preview

**Week 5: The Nominatim API (Deep Dive)**
- Parsing complex nested JSON responses
- Advanced error handling patterns
- Building a complete CLI geocoding tool
- Structured address components

---

*End of Week 4 Lecture*
