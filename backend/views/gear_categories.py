from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Piece
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render


def gearcat(request, cat):
    cat = int(cat)
    final_cat = ""
    if cat == 1:
        final_cat = 'Cam'
    elif cat == 2:
        final_cat = 'Tricam'
    elif cat == 3:
        final_cat = 'Nut'
    elif cat == 4:
        final_cat = 'Ballnut'
    elif cat == 5:
        final_cat = 'Hex'
    elif cat == 6:
        final_cat = 'Bigbro'
    
    pieces = Piece.objects.filter(gear_type=final_cat)
    p = Paginator(pieces, 50)
    page = request.GET.get('page')
    gear = p.get_page(page)
    context = {
        "pieces": pieces,
        "gear": gear,
        "cat": final_cat
    }
    return render(request, 'gearcat.html', context)

