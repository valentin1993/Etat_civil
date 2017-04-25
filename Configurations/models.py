# coding: utf-8

from django.db import models
from django.utils.encoding import force_text

FAVORITE_THEME = (
    ('Datasystems', 'Datasystems'),
    ('Cameroun', 'Cameroun'),
)

class Theme(models.Model):
    favorite_theme = models.CharField(max_length = 20, choices=FAVORITE_THEME, verbose_name="Sélectionner le thème", default=None, blank=False)

