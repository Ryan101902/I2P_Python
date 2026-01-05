# Week 6: Searching for Places (Lazy Loading)

**Phase 2: The API & The Cloud** — "Fetching the World"

---

## Concepts
- Query parameters
- Pagination
- Lazy Evaluation (Generators)
- The `yield` keyword

---

## Project Task

Script that asks "What do you want to eat?". Use a Generator (`yield`) to handle API pagination, fetching results one page at a time to avoid memory overload.

### Why Generators?

When searching for "pizza" in a city, there might be hundreds of results. Loading all at once:
- Uses lots of memory
- Makes the user wait
- Wastes API calls if user only needs top 5

Generators fetch results **on demand**.

### Generator Example

```python
import requests
import time

def search_places(query, limit_per_page=10):
    """
    Generator that yields places one at a time,
    fetching new pages only when needed.
    """
    headers = {
        "User-Agent": "CS101-Search/1.0 (your-email@university.edu)"
    }

    page = 0

    while True:
        # Fetch next page
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "limit": limit_per_page,
                "offset": page * limit_per_page
            },
            headers=headers
        )

        data = response.json()

        if not data:
            return  # No more results

        # Yield each result one at a time
        for place in data:
            yield {
                "name": place["display_name"],
                "coords": (float(place["lat"]), float(place["lon"]))
            }

        page += 1
        time.sleep(1)  # Rate limiting


# Usage - results are fetched lazily!
search = search_places("pizza taipei")

# Only fetches first page
print("First 3 results:")
for i, place in enumerate(search):
    print(f"  {place['name'][:50]}...")
    if i >= 2:
        break  # Stop early - no wasted API calls!
```

### How Generators Work

```python
def count_up():
    n = 1
    while True:
        yield n  # Pause here, return n
        n += 1   # Resume here when next() is called

counter = count_up()
print(next(counter))  # 1
print(next(counter))  # 2
print(next(counter))  # 3
# Can continue forever, but only computes what you need
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
