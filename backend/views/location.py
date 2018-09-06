from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Area

# Create your views here.

def location(request, pk):
    """display location details of a specific area and its rack"""
    location = Area.objects.get(pk)
    arearack = location.area_rack.all()
    userrack = []
    if request.user.id:
        finalrack = location.user_rack.all()
        for item in userrack:
            if item in arearack:
                userrack.append(item)
                arearack.delete(item)
    arealat = location.lat
    arealong = location.long

    
    context = {
        "location": location,
        "arearack": arearack,
        "userrack": userrack,
        "arealat0": arealat,
        "arealong": arealong
    }
    return render(request, 'location.html', context)