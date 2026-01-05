# Week 15: Final Integration Sprint

**Phase 4: The Web Interface** — "Showing the User"

---

## Focus

Connecting all the pieces:

```
User Input Form → Flask → Nominatim API → Sorting Logic → Folium Map Display
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Flask Web Server                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  HTML Form   │───▶│  Flask Route │───▶│  Nominatim API   │  │
│  │  (User Input)│    │  (Controller)│    │  (Find Places)   │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
│                              │                    │             │
│                              ▼                    ▼             │
│                      ┌──────────────┐    ┌──────────────────┐  │
│                      │  OSRM API    │◀───│  Filter & Sort   │  │
│                      │  (Get Routes)│    │  (Business Logic)│  │
│                      └──────────────┘    └──────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│                      ┌──────────────────────────────────────┐  │
│                      │        Folium Map Generation         │  │
│                      │   (Markers + Route + Interactive)    │  │
│                      └──────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│                      ┌──────────────────────────────────────┐  │
│                      │          HTML Response               │  │
│                      │      (Map embedded in page)          │  │
│                      └──────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
smart_city_navigator/
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page with search form
│   └── results.html      # Results page with map
├── static/
│   └── style.css         # Optional styling
└── utils/
    ├── __init__.py
    ├── geocoding.py      # Nominatim API wrapper
    ├── routing.py        # OSRM API wrapper
    ├── places.py         # Place class and helpers
    └── mapping.py        # Folium map generation
```

---

## Integration Checklist

- [ ] User can enter a starting location
- [ ] User can select a category (food, cafe, etc.)
- [ ] User can set a time constraint (e.g., 10 min walk)
- [ ] App geocodes the starting location (Nominatim)
- [ ] App searches for nearby places (Nominatim)
- [ ] App gets real walking times (OSRM)
- [ ] App filters places by walking time
- [ ] App sorts places by rating
- [ ] App optimizes visiting order (TSP)
- [ ] App generates interactive map (Folium)
- [ ] Map shows markers for all places
- [ ] Map shows route between places
- [ ] Results display on web page

---

## Tips for Integration

1. **Test each component separately first**
2. **Handle errors gracefully** — APIs can fail
3. **Add loading indicators** — API calls take time
4. **Cache results** — Avoid repeated API calls
5. **Rate limit** — Use your `@rate_limit` decorator

---

## Lab Exercises

See the `labs/` folder for integration exercises.

## Lecture Materials

See the `lectures/` folder for the final architecture discussion.
