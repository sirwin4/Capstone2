from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Piece
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render


def gear(request, cat):
    pieces = Piece.objects.filter(Type=cat)
    p = Paginator(pieces, 50)
    page = request.GET.get('page')
    gear = p.get_page(page)
    context = {
        "gear": gear
    }
    return render(request, 'gear.html', context)