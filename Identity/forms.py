#-*- coding: utf-8 -*-

from django import forms
from .models import *

class IdentityForm(forms.ModelForm) :
    
    class Meta :
        model = Identity
        fields = ['title', 'young_girl_lastname' ,'lastname', 'firstname', 'sex', 'birthday', 'birthcity', 'birthcountry', 'nationality', 'job', 'adress', 'city', 'zip', 'country', 'mail', 'phone']
