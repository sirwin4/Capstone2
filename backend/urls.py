from django.conf.urls import url
from django.urls import include, path
from django.views.generic import TemplateView


from . import views

app_name = "backend"
urlpatterns = [
    url(r'^maps$', views.maps, name='maps'),
    url(r'^location/(?P<pk>[0-9]+)/$', views.location, name="location"),
]