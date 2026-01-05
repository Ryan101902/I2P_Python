# Week 4: HTTP Requests & API Keys

**Phase 2: The API & The Cloud** — "Fetching the World"

---

## Concepts
- The Request/Response cycle
- HTTP Status Codes (200 vs 403 vs 404)
- User-Agent Headers
- API etiquette

---

## Project Task

Make specific calls to `https://nominatim.openstreetmap.org` using the `requests` library. Learn why OSM requires a valid Email/User-Agent to prevent banning.

### Your First API Call

```python
import requests

# IMPORTANT: Always include a User-Agent header!
headers = {
    "User-Agent": "CS101-Project/1.0 (your-email@university.edu)"
}

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={
        "q": "National Taiwan University",
        "format": "json"
    },
    headers=headers
)

# Check status
print(f"Status Code: {response.status_code}")

# Parse JSON response
if response.status_code == 200:
    data = response.json()
    print(data)
```

---

## HTTP Status Codes

| Code | Meaning | What to do |
|------|---------|------------|
| 200 | OK | Success! Parse the response |
| 400 | Bad Request | Check your query parameters |
| 403 | Forbidden | Missing/invalid User-Agent |
| 404 | Not Found | Wrong URL or endpoint |
| 429 | Too Many Requests | Slow down! Add delays |
| 500 | Server Error | Not your fault, try again later |

---

## Why User-Agent Matters

OpenStreetMap is a **free, community-run service**. The User-Agent header:

1. Identifies who is making requests
2. Allows OSM to contact you if there's an issue
3. Helps OSM monitor usage patterns
4. **Required** — requests without it get blocked (403)

```python
# Good User-Agent
headers = {
    "User-Agent": "MyApp/1.0 (contact@example.com)"
}

# Bad (will get blocked!)
headers = {}  # No User-Agent
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
