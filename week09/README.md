# Week 9: Functional Patterns & Sorting

**Phase 3: Algorithms & Logic** — "Making Smart Decisions"

---

## Concepts
- Functional Programming (`map`, `filter`, `reduce`)
- Lambda functions
- Immutability
- Sorting with custom keys

---

## Project Task

Sort the downloaded Places by Rating (High→Low). Use `filter()` or List Comprehensions to purely remove any place further than a 15-minute walk without modifying the original list.

### Sorting Places

```python
places = [
    {"name": "Pizza A", "rating": 4.2, "walk_time": 8},
    {"name": "Pizza B", "rating": 4.8, "walk_time": 12},
    {"name": "Pizza C", "rating": 3.9, "walk_time": 5},
    {"name": "Pizza D", "rating": 4.5, "walk_time": 20},
]

# Sort by rating (highest first) - creates NEW list
sorted_places = sorted(places, key=lambda p: p["rating"], reverse=True)

for p in sorted_places:
    print(f"{p['name']}: {p['rating']} stars")
```

### Filtering (Immutable Style)

```python
# Using filter() - returns iterator
nearby = filter(lambda p: p["walk_time"] <= 15, places)
nearby_list = list(nearby)

# Using list comprehension (more Pythonic)
nearby = [p for p in places if p["walk_time"] <= 15]

# Original list unchanged!
print(len(places))   # Still 4
print(len(nearby))   # 3 (Pizza D filtered out)
```

### Chaining Operations

```python
# Get top 3 nearby places, sorted by rating
result = sorted(
    [p for p in places if p["walk_time"] <= 15],
    key=lambda p: p["rating"],
    reverse=True
)[:3]
```

### Map, Filter, Reduce

```python
from functools import reduce

ratings = [4.2, 4.8, 3.9, 4.5]

# Map: Apply function to each element
doubled = list(map(lambda x: x * 2, ratings))

# Filter: Keep elements that pass test
high_ratings = list(filter(lambda x: x >= 4.0, ratings))

# Reduce: Combine all elements into one
total = reduce(lambda acc, x: acc + x, ratings, 0)
average = total / len(ratings)
```

---

## Drill

Complete **P46–P50 (Logic & Codes)** from *99 Problems in Python*. Understanding truth tables helps with writing complex filter conditions.

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
