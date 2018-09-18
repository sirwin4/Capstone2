from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Userrack, Piece
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def profile(request):
    """display piece details of a specific area and its rack"""
    current_user = request.user
    piece_raw = Userrack.objects.filter(user=current_user)
    pieces = []
    if len(piece_raw) != 0:
        for item in piece_raw:
            quantity = item.quantity
            gear = Piece.objects.get(id=item.piece_id)
            setattr(gear, "quantity", quantity)
            pieces.append(gear)
    has_gear = len(pieces)

    context = {
        "current_user": current_user,
        "pieces": pieces,
        "has_gear": has_gear
    }
    return render(request, 'profile.html', context)