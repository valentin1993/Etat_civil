#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from .models import Theme

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        widgets = {'favorite_theme' : forms.RadioSelect, }
        fields=('favorite_theme',)


