"""Etat_civil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from BirthCertificate import views
from Identity import views
from Accueil import views
from log import views
from Mairie import views
from Table import views
from Recensement import views
from Configurations import views

import debug_toolbar


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^BirthCertificate/', include('BirthCertificate.urls')),
    url(r'^Identity/', include('Identity.urls')),
    url(r'^Accueil/', include('Accueil.urls')),
    url(r'^Home/', include('log.urls')),
    url(r'^Mairie/', include('Mairie.urls')), 
    url(r'^Table/', include('Table.urls')), 
    url(r'^Recensement/', include('Recensement.urls')),
    url(r'^Configurations/', include('Configurations.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
] 