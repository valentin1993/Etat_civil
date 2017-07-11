#-*- coding: utf-8 -*-

from django import forms
from .models import *
from Informations.models import InformationsInstitution

class CustomLabelModelChoiceField(forms.ModelChoiceField):
    
    def __init__(self, *args, **kwargs):
        self._label_from_instance = kwargs.pop('label_func', force_text)
        super(CustomLabelModelChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return self._label_from_instance(obj)

class IndividuFormulaire(forms.ModelForm) :
    
    InformationsInstitution = forms.CharField(widget=forms.HiddenInput(), initial=InformationsInstitution.objects.last().Institution.encode('utf-8'))
    Utilisateur = forms.CharField(widget=forms.HiddenInput())

    class Meta :
        model = Individu
        fields = [
                'Etat', 
                'Utilisateur', 
                'Civilite', 
                'NomJeuneFille',
                'Prenom', 
                'Nom', 
                'Statut', 
                'Sexe', 
                'DateNaissance', 
                'VilleNaissance', 
                'PaysNaissance', 
                'Nationalite1', 
                'Nationalite2',
                'Profession', 
                'Adresse', 
                'Ville', 
                'Zip', 
                'Pays', 
                'Mail', 
                'Telephone', 
                'InformationsInstitution',
                'Image',
                'CarteIdentite']


class SocieteFormulaire(forms.ModelForm) :
    
    Responsable = CustomLabelModelChoiceField(Individu.objects.filter(), required=False, label = "Responsable", label_func=lambda obj: '%s %s %s' % (obj.Nom, obj.Prenom, obj.NumeroIdentification))
    InformationsInstitution = forms.CharField(widget=forms.HiddenInput(), initial=InformationsInstitution.objects.using('default').last().Ville.encode('utf-8'))
    Utilisateur = forms.CharField(widget=forms.HiddenInput())

    class Meta :
        model = Societe
        fields = [
                'Nom',
                'Etat', 
                'Utilisateur', 
                'Adresse', 
                'Ville', 
                'Zip', 
                'Region',
                'Pays', 
                'Mail',
                'Web',
                'Telephone',
                'Fax',
                'SIREN',
                'SIRET',
                'NAF_APE',
                'RCS',
                'CHOIX_TVA',
                'TVA',
                'Type',
                'Effectif', 
                'Capital',
                'Responsable',
                'InformationsInstitution',]


class IndividuFormCivility(forms.ModelForm) :
    
    institution = forms.CharField(widget=forms.HiddenInput(), initial=InformationsInstitution.objects.last().Institution.encode('utf-8'))
    Utilisateur = forms.CharField(widget=forms.HiddenInput())

    class Meta :
        model = Individu
        fields = ['Etat', 'Utilisateur', 'Nom', 'Statut', 'Nationalite1', 'Nationalite2', 'Profession', 'Image', 'CarteIdentite']


class IndividuFormCoordonates(forms.ModelForm) :
    
    institution = forms.CharField(widget=forms.HiddenInput(), initial=InformationsInstitution.objects.last().Institution.encode('utf-8'))
    Utilisateur = forms.CharField(widget=forms.HiddenInput())

    class Meta :
        model = Individu
        fields = ['Utilisateur', 'Adresse', 'Ville', 'Zip', 'Pays']

class IndividuFormContact(forms.ModelForm) :
    
    institution = forms.CharField(widget=forms.HiddenInput(), initial=InformationsInstitution.objects.last().Institution.encode('utf-8'))
    Utilisateur = forms.CharField(widget=forms.HiddenInput())

    class Meta :
        model = Individu
        fields = ['Utilisateur', 'Mail', 'Telephone']