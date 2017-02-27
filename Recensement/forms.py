#-*- coding: utf-8 -*-

from django import forms
from .models import *

class Attestation_Recensement_Form(forms.ModelForm) :
    
    class Meta :
        model = Attestation_Recensement
        fields = "__all__"