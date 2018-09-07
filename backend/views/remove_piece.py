from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from backend.models import Piece
from django.contrib.auth.models import User
from django.urls import reverse

# @login_required
def remove_piece(request, pk):
    piece_requested = Piece.objects.get(id=pk)
    current_user = User.objects.all()[0]
    p = current_user.piece_set.all()
    if len(p):
        if piece_requested in p:
            modify = piece_requested.userrack_set.get(user=current_user)
            if modify.quantity > 0:
                modify.quantity = modify.quantity - 1
                modify.save()
    return HttpResponseRedirect(reverse('backend:piece', kwargs={'pk' : piece_requested.id}))   