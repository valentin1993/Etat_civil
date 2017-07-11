from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Accueil$', views.Identity_Home, name="Home"),
    url(r'^Choix$', views.Identity_Choice, name="IdentityChoice"),
    url(r'^Formulaire/Individus$', views.Identity_Individu_Form, name="IndividuFormulaire"),
    url(r'^Formulaire/Societes$', views.Identity_Societe_Form, name = "SocieteFormulaire"),
    url(r'^Formulaire/Individus/Resume/(?P<id>\d+)/$', views.Identity_Individu_Resume, name="IndividuResume"),
    url(r'^Formulaire/Societes/Resume/(?P<id>\d+)/$', views.Identity_Societe_Resume, name="SocieteResume"),
    url(r'^Formulaire/Edition$', views.Identity_Update, name="Edition"),
    url(r'^Formulaire/Individus/Recherche$', views.Identity_Individu_Researching, name="IndividuRecherche"),
    url(r'^Formulaire/Societes/Recherche$', views.Identity_Societe_Researching, name="SocieteRecherche"),
    url(r'^Formulaire/Societes/Recherche_Fraude$', views.Identity_Societe_Recherche_Fraude, name="SocieteRechercheFraude"),
    url(r'^Formulaire/Individu/Consultation/PDF/$', views.Identity_Consultation_PDF, name="Consultation"),
    url(r'^Formulaire/Societe/Consultation/PDF/$', views.Identity_Societe_Consultation_PDF, name="SocieteConsultation"),
    url(r'^Formulaire/Supression$', views.Identity_Deleting, name="Suppression"),
    url(r'^Formulaire/Individus/PDF/(?P<id>\d+)/$', views.Identity_Individu_PDF, name="IndividuPDF"),
    url(r'^Formulaire/Societes/PDF/(?P<id>\d+)/$', views.Identity_Societe_PDF, name="SocietePDF"),
    url(r'^Statistiques$', views.Chartview, name="Statistiques"),
    url(r'^Formulaire/Edition/Civilite$', views.Identity_UpdateCivility, name="EditionCivilite"),
    url(r'^Formulaire/Edtiton/Coordonnees$', views.Identity_UpdateCoordonates, name="EditionCoordonnees"),
    url(r'^Formulaire/Edition/Contact$', views.Identity_UpdateContact, name="EditionContact"),
]
