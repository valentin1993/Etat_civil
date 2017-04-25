#-*- coding: utf-8 -*-

from django import forms
from .models import *
from Mairie.models import Mairie

class PersonForm(forms.ModelForm) :
    
    mairie = forms.CharField(widget=forms.HiddenInput(), initial=Mairie.objects.using('default').last().city.encode('utf-8'))

    class Meta :
        model = Person
        fields = ['title', 'young_girl_lastname' ,'lastname', 'firstname', 'status', 'sex', 'birthday', 'birthcity', 'birthcountry', 'birthmairie', 'nationality', 'job', 'adress', 'city', 'zip', 'country', 'mail', 'phone', 'mairie']


class PersonForm2(forms.ModelForm) :
    
    mairie = forms.CharField(widget=forms.HiddenInput(), initial=Mairie.objects.using('default').last().city.encode('utf-8'))
    sex = forms.CharField(required=False, label = "Sexe")
    birthcountry = forms.CharField(required=False, label = "Pays de Naissance")
    social_number = forms.CharField(widget=forms.HiddenInput())
    
    class Meta :
        model = Person
        fields = ['title', 'young_girl_lastname' ,'lastname', 'firstname', 'status', 'sex', 'birthday', 'birthcity', 'birthcountry', 'birthmairie', 'nationality', 'job', 'adress', 'city', 'zip', 'country', 'mail', 'phone', 'mairie', 'social_number']
    
    def __init__(self, *args, **kwargs):    
            super(PersonForm2, self).__init__(*args, **kwargs)
            for key, value in self.fields.iteritems() :
                self.fields[key].widget.attrs.update({'class':'form-fields'})