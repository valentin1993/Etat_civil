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

@login_required
def Mairie_home(request) :

    return render(request, 'Mairie_home.html')

@login_required
def Mairie_form(request):

    # Fonction permettant de créer le formulaire Mairie et le remplissage

    Mform = MairieForm(request.POST or None)
    template_name = 'Mairie_form.html'

    if Mform.is_valid() :   # Vérification sur la validité des données
        if 'saving' in request.POST :
            post = Mform.save()
            template_name = 'Mairie_Resume.html'
            return HttpResponseRedirect(reverse('Mairieresume'))

    return render(request, template_name, {"Mform" : Mform})

@login_required
def Mairie_Resume(request) :
    
    mairie = Mairie.objects.latest('id')
    return render(request, 'Mairie_resume.html', {"mairie" : mairie})