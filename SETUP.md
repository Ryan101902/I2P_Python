# Setup Guide

This guide will help you set up your development environment for CS101.

---

## Table of Contents

1. [Python Installation](#1-python-installation)
2. [Virtual Environment Setup](#2-virtual-environment-setup)
3. [Installing Required Packages](#3-installing-required-packages)
4. [API Setup & Guidelines](#4-api-setup--guidelines)
5. [Verifying Your Setup](#5-verifying-your-setup)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Python Installation

### Windows

1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. **Important:** Check ✅ "Add Python to PATH" during installation
3. Verify installation:
   ```cmd
   python --version
   ```

### macOS

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

---

## 2. Virtual Environment Setup

A virtual environment keeps your project dependencies isolated.

### Create a Virtual Environment

```bash
# Navigate to the course directory
cd I2P_Python

# Create virtual environment
python3 -m venv venv

# Or on Windows
python -m venv venv
```

### Activate the Virtual Environment

```bash
# macOS / Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of your terminal prompt.

### Deactivate (when done working)

```bash
deactivate
```

---

## 3. Installing Required Packages

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:
- `requests` — For making HTTP API calls
- `flask` — Web framework for the final project
- `folium` — For generating interactive maps

### Manual Installation (if needed)

```bash
pip install requests flask folium
```

### Verify Installation

```bash
pip list
```

You should see `requests`, `flask`, and `folium` in the list.

---

## 4. API Setup & Guidelines

This course uses **free, open APIs**. No API keys required! However, you must follow usage guidelines.

### Nominatim API (OpenStreetMap Geocoding)

**Endpoint:** `https://nominatim.openstreetmap.org`

**Usage Policy (IMPORTANT):**
- Maximum **1 request per second**
- You **MUST** include a valid `User-Agent` header with your email
- Bulk geocoding is prohibited

**Example Request:**

```python
import requests

headers = {
    "User-Agent": "CS101-CourseProject/1.0 (your-email@university.edu)"
}

response = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={
        "q": "National Taiwan University",
        "format": "json"
    },
    headers=headers
)

data = response.json()
print(data[0]["lat"], data[0]["lon"])
```

**Documentation:** [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)

---

### OSRM API (Open Source Routing Machine)

**Demo Server Endpoint:** `https://router.project-osrm.org`

**Usage Policy:**
- Demo server is for **testing only** (not production)
- Be respectful with request frequency
- For heavy usage, consider running your own OSRM server

**Example Request (Walking Route):**

```python
import requests

# Route from point A to point B (longitude,latitude format!)
start = "121.5654,25.0330"  # Taipei 101
end = "121.5598,25.0392"    # Taipei Main Station

url = f"https://router.project-osrm.org/route/v1/foot/{start};{end}"

response = requests.get(url, params={
    "overview": "full",
    "geometries": "geojson"
})

data = response.json()
duration_seconds = data["routes"][0]["duration"]
print(f"Walking time: {duration_seconds / 60:.1f} minutes")
```

**Note:** OSRM uses `longitude,latitude` order (opposite of most mapping systems!)

**Documentation:** [OSRM API Docs](https://project-osrm.org/docs/v5.24.0/api/)

---

### Rate Limiting Best Practice

To avoid getting banned, always add delays between API calls:

```python
import time
import requests

def safe_request(url, headers, params):
    """Make a request with rate limiting."""
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1)  # Wait 1 second before next call
    return response
```

In Week 12, you'll learn to create a `@rate_limit` decorator for this!

---

## 5. Verifying Your Setup

Run this script to verify everything works:

```python
# test_setup.py
import requests
import folium
from flask import Flask

print("=" * 50)
print("CS101 Setup Verification")
print("=" * 50)

# Test 1: Requests library
print("\n[1/4] Testing requests library...")
try:
    r = requests.get("https://httpbin.org/get", timeout=10)
    assert r.status_code == 200
    print("✓ requests is working")
except Exception as e:
    print(f"✗ requests failed: {e}")

# Test 2: Nominatim API
print("\n[2/4] Testing Nominatim API...")
try:
    headers = {"User-Agent": "CS101-SetupTest/1.0 (test@example.com)"}
    r = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": "Taipei", "format": "json", "limit": 1},
        headers=headers,
        timeout=10
    )
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Nominatim API is working (found: {data[0]['display_name'][:40]}...)")
except Exception as e:
    print(f"✗ Nominatim API failed: {e}")

# Test 3: Folium
print("\n[3/4] Testing Folium...")
try:
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)
    folium.Marker([25.0330, 121.5654], popup="Taipei 101").add_to(m)
    m.save("test_map.html")
    print("✓ Folium is working (created test_map.html)")
except Exception as e:
    print(f"✗ Folium failed: {e}")

# Test 4: Flask
print("\n[4/4] Testing Flask...")
try:
    app = Flask(__name__)
    with app.test_client() as client:
        @app.route("/test")
        def test():
            return "OK"
        # Just verify Flask can be imported and configured
    print("✓ Flask is working")
except Exception as e:
    print(f"✗ Flask failed: {e}")

print("\n" + "=" * 50)
print("Setup verification complete!")
print("=" * 50)
```

Save this as `test_setup.py` and run:

```bash
python test_setup.py
```

---

## 6. Troubleshooting

### "pip is not recognized"

- Windows: Reinstall Python and check "Add Python to PATH"
- macOS/Linux: Use `pip3` instead of `pip`

### "SSL Certificate Error" with requests

```bash
pip install --upgrade certifi
```

### "Permission denied" when installing packages

Use `--user` flag:
```bash
pip install --user -r requirements.txt
```

Or use a virtual environment (recommended).

### Nominatim returns 403 Forbidden

You forgot the `User-Agent` header! Always include it:
```python
headers = {"User-Agent": "YourApp/1.0 (your-email@example.com)"}
requests.get(url, headers=headers)
```

### OSRM returns empty routes

Check coordinate order! OSRM uses **longitude,latitude** (not latitude,longitude):
```python
# Correct
"121.5654,25.0330"  # longitude first!

# Wrong
"25.0330,121.5654"  # latitude first (common mistake)
```

### Folium map not displaying

- Make sure you're opening the `.html` file in a web browser
- Check that the coordinates are valid numbers
- Try a simple map first before adding markers

---

## Need Help?

- Check the week's lab materials for specific guidance
- Ask during office hours or lab sessions
- Search the error message online — Stack Overflow is your friend!
