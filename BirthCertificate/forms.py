#-*- coding: utf-8 -*-

from django import forms
from BirthCertificate.models import *
from django_countries.widgets import CountrySelectWidget

class CustomLabelModelChoiceField(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        self._label_from_instance = kwargs.pop('label_func', force_text)
        super(CustomLabelModelChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return self._label_from_instance(obj)

class BirthCertificateForm(forms.ModelForm):
    fk_parent1 = CustomLabelModelChoiceField(Identity.objects.filter(sex = "Masculin"), required=False, label = "Père", label_func=lambda obj: '%s %s %s %s' % (obj.lastname, obj.firstname, obj.birthday, obj.birthcity))
    fk_parent2 = CustomLabelModelChoiceField(Identity.objects.filter(sex = "Feminin"), required=False, label = "Mère", label_func=lambda obj: '%s %s %s %s' % (obj.lastname, obj.firstname, obj.birthday, obj.birthcity))

    class Meta :
        model = BirthCertificate
        fields = ['lastname', 'firstname', 'sex', 'birthday', 'birthhour', 'birthcity', 'birthcountry','fk_parent1', 'fk_parent2']
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):    
        super(BirthCertificateForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.iteritems() :
            self.fields[key].widget.attrs.update({'class':'form-fields'})   


class IdentityForm(forms.ModelForm) :
    
    class Meta :
        model = Identity
        fields = ['title', 'lastname', 'firstname', 'sex', 'birthday', 'birthcity', 'birthcountry', 'nationality', 'job', 'adress', 'city', 'zip', 'country', 'mail', 'phone']
        widgets = {'country': CountrySelectWidget()}

