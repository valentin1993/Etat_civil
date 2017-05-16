#-*- coding: utf-8 -*-

import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from BirthCertificate.models import BirthCertificate
from Mairie.models import Mairie 

from BirthCertificate.forms import BirthCertificateForm
from Mairie.forms import MairieForm

from django.views.generic.edit import UpdateView
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext

import datetime
import Logger, Search, Folds, Docs, Buffer, EnterSearch
import Global_variables

@login_required
def Table(request) :
        
    return render(request, 'Table.html')

@login_required
def Table_annuelle_BirthCertificate(request) :

    query_naissance = request.GET.get('q1')
    #request.session['query_naissance'] = query_naissance

    if query_naissance  :
        query_naissance_list = BirthCertificate.objects.filter(created__icontains=query_naissance).order_by('lastname')
    else :
        query_naissance_list = BirthCertificate.objects.none() # == []

    paginator = Paginator(query_naissance_list, 6)
    page = request.GET.get('page', 1)

    try:
        query_naissance_list = paginator.page(page)
    except PageNotAnInteger:
        query_naissance_list = paginator.page(1)
    except EmptyPage:
        query_naissance_list = paginator.page(paginator.num_pages)

    context = {
        "BirthCertificate":BirthCertificate,
        "query_naissance" : query_naissance,
        "query_naissance_list" : query_naissance_list,
        "PageNotAnInteger":PageNotAnInteger,
        }

    return render(request, 'annuel.html', context)

@login_required
def Table_Naissance_PDF(request) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID

    today = datetime.datetime.now()
    query_naissance_list = BirthCertificate.objects.filter(created__icontains=today.year).order_by('lastname')
    mairie = get_object_or_404(Mairie, pk=Mairie.objects.last().id)

    data = {"mairie" : mairie, "query_naissance_list":query_naissance_list, "today":today}

    template = get_template('Table_raw.html')
    html  = template.render(Context(data))

    filename_temp = 'Table_annuelle_Naissance_' + str(today.year) 
    filename = filename_temp + '.pdf'
    path = Global_variables.Individu_path.path + filename

    
    file = open(path, "w+b") 
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.close()

    ###############################
    # Queries with DatasystemsDOC #
    ###############################

     # Search if document already exist inside by comparing expression
    Search_Docs = EnterSearch.find_parameters(SID, title=filename_temp)
    #print Search_Docs
    print "Recherche des occurences de documents"

    # If folder exists but not document
    if len(Search_Docs) == 0 :
            
        print "nombre d'élément dans la liste : " + str(len(Search_Docs))
            
        # Create document inside the good folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = 8978466)
        DocID = Create_Docs[0]['id']
        print "nouveau document crée dans dossier existant"

            #############################
            # Folder exists and doc too #
            #############################

    else :
            
        print "Nombre d'occurence trouvée : " + str(len(Search_Docs))
            
        Search_Docs_ID = Search_Docs[0]['id']

        # Update the document in the good folder
        Upload_Docs = Docs.upload(path, SID, Search_Docs_ID , filename)
        print Upload_Docs

    Logger.logout(SID)
    
    for element in glob.glob(path) :
        os.remove(element)


    context = {
        "mairie":mairie,
        "query_naissance_list":query_naissance_list,
    }

    return render(request, 'Table.html', context) # Template page générée après PDF
