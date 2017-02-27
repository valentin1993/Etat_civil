from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^BC_accueil$', views.BirthCertificate_Home, name="BChome"),
    url(r'^formulaire$', views.BirthCertificate_Form, name = "BCform"),
    url(r'^formulaire_traite/(?P<id>\d+)/$', views.BirthCertificate_Resume, name="BC_treated"),
    url(r'^BirthCertificate_PDF/(?P<id>\d+)/$', views.BirthCertificate_PDF, name="PDF"),
    url(r'^not_found$', views.BirthCertificate_notfound, name="BCnotfound"),
]
