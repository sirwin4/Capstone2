from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Piece
from django.contrib.auth.models import User
from django.core.paginator import Paginator

def gear(request):
    pieces = Piece.objects.all()
    p = Paginator(pieces, 50)
    context = {
        "pieces": pieces
    }
    return render(request, 'gear.html', context)