from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Area, Piece, Arearack, Userrack
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

#add @login_required
def location(request, pk):
    """display location details of a specific area and its rack"""
    location = Area.objects.get(id=pk)
    area_list =list(location.piece_set.all().values('id', 'name', 'standard_number', 'min_size', 'max_size'))
    userrack = []
    user = User.objects.all()[0]
    for item in area_list:
        area_quantity = Arearack.objects.get(area=location.id, piece=item['id']).quantity
        item['areaquantity'] = area_quantity
        user_quantity = Userrack.objects.get(piece=item['id'], user=user).quantity 
        if user_quantity:
            item['userquantity'] = user_quantity
        else:
            item['userquantity'] = 0
        if item['userquantity'] >= item['areaquantity']:
            userrack.append(item)
            area_list.remove(item)
    arealat = location.lat
    arealong = location.long

    
    context = {
        "location": location,
        "arearack": area_list,
        "userrack": userrack,
        "arealat": arealat,
        "arealong": arealong
    }
    return render(request, 'location.html', context)