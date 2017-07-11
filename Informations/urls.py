from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Accueil/$', views.Institution_home, name="InstitutionHome"),
    url(r'^Formulaire/$', views.Institution_form, name="InstitutionFormulaire"),
    url(r'^Formulaire/traite/$', views.Institution_Resume, name="InstitutionResume")

]
