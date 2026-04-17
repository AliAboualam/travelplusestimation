import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loaders import (
    get_hotel_prices,
    load_activities,
    load_guides,
    load_hotels,
    load_monuments,
    load_restaurants,
    load_transport,
)


def form_view(request):
    """Serve the estimation form, injecting CSV data as JSON for the frontend."""
    context = {
        "transport_json": json.dumps(load_transport()),
        "hotels_json": json.dumps(load_hotels()),
        "monuments_json": json.dumps(load_monuments()),
        "restaurants_json": json.dumps(load_restaurants()),
        "activities_json": json.dumps(load_activities()),
        "guides_json": json.dumps(load_guides()),
    }
    return render(request, "estimation_form.html", context)


@csrf_exempt
def submit_estimation(request):
    """
    Receive the form data as JSON, process it, and render the result page.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            payload = request.POST.get("payload", "")
            data = json.loads(payload)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    nb_personnes = data.get("nb_personnes", 1)

    vehicle_lookup = {vehicle["type"]: vehicle for vehicle in load_transport()}
    transport_items = []
    transport_total = 0
    for item in data.get("transport_items", []):
        service_type = item.get("service_type")
        vehicle_type = item.get("vehicle_type")
        quantity = int(item.get("quantity", 0) or 0)
        if service_type not in {"airport", "regular"} or not vehicle_type or quantity <= 0:
            continue

        vehicle = vehicle_lookup.get(vehicle_type)
        if not vehicle:
            continue

        unit_price = vehicle["prix_aeroport"] if service_type == "airport" else vehicle["prix_jour"]
        line_total = unit_price * quantity
        transport_total += line_total
        transport_items.append({
            "service_type": service_type,
            "service_type_label": "Transfert aéroport" if service_type == "airport" else "Mise à disposition",
            "vehicle_type": vehicle["type"],
            "capacite": vehicle["capacite"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total,
        })

    monuments_total = sum(
        m["prix_par_personne"] * nb_personnes
        for m in data.get("monuments", [])
    )

    activities_total = sum(
        a["prix_par_personne"] * nb_personnes
        for a in data.get("activities", [])
    )

    extras_total = sum(
        e["prix_par_personne"] * nb_personnes
        for e in data.get("extras", [])
    )

    hotel_prices = get_hotel_prices()
    total_hotel_price_single = 0
    total_hotel_price_double = 0
    for hotel_entry in data.get("hotels", []):
        prices = hotel_prices.get(hotel_entry["hotel"], {})
        nuits = hotel_entry.get("nuits", 1)
        total_hotel_price_single += (prices.get("prix_single") or 0) * nuits
        total_hotel_price_double += (prices.get("prix_double") or 0) * nuits

    restaurant_total = sum(
        r.get("prix_par_personne", 0) * nb_personnes
        for r in data.get("restaurants", [])
    )

    guides_data = []
    guides_total = 0
    for g in data.get("guides", []):
        jours = g.get("jours", 0)
        if jours <= 0:
            continue
        full_days = int(jours)
        has_half = 1 if (jours - full_days) > 0 else 0
        prix_journee = g.get("prix_journee", 0)
        prix_demi_journee = g.get("prix_demi_journee", 0)
        if prix_journee > 0:
            cout = full_days * prix_journee + has_half * prix_demi_journee
        else:
            half_day_count = int(jours / 0.5)
            cout = half_day_count * prix_demi_journee
        guides_total += cout
        guides_data.append({
            "ville": g.get("ville", ""),
            "jours": jours,
            "cout": cout,
        })

    total_single = transport_total + monuments_total + activities_total + extras_total + restaurant_total + guides_total +  total_hotel_price_single * nb_personnes if nb_personnes > 0 else 0
    total_double = transport_total + monuments_total + activities_total + extras_total + restaurant_total + guides_total +  total_hotel_price_double * nb_personnes if nb_personnes > 0 else 0
    total_par_personne_single = ((transport_total + monuments_total + activities_total + extras_total + restaurant_total + guides_total) / nb_personnes) + total_hotel_price_single if nb_personnes > 0 else 0
    total_par_personne_double = ((transport_total + monuments_total + activities_total + extras_total + restaurant_total + guides_total) / nb_personnes) + total_hotel_price_double if nb_personnes > 0 else 0

    context = {
        "data": data,
        "nb_personnes": nb_personnes,
        "transport_items": transport_items,
        "villes": data.get("villes", []),
        "hotels": data.get("hotels", []),
        "monuments": data.get("monuments", []),
        "activities": data.get("activities", []),
        "restaurants": data.get("restaurants", []),
        "guides": guides_data,
        "extras": data.get("extras", []),
        "transport_total": transport_total,
        "monuments_total": monuments_total,
        "activities_total": activities_total,
        "extras_total": extras_total,
        "restaurant_total": restaurant_total,
        "guides_total": guides_total,
        "total_hotel_price_single": total_hotel_price_single,
        "total_hotel_price_double": total_hotel_price_double,
        "total_single": total_single,
        "total_double": total_double,
        "total_par_personne_single": total_par_personne_single,
        "total_par_personne_double": total_par_personne_double,
        "form_data_json": json.dumps(data),
        "lang": data.get("lang", "fr"),
    }
    return render(request, "estimation_result.html", context)
