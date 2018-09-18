from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from backend.models import Piece
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

#add @login_required
def piece(request, pk):
    """display piece details of a specific area and its rack"""
    piece = Piece.objects.get(id=pk)
    user = request.user
    user_gear = []
    if user.username != "":
        user_gear = piece.userrack_set.filter(user=user)
    quantity = 0
    if len(user_gear) != 0:
        quantity = user_gear[0].quantity
    context = {
        "piece": piece,
        "user": user,
        "quantity": quantity
    }
    return render(request, 'piece.html', context)