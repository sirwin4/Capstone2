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
    if len(area_list):
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
    else:
        user_list = Userrack.objects.filter(user=user)
        cam_list = []
        for item in user_list:
            piece = Piece.objects.get(id=item.piece_id)
            if piece.SLCD == True:
                cam_list.append(piece)

        indian_creek = 0
        range_list = ""
        for item in cam_list:
            if item.max_size <= 90 and item.min_size >= 10:
                total = Userrack.objects.get(piece=item.id, user=user).quantity
                expansion = item.max_size - item.min_size
                minimum = (item.min_size - (expansion/2))
                low_end = item.min_size
                for cam in cam_list:
                    if cam.min_size >= 10 and cam.min_size >= minimum and cam.max_size <= item.max_size and cam.id != item.id:
                        total += Userrack.objects.get(piece=cam.id, user=user).quantity
                        if cam.min_size < low_end:
                            low_end = cam.min_size
                        if total >= 10:
                            if indian_creek >= 10:
                                print("cool")
                                if total >= indian_creek:
                                    indian_creek = total
                                value = "%.1f mm to %.1f mm"%(low_end, item.max_size)
                                range_list = value +", " + range_list
                            elif(total >= 10):
                                indian_creek = total
                                value = "%.1f mm to %.1f mm "%(low_end, item.max_size)
                                range_list = value + " covered"

                        elif indian_creek < 10:
                            if total > indian_creek:
                                indian_creek = total
                                percent = total / 10 * 100
                                range_list = '%.1f mm to %.1f mm closest to covered with %.1f percent'%(low_end, item.max_size, percent)
                
        print(range_list)
    arealat = location.lat
    arealong = location.long

    
    context = {
        "location": location,
        "rangelist": range_list,
        "arearack": area_list,
        "userrack": userrack,
        "arealat": arealat,
        "arealong": arealong
    }
    return render(request, 'location.html', context)