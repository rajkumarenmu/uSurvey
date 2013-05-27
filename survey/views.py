from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from investigator_configs import *
from rapidsms.contrib.locations.models import Location
from survey.forms import *
import json

def new_investigator(request):
    list_of_eductional_levels = [education[0] for education in LEVEL_OF_EDUCATION]
    list_of_languages = [language[0] for language in LANGUAGES]
    investigator = InvestigatorForm()
    return render(request, 'investigators/new.html', {'list_of_eductional_levels': list_of_eductional_levels, 'list_of_languages': list_of_languages, 'form': investigator })

def get_locations(request):
    locations = Location.objects.filter(name__icontains=request.GET['q'])
    location_hash = {}
    for location in locations:
        location_hash[location.auto_complete_text()] = location.id
    return HttpResponse(json.dumps(location_hash), content_type="application/json")

def create_or_list_investigators(request):
    investigator = InvestigatorForm(request.POST)
    investigator.save()
    return HttpResponse(status=201)