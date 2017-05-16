#-*- coding: utf-8 -*-

from django import forms
from .models import *
from Mairie.models import Mairie

class Attestation_Recensement_Form(forms.ModelForm) :
    
    mairie = forms.CharField(widget=forms.HiddenInput(), initial=Mairie.objects.using('default').last().city.encode('utf-8'))
    sex = forms.CharField(required=False, label = "Sexe")
    birthcountry = forms.CharField(required=False, label = "Pays de Naissance")
    social_number = forms.CharField(widget=forms.HiddenInput())

    class Meta :
        model = Attestation_Recensement
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):    
            super(Attestation_Recensement_Form, self).__init__(*args, **kwargs)
            for key, value in self.fields.iteritems() :
                self.fields[key].widget.attrs.update({'class':'form-fields'})