# Copyright (C) 2017     Valentin JUNGBLUTH  <valentin@datasystems.fr>
# Copyright (C) 2017     Alexis MOLTER       <amolter@datasystems.fr>

# This script lets to define urls for "Accueil"

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Choix/', views.Choice, name="choix"),
    url(r'^Accueil/', views.Accueil, name="accueil"),
]
