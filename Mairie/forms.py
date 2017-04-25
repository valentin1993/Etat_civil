#-*- coding: utf-8 -*-

from django import forms
from .models import *

class MairieForm(forms.ModelForm) :
    
    class Meta :
        model = Mairie
        fields = '__all__'
