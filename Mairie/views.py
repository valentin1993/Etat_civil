# -*- coding: utf-8 -*-
import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from django.template import Context, RequestContext
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Mairie
from forms import MairieForm

from django.contrib import messages 

@login_required
def Mairie_home(request) :

    return render(request, 'Mairie_home.html')

@login_required
def Mairie_form(request):

    # Fonction permettant de créer le formulaire Mairie et le remplissage

    success = False

    if request.method == 'POST':

        Mform = MairieForm(request.POST or None)

        if Mform.is_valid() :   # Vérification sur la validité des données
            post = Mform.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('Mairieresume'))

        else:
            messages.error(request, "Le formulaire est invalide !")

    else:
        Mform = MairieForm()

    return render(request, 'Mairie_form.html', {"Mform" : Mform})

@login_required
def Mairie_Resume(request) :
    
    mairie = Mairie.objects.latest('id')
    return render(request, 'Mairie_Resume.html', {"mairie" : mairie})