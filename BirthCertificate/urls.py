from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^BC_accueil$', views.BirthCertificate_Home, name="BChome"),
    url(r'^formulaire$', views.BirthCertificate_Form, name = "BCform"),
    url(r'^formulaire2$', views.BirthCertificate_Form_unique_number, name = "BCform2"),
    url(r'^formulaire_traite/(?P<id>\d+)/$', views.BirthCertificate_Resume, name="BC_treated"),
    url(r'^formulaire2_traite/(?P<id>\d+)/$', views.BirthCertificate_Resume_unique_number, name="BC_treated2"),
    url(r'^BirthCertificate_PDF/(?P<id>\d+)/$', views.BirthCertificate_PDF, name="PDF"),
    url(r'^not_found$', views.BirthCertificate_notfound, name="BCnotfound"),
]
