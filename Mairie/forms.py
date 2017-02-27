#-*- coding: utf-8 -*-

from django import forms
from .models import *

class MairieForm(forms.ModelForm) :
    
    class Meta :
        model = Mairie
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(MairieForm, self).__init__(*args, **kwargs)
    #     self.fields['logo'].required = False