import csv
from pathlib import Path

FILES_DIR = Path(__file__).resolve().parent.parent / "files"


def _strip_row(row: dict) -> dict:
    """Strip whitespace from keys and values, lowercase keys."""
    return {k.strip().lower(): v.strip() for k, v in row.items() if k and k.strip()}


def _parse_price(value: str):
    """Parse a price string to int. Returns int or None."""
    val = value.strip()
    if not val:
        return None
    try:
        return int(float(val))
    except ValueError:
        return None


def _normalize_city(name: str) -> str:
    """Strip whitespace and title-case city names for consistency."""
    return name.strip().title()


def load_hotels() -> list[dict]:
    """Return list of hotels with parsed numeric prices (None if unavailable)."""
    hotels = []
    with open(FILES_DIR / "Hotels.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = _strip_row(row)
            etoiles_str = row.get("etoiles", "")
            etoiles = int(etoiles_str) if etoiles_str else None
            supplement_str = row.get("supplement dp", "")
            if supplement_str.upper() == "INCLUS":
                supplement = "INCLUS"
            else:
                supplement = _parse_price(supplement_str)
            hotels.append({
                "hotel": row["hotel"],
                "ville": _normalize_city(row["ville"]),
                "etoiles": etoiles,
                "prix_double": _parse_price(row.get("prix par personne en double", "")),
                "prix_single": _parse_price(row.get("prix par personne en single", "")),
                "supplement_dp": supplement,
            })
    return hotels


def load_transport() -> list[dict]:
    """Return list of vehicle options with numeric prices."""
    transport = []
    with open(FILES_DIR / "Transport.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = _strip_row(row)
            transport.append({
                "type": row["type de vehicule"],
                "capacite": int(row.get("capacité maximale en nombre de personnes", "0").split()[0]),
                "prix_aeroport": int(row.get("prix transfer aéroport", "0")),
                "prix_jour": int(row.get("prix de mise à disposition par jour", "0")),
            })
    return transport


def load_monuments() -> list[dict]:
    """Return list of monuments with numeric prices."""
    monuments = []
    with open(FILES_DIR / "Monuments.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = _strip_row(row)
            prix = _parse_price(row.get("prix par personne", ""))
            monuments.append({
                "monument": row["monument"],
                "ville": _normalize_city(row["ville"]),
                "prix": prix if prix is not None else 0,
            })
    return monuments


def load_activities() -> list[dict]:
    """Return list of activities with numeric prices."""
    activities = []
    with open(FILES_DIR / "Activités.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = _strip_row(row)
            prix = _parse_price(row.get("prix par personne", ""))
            activities.append({
                "activite": row["monument"],
                "ville": _normalize_city(row["ville"]),
                "prix": prix if prix is not None else 0,
            })
    return activities


def load_guides() -> list[dict]:
    """Return list of guides with prices per half-day and full-day."""
    guides = []
    with open(FILES_DIR / "Guides.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = _strip_row(row)
            guides.append({
                "ville": _normalize_city(row["ville"]),
                "prix_demi_journee": _parse_price(row.get("prix demi journée", "")) or 0,
                "prix_journee": _parse_price(row.get("prix journée", "")) or 0,
            })
    return guides


def load_restaurants() -> list[dict]:
    """Return list of restaurants with numeric lunch/dinner prices."""
    restaurants = []
    with open(FILES_DIR / "Restaurants.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = _strip_row(row)
            restaurants.append({
                "restaurant": row["restaurant"],
                "ville": _normalize_city(row["ville"]),
                "prix_dejeuner": _parse_price(row.get("prix par personne déjeuner", "")) or 0,
                "prix_diner": _parse_price(row.get("prix par per diner", "")) or 0,
            })
    return restaurants


def get_hotel_prices() -> dict[str, dict]:
    """Return a dict mapping hotel name to its prices."""
    return {
        h["hotel"]: {
            "prix_double": h["prix_double"],
            "prix_single": h["prix_single"],
            "supplement_dp": h["supplement_dp"],
        }
        for h in load_hotels()
    }
