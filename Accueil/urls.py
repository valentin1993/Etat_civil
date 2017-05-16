# Copyright (C) 2017     Valentin JUNGBLUTH  <valentin@datasystems.fr>
# Copyright (C) 2017     Alexis MOLTER       <amolter@datasystems.fr>

# This script lets to define urls for "Accueil"

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choix/', views.Choice, name="choix"),
    url(r'^accueil/', views.Accueil, name="accueil"),
    url(r'^test/', views.Test, name="test"),
]
