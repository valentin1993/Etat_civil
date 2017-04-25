from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Identity_accueil$', views.Identity_Home, name="home"),
    url(r'^formulaire$', views.Identity_Form, name="form"),
    url(r'^formulaire2$', views.Identity_Form_unique_number, name = "form2"),
    url(r'^formulaire_traite/(?P<id>\d+)/$', views.Identity_Resume, name="treated"),
    url(r'^formulaire2_traite/(?P<id>\d+)/$', views.Identity_Resume_unique_number, name="treated2"),
    url(r'^formulaire_edit$', views.Identity_Update, name="edited"),
    url(r'^recherche$', views.Identity_Researching, name="searched"),
    url(r'^supprimer$', views.Identity_Deleting, name="deleted"),
    url(r'^Identity_PDF/(?P<id>\d+)/$', views.Identity_PDF, name="IdentityPDF"),
    url(r'^statistics$', views.Chartview, name="statistics"),
]
