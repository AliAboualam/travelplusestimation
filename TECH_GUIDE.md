# Technology Guide — Excursion Estimation Project

## Overview

This project is a Django web application for generating tourist circuit cost estimations. Users fill in a form selecting transport, hotels, monuments, restaurants, and extras; the backend computes totals and renders a result page.

---

## Stack at a Glance

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | Django 6.0.4 |
| Database | SQLite 3 (via Django ORM) |
| Data source | CSV files parsed with Python's `csv` stdlib module |
| Frontend rendering | Django template engine (Jinja2-style syntax) |
| Frontend styling | Tailwind CSS 3 (CDN) |
| Frontend logic | Vanilla JavaScript (ES2020) |
| Excel → CSV conversion | pandas 3.0 + openpyxl 3.1 |

---

## Technologies in Detail

### Python 3.12
The runtime for the entire backend. Key standard-library modules used:
- **`csv`** — reads the Hotels, Transport, Monuments, and Restaurants CSV files in `estimation/data_loaders.py`
- **`json`** — serialises Python dicts to JSON for the frontend and deserialises form submissions from the browser
- **`pathlib.Path`** — provides OS-agnostic file paths to locate the `files/` directory

### Django 6.0.4
The main web framework. Concepts used:

| Concept | Where |
|---|---|
| URL routing (`urls.py`) | Maps `/` → form view, `/submit/` → estimation view |
| Function-based views | `form_view`, `submit_estimation` in `estimation/views.py` |
| Template rendering (`render`) | Passes Python context dicts to HTML templates |
| `JsonResponse` | Returns 405 / 400 error responses |
| `csrf_exempt` decorator | Temporarily disables CSRF for the `/submit/` endpoint (to be replaced with JS CSRF header in production) |
| ORM / migrations | Provided by Django; database models defined in `estimation/models.py` |
| `manage.py` | CLI entry point: `runserver`, `migrate`, `makemigrations` |
| `settings.py` | Configures `BASE_DIR`, `INSTALLED_APPS`, `TEMPLATES`, `DATABASES` |

**Key dependencies pulled in by Django:**
- **asgiref 3.11** — ASGI compatibility layer (used by Django's async support)
- **sqlparse 0.5** — SQL formatter used internally by Django's ORM debug output

### SQLite 3
The default database bundled with Python. Managed entirely through Django's ORM and migration system. The database file is `excursionEstimation/db.sqlite3`.

### CSV data layer (`estimation/data_loaders.py`)
Four CSV files in `files/` act as the application's price catalogue:
- `Hotels.csv` — hotel name, city, double price, single price
- `Transport.csv` — vehicle type, capacity, airport transfer price, daily price
- `Monuments.csv` — monument name, city, entry price per person
- `Restaurants.csv` — restaurant name, city, lunch price, dinner price

`data_loaders.py` exposes:
- `load_hotels()`, `load_transport()`, `load_monuments()`, `load_restaurants()` — return plain Python lists of dicts with cleaned, typed values
- `get_hotel_prices()` — convenience dict keyed by hotel name for O(1) lookup in `views.py`

Prices are stored as plain integers (Dhs). `None` indicates "price on request."

### Django Template Engine
Used to render `estimation_form.html` and `estimation_result.html`. Key features used:
- `{{ variable }}` — outputs Python context values
- `{{ variable|safe }}` — outputs a pre-serialised JSON string without HTML-escaping (used to inject CSV data into JavaScript constants)

### Tailwind CSS 3 (CDN)
Utility-first CSS framework loaded from `https://cdn.tailwindcss.com`. Applied directly to HTML elements via class names. No build step required in development.

### Vanilla JavaScript (ES2020)
All frontend logic lives inside a `<script>` block in `estimation_form.html`. Responsibilities:
- Dynamically renders city checkboxes, hotel rows, monument checkboxes, restaurant rows, and extras from the `HOTELS`, `MONUMENTS`, `RESTAURANTS`, `TRANSPORT` constants (injected by Django)
- Suggests the appropriate vehicle type based on the number of passengers
- Collects form state into a structured JSON payload on submit
- POSTs JSON to `/submit/` via the Fetch API, then replaces the page with the HTML response

### pandas 3.0 + openpyxl 3.1
Used exclusively in `files/files_creation/price_creation.py` — a one-off utility script that converts source Excel price sheets (`Tarifs prestataires.xlsx`) into the CSV files consumed by the application. Not a runtime dependency of the Django app itself.

Other packages installed alongside pandas:
- **numpy 2.4** — numerical backend for pandas
- **python-dateutil 2.9** — date parsing for pandas
- **et_xmlfile 2.0 / lxml 6.0** — XML/XLSX parsing helpers for openpyxl
- **python-docx 1.2** — not used yet; available for future Word document generation

---

## Project Structure

```
excursionEstimation/
├── manage.py                  # Django CLI
├── db.sqlite3                 # SQLite database
├── circuit_project/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── estimation/                # Main Django app
│   ├── views.py               # Form view + estimation submission logic
│   ├── data_loaders.py        # CSV parsing layer
│   ├── models.py
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── estimation_form.html   # Form page (Tailwind + Vanilla JS)
│   └── estimation_result.html # Result page
└── files/
    ├── Hotels.csv
    ├── Transport.csv
    ├── Monuments.csv
    ├── Restaurants.csv
    └── files_creation/
        └── price_creation.py  # Excel → CSV converter
```

---

## Data Flow

```
Browser          Django           data_loaders.py      CSV files
  |                |                    |                   |
  |-- GET / ------>|                    |                   |
  |                |-- load_*() ------->|-- open/parse ---->|
  |                |<---- lists --------|                   |
  |<-- HTML+JSON --|                    |                   |
  |                |                    |                   |
  |-- POST /submit/ (JSON) ------------>|                   |
  |                |-- get_hotel_prices()>|-- parse -------->|
  |                |<---- dict ----------|                   |
  |                |-- compute totals    |                   |
  |<-- HTML result--|                    |                   |
```
