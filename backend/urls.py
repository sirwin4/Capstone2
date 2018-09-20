from django.conf.urls import url
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

app_name = "backend"
urlpatterns = [
    url(r'^maps/$', views.maps, name='maps'),
    url(r'^register/$', views.register, name="register"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/maps'}, name='logout'),
    url(r'^location/(?P<pk>[0-9]+)/$', views.location, name="location"),
    url(r'^piece/(?P<pk>[0-9]+)/$', views.piece, name="piece"),
    url(r'^gear/$', views.gear, name="gear"),
    url(r'^add_piece/(?P<pk>[0-9]+)/$', views.add_piece, name="add_piece"),
    url(r'^remove_piece/(?P<pk>[0-9]+)/$', views.remove_piece, name="remove_piece"),
    url(r'^gearcat/(?P<cat>[0-9]+)/$', views.gearcat, name="gearcat"),

]