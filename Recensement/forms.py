#-*- coding: utf-8 -*-

from django import forms
from .models import *
from Mairie.models import Mairie

class Attestation_Recensement_Form(forms.ModelForm) :
    
    mairie = forms.CharField(widget=forms.HiddenInput(), initial=Mairie.objects.using('default').last().city.encode('utf-8'))
    
    class Meta :
        model = Attestation_Recensement
        fields = "__all__"