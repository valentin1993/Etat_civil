from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^table/', views.Table, name="accueiltable"),
    url(r'^annuel/$', views.Table_annuelle_BirthCertificate, name="annuel"),
    url(r'^annuel_PDF/$', views.Table_Naissance_PDF, name="NaissancePDF"),

]
