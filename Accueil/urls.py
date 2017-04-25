from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^choix/', views.Choice, name="choix"),
    url(r'^accueil/', views.Accueil, name="accueil"),
]
