from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accueil/$', views.Mairie_home, name="Mairiehome"),
    url(r'^formulaire/$', views.Mairie_form, name="Mairieform"),
    url(r'^formulaire_traite/$', views.Mairie_Resume, name="Mairieresume")


]
