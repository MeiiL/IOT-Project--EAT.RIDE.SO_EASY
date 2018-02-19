from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^gmap', views.gmap, name='gmap'),
    url(r'^$', views.motion, name='motion'),
              ]
