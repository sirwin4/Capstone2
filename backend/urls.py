from django.conf.urls import url
from django.urls import include, path
from django.views.generic import TemplateView


from . import views

app_name = "backend"
urlpatterns = [
    url(r'^maps/$', views.maps, name='maps'),
    url(r'^location/(?P<pk>[0-9]+)/$', views.location, name="location"),
    url(r'^piece/(?P<pk>[0-9]+)/$', views.piece, name="piece"),
    url(r'^add_piece/(?P<pk>[0-9]+)/$', views.add_piece, name="add_piece"),
    url(r'^remove_piece/(?P<pk>[0-9]+)/$', views.remove_piece, name="remove_piece"),
]