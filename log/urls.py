# log/urls.py
from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^login/$', views.connexion, name='login'),
    url(r'^logout/$', views.deconnexion, name='logout'),
    url(r'^Users/Connected/$', views.ConnectedUsers, name='ConnectedUsers'),
]