# Week 14: Interactive Maps with Folium

**Phase 4: The Web Interface** — "Showing the User"

---

## Concepts
- Python-to-JS transpilation
- Folium library (Python wrapper for Leaflet.js)
- Map markers and popups
- Drawing routes on maps

---

## Project Task

Use the `folium` library to generate an interactive map HTML file. Add markers for your found places and draw lines for the calculated route.

### Basic Map

```python
import folium

# Create a map centered on Taipei
m = folium.Map(
    location=[25.0330, 121.5654],  # Taipei 101
    zoom_start=14
)

# Save to HTML
m.save("map.html")
```

### Adding Markers

```python
import folium

m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)

# Add markers for places
places = [
    {"name": "Taipei 101", "coords": [25.0330, 121.5654], "rating": 4.7},
    {"name": "Din Tai Fung", "coords": [25.0339, 121.5645], "rating": 4.9},
    {"name": "Night Market", "coords": [25.0878, 121.5241], "rating": 4.5},
]

for place in places:
    folium.Marker(
        location=place["coords"],
        popup=f"{place['name']}<br>Rating: {place['rating']}",
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
    ).add_to(m)

m.save("places_map.html")
```

### Drawing Routes

```python
import folium

m = folium.Map(location=[25.0400, 121.5400], zoom_start=13)

# Route coordinates (from OSRM geometry)
route_coords = [
    [25.0330, 121.5654],  # Start: Taipei 101
    [25.0380, 121.5550],  # Waypoint
    [25.0420, 121.5450],  # Waypoint
    [25.0478, 121.5170],  # End: Main Station
]

# Draw the route line
folium.PolyLine(
    locations=route_coords,
    color="blue",
    weight=5,
    opacity=0.7
).add_to(m)

# Add start and end markers
folium.Marker(
    route_coords[0],
    popup="Start",
    icon=folium.Icon(color="green", icon="play")
).add_to(m)

folium.Marker(
    route_coords[-1],
    popup="End",
    icon=folium.Icon(color="red", icon="stop")
).add_to(m)

m.save("route_map.html")
```

### Embedding in Flask

```python
from flask import Flask, render_template_string
import folium

app = Flask(__name__)

@app.route("/map")
def show_map():
    # Create map
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)
    folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)

    # Get HTML representation
    map_html = m._repr_html_()

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head><title>Map</title></head>
        <body>
            <h1>Interactive Map</h1>
            {{ map_html | safe }}
        </body>
        </html>
    """, map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
