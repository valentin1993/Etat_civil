#-*- coding: utf-8 -*-

from django import forms
from .models import *

class InformationsInstitutionFormulaire(forms.ModelForm) :
    
    class Meta :
        model = InformationsInstitution
        fields = '__all__'
