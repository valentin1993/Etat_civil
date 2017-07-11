"""DatasystemsCORE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    http://docs.djangoproject.com/en/1.10/topics/http/urls/
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
import os
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from Identity import views
from Accueil import views
from log import views
from Informations import views
from Configurations import views

import debug_toolbar
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name=os.path.join(settings.BASE_DIR, 'Accueil/templates/Choice.html')),
        name='choice'),
    url(r'^admin/', admin.site.urls),
    url(r'^Identity/', include('Identity.urls')),
    url(r'^Accueil/', include('Accueil.urls')),
    url(r'^Home/', include('log.urls')),
    url(r'^Informations/', include('Informations.urls')), 
    url(r'^Configurations/', include('Configurations.urls')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

