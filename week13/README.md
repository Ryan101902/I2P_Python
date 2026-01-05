# Week 13: Introduction to Flask (Web Server)

**Phase 4: The Web Interface** — "Showing the User"

---

## Concepts
- Web server basics
- Routes and endpoints
- HTML templates
- Jinja2 templating

---

## Project Task

"Hello World" web server. Passing Python variables to an HTML page using Jinja2.

### Minimal Flask App

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/about")
def about():
    return "This is the Smart City Navigator!"

if __name__ == "__main__":
    app.run(debug=True)
```

Run with:
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### Using Templates

**Folder structure:**
```
project/
├── app.py
└── templates/
    └── index.html
```

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    places = [
        {"name": "Pizza A", "rating": 4.5},
        {"name": "Pizza B", "rating": 4.8},
        {"name": "Pizza C", "rating": 4.2},
    ]
    return render_template("index.html", places=places, title="My Places")

if __name__ == "__main__":
    app.run(debug=True)
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>

    <ul>
    {% for place in places %}
        <li>{{ place.name }} - {{ place.rating }} stars</li>
    {% endfor %}
    </ul>
</body>
</html>
```

### Handling Form Input

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]
        # Do something with query...
        return f"You searched for: {query}"

    return render_template("search.html")
```

---

## Lab Exercises

See the `labs/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
