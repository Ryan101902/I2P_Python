# Week 10: The "Traveling Salesperson" (Graph Theory Lite)

**Phase 3: Algorithms & Logic** — "Making Smart Decisions"

---

## Concepts
- Permutations
- Brute Force optimization
- Graph Theory basics (nodes, edges, weights)

---

## Project Task

Given 3 selected restaurants, find the order of visitation that results in the shortest total walking time.

### The Problem

You want to visit 3 restaurants. What order minimizes total walking time?

```
Start → Restaurant A → Restaurant B → Restaurant C → End

vs

Start → Restaurant C → Restaurant A → Restaurant B → End

vs ... (other permutations)
```

### Brute Force Solution

```python
from itertools import permutations

def total_walking_time(route, distance_matrix):
    """Calculate total time for a route through all places."""
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i + 1]]
    return total


def find_optimal_route(start, places_to_visit, distance_matrix):
    """
    Find the order of visiting places that minimizes total walking time.
    Uses brute force - checks all permutations.
    """
    best_route = None
    best_time = float('inf')

    # Try all possible orderings
    for perm in permutations(places_to_visit):
        # Route: start -> perm[0] -> perm[1] -> ... -> perm[-1]
        route = [start] + list(perm)
        time = total_walking_time(route, distance_matrix)

        if time < best_time:
            best_time = time
            best_route = route

    return best_route, best_time


# Example
# Places: 0=Start, 1=Pizza A, 2=Pizza B, 3=Pizza C
distance_matrix = [
    [0,  5, 10, 15],  # From Start
    [5,  0,  8,  7],  # From Pizza A
    [10, 8,  0,  6],  # From Pizza B
    [15, 7,  6,  0],  # From Pizza C
]

route, time = find_optimal_route(0, [1, 2, 3], distance_matrix)
print(f"Best route: {route}")
print(f"Total time: {time} minutes")
```

### Why Brute Force Works (For Small N)

| Places | Permutations | Time |
|--------|--------------|------|
| 3 | 6 | Instant |
| 5 | 120 | Instant |
| 10 | 3,628,800 | Slow |
| 15 | 1,307,674,368,000 | Impossible |

For our project (3-5 restaurants), brute force is fine!

---

## Drill

Review **P80–P86 (Graphs)** from *99 Problems in Python*. Visualizing nodes and edges is critical for understanding routing logic.

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
