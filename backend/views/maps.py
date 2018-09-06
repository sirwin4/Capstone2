from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Area

# Create your views here.

def maps(request):
    """display locations, use mapping JS import to display and create interactive environment"""
    location_list = Area.objects.all().values('name', 'description', 'lat', 'long', 'id')
    locations = list(location_list)
    print(locations[1]['id'])
    context = {"locations": locations}
    return render(request, 'maps.html', context)