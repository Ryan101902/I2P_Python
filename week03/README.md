# Week 3: JSON & File I/O

**Phase 1: Data & Coordinates** — "Where am I?"

---

## Concepts
- JSON format
- Reading/Writing files
- Data persistence

---

## Project Task

Save your database of "favorite places" to a `.json` file and write a script to load it back.

### Writing JSON

```python
import json

places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7},
    {"name": "Night Market", "coords": [25.0478, 121.5170], "rating": 4.5},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9},
]

# Save to file
with open("places.json", "w", encoding="utf-8") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)

print("Saved places to places.json")
```

### Reading JSON

```python
import json

# Load from file
with open("places.json", "r", encoding="utf-8") as f:
    places = json.load(f)

# Use the data
for place in places:
    print(f"{place['name']}: {place['rating']} stars")
```

### Sample JSON Structure

```json
[
  {
    "name": "Taipei 101",
    "coords": [25.0330, 121.5654],
    "rating": 4.7,
    "category": "landmark",
    "tags": ["tourist", "shopping", "observation"]
  },
  {
    "name": "Shilin Night Market",
    "coords": [25.0878, 121.5241],
    "rating": 4.5,
    "category": "food",
    "tags": ["night market", "street food", "local"]
  }
]
```

---

## Understanding JSON

JSON (JavaScript Object Notation) maps directly to Python:

| JSON | Python |
|------|--------|
| `{}` object | `dict` |
| `[]` array | `list` |
| `"string"` | `str` |
| `123` | `int` |
| `12.34` | `float` |
| `true/false` | `True/False` |
| `null` | `None` |

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
