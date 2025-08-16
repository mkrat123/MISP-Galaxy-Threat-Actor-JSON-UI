# Create your views here.
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ThreatActor
import pycountry # type: ignore

def index(request):
    return render(request, 'MispGalaxy/threatactor.html')

def threat_actor_browser(request):
    """Render main page with all threat actors list."""
    #actors = ThreatActor.objects.all().order_by("name")
    actors = ThreatActor.objects.all()
    return render(request, "MispGalaxy/threatactor.html", {"actors": actors})


def country_name_to_iso(country_name):
    """Convert country name to ISO Alpha-2 code."""
    if not country_name:
        return None
    try:
        return pycountry.countries.lookup(country_name).alpha_2.lower()
    except LookupError:
        return None  # If country not found, return None

def get_actor_details(request, actor_id):
    actor = ThreatActor.objects.get(id=actor_id)
    victims_raw = list(actor.victims.values_list("victim", flat=True))
    victims_iso = [country_name_to_iso(v) for v in victims_raw if country_name_to_iso(v)]


    return JsonResponse({
        "name": actor.name,
        "description": actor.description,
        "country": country_name_to_iso(actor.country),
        "attribution_confidence": actor.attribution_confidence,
        "suspected_state_sponsor": actor.suspected_state_sponsor,
        "target_category": actor.target_category,
        "incident_type": actor.incident_type,
        "synonyms": list(actor.synonyms.values_list("synonym", flat=True)),
        "victims": victims_iso,  # ✅ Now ISO codes for chart
        "references": list(actor.references.values_list("reference_url", flat=True)),
    })

from django.urls import reverse

def search_actor_ajax(request):
    query = request.GET.get("q", "")
    actors = ThreatActor.objects.filter(
        Q(name__icontains=query) | Q(synonyms__synonym__icontains=query)
    ).distinct()

    data = []
    for actor in actors:
        matching_synonyms = actor.synonyms.filter(synonym__icontains=query).values_list("synonym", flat=True)
        data.append({
            "id": actor.id,
            "name": actor.name,
            "url": reverse("get_actor_details", args=[actor.id]),  # ✅ add full URL
            "synonyms": list(matching_synonyms),
        })

    return JsonResponse(data, safe=False)