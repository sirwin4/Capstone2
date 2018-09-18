from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from backend.models import Piece, Userrack
from django.contrib.auth.models import User
from django.urls import reverse

# @login_required
def add_piece(request, pk):
    piece_requested = Piece.objects.get(id=pk)
    current_user = request.user
    p = current_user.piece_set.all()
    if len(p):
        print("cool")
        if piece_requested in p:
            modify = piece_requested.userrack_set.get(user=current_user)
            modify.quantity = modify.quantity + 1
            modify.save()
        else:
            Userrack.objects.create(user=current_user, piece=piece_requested, quantity=1)
            
    return HttpResponseRedirect(reverse('backend:piece', kwargs={'pk' : piece_requested.id}))