# -*- coding: utf-8 -*-
import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from django.template import Context, RequestContext
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import InformationsInstitution
from Identity import views
from forms import InformationsInstitutionFormulaire

from django.contrib import messages 

@login_required
def Institution_home(request) :

    return render(request, 'Institution_home.html')

@login_required
def Institution_form(request):

    # Fonction permettant de créer le formulaire Mairie et le remplissage

    #query_responsable = request.GET.get('responsable')

    success = False

    if request.method == 'POST':

        Mform = InformationsInstitutionFormulaire(request.POST or None)

        if Mform.is_valid() :   # Vérification sur la validité des données
            post = Mform.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('InstitutionResume'))

        else:
            messages.error(request, "Le formulaire est invalide !")

    else:
        Mform = InformationsInstitutionFormulaire()

        #responsable = Individu.objects.filter(Nom=query_responsable)

        Mform = InformationsInstitutionFormulaire(request.POST or None)
        #Mform.fields['Responsable'].queryset = responsable

        context = {
        "Mform" : Mform,
        #"query_responsable" : query_responsable,
        #"Individu" : Individu
    }

    return render(request, 'Institution_form.html', context)

@login_required
def Institution_Resume(request) :
    
    institution = InformationsInstitution.objects.latest('id')
    return render(request, 'Institution_resume.html', {"institution" : institution})
