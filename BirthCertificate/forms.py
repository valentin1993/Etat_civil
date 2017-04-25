#-*- coding: utf-8 -*-

from django import forms
from BirthCertificate.models import *
from django_countries.widgets import CountrySelectWidget
from Mairie.models import Mairie

class CustomLabelModelChoiceField(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        self._label_from_instance = kwargs.pop('label_func', force_text)
        super(CustomLabelModelChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return self._label_from_instance(obj)

class BirthCertificateForm(forms.ModelForm):
    fk_parent1 = CustomLabelModelChoiceField(Person.objects.filter(), required=False, label = "Père", label_func=lambda obj: '%s %s %s' % (obj.lastname, obj.firstname, obj.social_number))
    fk_parent2 = CustomLabelModelChoiceField(Person.objects.filter(), required=False, label = "Mère", label_func=lambda obj: '%s %s %s' % (obj.lastname, obj.firstname, obj.social_number))
    mairie = forms.CharField(widget=forms.HiddenInput(), initial=Mairie.objects.using('default').last().city.encode('utf-8'))
    social_number = forms.CharField(widget=forms.HiddenInput(),required=False)


    class Meta :
        model = BirthCertificate
        fields = ['lastname', 'firstname', 'sex', 'birthday', 'birthhour', 'birthcity', 'birthcountry','fk_parent1', 'fk_parent2', 'mairie', 'social_number']
        widgets = {'country': CountrySelectWidget()}

        def __init__(self, *args, **kwargs):    
            super(BirthCertificateForm, self).__init__(*args, **kwargs)
            for key, value in self.fields.iteritems() :
                self.fields[key].widget.attrs.update({'class':'form-fields'})  


class BirthCertificateForm2(forms.ModelForm):
    fk_parent1 = CustomLabelModelChoiceField(Person.objects.filter(), required=False, label = "Père", label_func=lambda obj: '%s %s %s' % (obj.lastname, obj.firstname, obj.social_number), empty_label=None)
    fk_parent2 = CustomLabelModelChoiceField(Person.objects.filter(), required=False, label = "Mère", label_func=lambda obj: '%s %s %s' % (obj.lastname, obj.firstname, obj.social_number), empty_label=None)
    sex = forms.CharField(required=False, label = "Sexe")
    birthcountry = forms.CharField(required=False, label = "Pays de Naissance")
    mairie = forms.CharField(widget=forms.HiddenInput(), initial=Mairie.objects.using('default').last().city.encode('utf-8')) 
    social_number = forms.CharField(widget=forms.HiddenInput(),required=False)


    class Meta :
        model = BirthCertificate
        fields = ['lastname', 'firstname', 'sex', 'birthday', 'birthhour', 'birthcity', 'birthcountry','fk_parent1', 'fk_parent2', 'mairie', 'social_number']
        widgets = {'country': CountrySelectWidget()}

        def __init__(self, *args, **kwargs):    
            super(BirthCertificateForm2, self).__init__(*args, **kwargs)
            for key, value in self.fields.iteritems() :
                self.fields[key].widget.attrs.update({'class':'form-fields'})   


class IdentityForm(forms.ModelForm) :
    
    class Meta :
        model = Person
        fields = ['title', 'lastname', 'firstname', 'sex', 'birthday', 'birthcity', 'birthcountry', 'nationality', 'job', 'adress', 'city', 'zip', 'country', 'mail', 'phone']
        widgets = {'country': CountrySelectWidget()}

