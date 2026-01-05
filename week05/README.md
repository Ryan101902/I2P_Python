# Week 5: The Nominatim API (Geocoding)

**Phase 2: The API & The Cloud** — "Fetching the World"

---

## Concepts
- Parsing complex nested JSON responses
- Error Handling (`try/except`)
- Geocoding (converting addresses to coordinates)

---

## Project Task

Build a CLI tool: User types "Empire State Building", script returns `(40.748, -73.985)` using the OSM free search endpoint.

### Geocoding CLI Tool

```python
import requests
import sys

def geocode(query):
    """Convert a place name to coordinates using Nominatim."""
    headers = {
        "User-Agent": "CS101-Geocoder/1.0 (your-email@university.edu)"
    }

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "limit": 1
            },
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # Raise exception for bad status codes

        data = response.json()

        if not data:
            return None, "No results found"

        result = data[0]
        lat = float(result["lat"])
        lon = float(result["lon"])
        display_name = result["display_name"]

        return (lat, lon), display_name

    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"
    except (KeyError, IndexError, ValueError) as e:
        return None, f"Parse error: {e}"


if __name__ == "__main__":
    while True:
        query = input("\nEnter a place name (or 'quit'): ").strip()

        if query.lower() == 'quit':
            break

        coords, info = geocode(query)

        if coords:
            print(f"Coordinates: {coords}")
            print(f"Full name: {info}")
        else:
            print(f"Error: {info}")
```

---

## Error Handling Patterns

```python
try:
    # Code that might fail
    response = requests.get(url)
    data = response.json()
    result = data[0]["lat"]

except requests.exceptions.ConnectionError:
    print("Cannot connect to the server")

except requests.exceptions.Timeout:
    print("Request timed out")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")

except json.JSONDecodeError:
    print("Invalid JSON response")

except (KeyError, IndexError):
    print("Unexpected response format")
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
