# Week 2: Lists, Loops & Dictionaries

**Phase 1: Data & Coordinates** — "Where am I?"

---

## Week 2-1: Lists, Loops & The Route

### Concepts
- Lists
- `for` loops
- `range`, `zip`, `map`, `filter`

### Project Task
Create a list of 5 coordinate tuples. Write a loop that calculates the total distance of the path connecting them sequentially.

### Example
```python
from haversine import haversine  # Your function from Week 1

route = [
    (25.0330, 121.5654),  # Taipei 101
    (25.0478, 121.5170),  # Taipei Main Station
    (25.0474, 121.5149),  # Zhongshan
    (25.0525, 121.5204),  # Shuanglian
    (25.0632, 121.5233),  # Minquan W. Rd.
]

total_distance = 0
for i in range(len(route) - 1):
    segment = haversine(route[i], route[i + 1])
    print(f"Segment {i+1}: {segment:.2f} km")
    total_distance += segment

print(f"Total route distance: {total_distance:.2f} km")
```

### Drill
Complete **P01–P10 (Lists)** from *99 Problems in Python* to master indexing and list manipulation.

---

## Week 2-2: Dictionaries & Storing "Places"

### Concepts
- Dictionaries (Key-Value pairs)
- Nested structures

### Project Task
Move from simple tuples to storing complex data:

```python
place = {
    "name": "Joe's Pizza",
    "coords": (40.71, -74.00),
    "rating": 4.5,
    "category": "restaurant",
    "tags": ["pizza", "italian", "cheap"]
}

# Accessing data
print(place["name"])           # Joe's Pizza
print(place["coords"][0])      # 40.71 (latitude)
print(place["tags"][0])        # pizza
```

### Building a Places Database
```python
places = [
    {"name": "Spot A", "coords": (25.033, 121.565), "rating": 4.2},
    {"name": "Spot B", "coords": (25.041, 121.551), "rating": 4.8},
    {"name": "Spot C", "coords": (25.029, 121.559), "rating": 3.9},
]

# Find highest rated
best = max(places, key=lambda p: p["rating"])
print(f"Best place: {best['name']} ({best['rating']} stars)")
```

### Drill
Complete **P11–P15 (Run-length encoding/Data compression)** from *99 Problems in Python*. These problems teach you how to process lists and look for patterns.

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
