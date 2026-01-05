# Week 1: Variables & The Coordinate System / Functions & Distance Logic

**Phase 1: Data & Coordinates** — "Where am I?"

---

## Week 1-1: Variables & The Coordinate System

### Concepts
- Variables
- Floats
- Tuples (Immutable data)

### Project Task
Create a script to store specific locations as `(latitude, longitude)` tuples. Print them out.

### Example
```python
# Storing locations as coordinate tuples
taipei_101 = (25.0330, 121.5654)
ntu_main_gate = (25.0174, 121.5405)
taipei_main_station = (25.0478, 121.5170)

print(f"Taipei 101 is located at: {taipei_101}")
print(f"Latitude: {taipei_101[0]}, Longitude: {taipei_101[1]}")
```

---

## Week 1-2: Functions & Distance Logic

### Concepts
- Math module
- Defining Functions
- Arguments

### CS Concept
**Abstraction** — Hiding complex math behind a function call.

### Project Task
Implement the **Haversine Formula** (calculating distance between two lat/long points on a sphere) as a Python function.

### The Haversine Formula
```python
import math

def haversine(coord1, coord2):
    """
    Calculate the great-circle distance between two points
    on Earth using the Haversine formula.

    Args:
        coord1: (latitude, longitude) tuple for point 1
        coord2: (latitude, longitude) tuple for point 2

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
