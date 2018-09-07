from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Area, Piece, Userrack, Arearack
from django.contrib.auth.models import User
# Create your views here.

def maps(request):
    """display locations, use mapping JS import to display and create interactive environment"""
    location_list = Area.objects.all().values('name', 'description', 'lat', 'long', 'id')
    locations = list(location_list)
    user = User.objects.all()[0]
    if user.id:
        for location in locations:
            area_list =list(Arearack.objects.values('id'))
            for item in area_list:
                area_quantity = Arearack.objects.filter(area=location['id'], piece=item['id'])[0].quantity
                user_quantity = Userrack.objects.get(piece=item['id'], user=user).quantity 
                if user_quantity:
                    location['coverage'] = (user_quantity / area_quantity * 100)
                else:
                    location['coverage'] = 0
                print(location['coverage'])

    context = {"locations": locations}
    return render(request, 'maps.html', context)