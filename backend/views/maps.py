from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Area, Piece, Userrack, Arearack
from django.contrib.auth.models import User
from .coverage_functions import coverage, area_req


def maps(request):
    """display locations, use mapping JS import to display and create interactive environment"""
    location_list = Area.objects.all().values('name', 'description', 'lat', 'long', 'id')
    locations = list(location_list)
    new_locations = []
    user = request.user
    if user.id:
        for location in locations:
            area_list =list(Arearack.objects.values('id', 'piece', 'area'))
            for area in area_list:
                location = Area.objects.get(id=area['area'])
                area_list =list(location.piece_set.all().values('id', 'name', 'min_size', 'max_size'))
                userrack = []
                user = request.user
                if user.is_authenticated:
                    user = user
                else: 
                    user = ''
                areacoverage = 0
                range_list = ""
                if len(area_list) != 0:
                    for item in area_list:
                        area_quantity = Arearack.objects.get(area=location.id, piece=item['id']).quantity
                        item['areaquantity'] = area_quantity
                        if user != '':
                            user_quantity = Userrack.objects.filter(piece=item['id'], user=user)
                            if len(user_quantity) != 0:
                                item['userquantity'] = user_quantity[0].quantity
                            else:
                                item['userquantity'] = 0
                            if item['userquantity'] >= item['areaquantity']:
                                userrack.append(item)
                                area_list.remove(item)
                    
                            cover = coverage(user)
                            areacoverage = area_req.area_req(user, location, cover)
                            new_locale = {"cover": areacoverage}
                            itera = location.__dict__
                            for key in itera.keys():
                                if key != "_state":
                                    new_locale[key] = itera[key]
                            new_locations.append(new_locale)
                            print(new_locale)
                else:
                    user_list = Userrack.objects.filter(user=user)
                    cam_list = []
                    if len(user_list) != 0:
                        for item in user_list:
                            piece = Piece.objects.get(id=item.piece_id)
                            if piece.SLCD == True:
                                cam_list.append(piece)

                        indian_creek = 0
                        for item in cam_list:
                            if item.max_size <= 90 and item.min_size >= 10:
                                total = Userrack.objects.get(piece=item.id, user=user).quantity
                                expansion = item.max_size - item.min_size
                                minimum = (item.min_size - (expansion/2))
                                low_end = item.min_size
                                for cam in cam_list:
                                    if cam.min_size >= 10 and cam.min_size >= minimum and cam.max_size <= item.max_size and cam.id != item.id:
                                        total += Userrack.objects.get(piece=cam.id, user=user).quantity
                                        if cam.min_size < low_end and cam.min_size >= 10:
                                            low_end = cam.min_size
                                        if total >= 10:
                                            if indian_creek >= 10:
                                                if total >= indian_creek:
                                                    indian_creek = total
                                            elif(total >= 10):
                                                indian_creek = total

                                        elif indian_creek < 10:
                                            if total > indian_creek:
                                                indian_creek = total
                                                percent = total / 10 * 100  

    context = {"locations": new_locations}
    return render(request, 'maps.html', context)