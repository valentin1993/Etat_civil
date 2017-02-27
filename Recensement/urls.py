from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Recensement_accueil$', views.Recensement_array, name="Rhome"),
    url(r'^Recensement_PDF$', views.Liste_Recensement_PDF, name="RecensementPDF"),
    url(r'^Attestation_Recensement$', views.Attestation_Recensement_Formulary, name="Rform"),
    url(r'^Attestation_Recensement_Resume/(?P<id>\d+)/$', views.Attestation_Recensement_Resume, name="Rtreated"),
    url(r'^Attestation_Recensement_PDF/(?P<id>\d+)/$', views.Attestation_Recensement_PDF, name="RPDF"),

]
