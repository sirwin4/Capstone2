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
    current_user = User.objects.all()[0]
    quantity = piece.userrack_set.get(user=current_user).quantity
    context = {
        "piece": piece,
        "quantity": quantity
    }
    return render(request, 'piece.html', context)