#-*- coding: utf-8 -*-

import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import BirthCertificate
from Identity.models import Identity
from .forms import BirthCertificateForm
from django.db import connection
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

import Logger, Search, Folds, Docs, Buffer


@login_required
def BirthCertificate_Home(request) :

    return render(request, 'BC_accueil.html')

@login_required
def BirthCertificate_notfound(request) :
    
    return render(request, 'Not_Found.html')

@login_required
def BirthCertificate_accueil(request) :
        
    return render(request, 'Accueil.html')

@login_required
def BirthCertificate_Form(request) :
    # Fonction permettant de créer le formulaire Acte de Naissance et le remplissage

    if request.method == 'POST':
        
        Bform = BirthCertificateForm(request.POST or None)

        if Bform.is_valid() :   # Vérification sur la validité des données
            if '_preview2' in request.POST :
                post = Bform.save(commit=False)
                template_name = 'BC_preview.html'

            elif '_save2' in request.POST :
                post = Bform.save()
                return HttpResponseRedirect(reverse('BC_treated', kwargs={'id': post.id}))

    else:
        Bform = BirthCertificateForm()

    return render(request, 'BC_form.html', {"Bform" : Bform})


        
@login_required
def BirthCertificate_Resume(request, id) :
    
    birthcertificate = get_object_or_404(BirthCertificate, pk=id)
    return render(request, 'BC_resume.html', {"birthcertificate" : birthcertificate})

@login_required
def BirthCertificate_PDF(request, id) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID
    
    folderId = None

    birthcertificate = get_object_or_404(BirthCertificate, pk=id)

    data = {"birthcertificate" : birthcertificate}

    template = get_template('BC_raw.html')
    html  = template.render(Context(data))


    filename_directory = str(BirthCertificate.objects.get(pk=id).lastname.encode('utf-8')) + "_" + str(BirthCertificate.objects.get(pk=id).firstname.encode('utf-8')) + "_" + str(BirthCertificate.objects.get(pk=id).birthday)
    filename_init = 'Acte_Naissance_' + filename_directory 
    filename = filename_init + '.pdf'
    path = '/Users/valentinjungbluth/Desktop/Django/Individus/' + filename

    
    file = open(path, "w+b") 
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.close()

    ###############################
    # Queries with DatasystemsDOC #
    ###############################

    # Search if folder exists or not 
    Folder_research = Search.find_folder(SID, filename_directory)
        
    # If folder doesn't exist
    if Folder_research == [] :
        
        print "dossier n'existe pas"
        
        # Create Folder in "Individus" Folder
        Create_Folds = Folds.create(SID, name = filename_directory, parentId = 8552450)

        print "dossier créé"

        # Create document inside the new folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Create_Folds['id'] )
        print "document ajouté dans dossier créé"


    # If folder already exist
    else :
        
        print "dossier existe déjà"
        
        # Search if document already exist inside by comparing expression
        Search_Docs = Search.find(SID, expression = filename_init, folderId = Folder_research[0]['id'])
        print Search_Docs
        print "Recherche des occurences de documents"

        #Search_Docs_ID = Search_Docs['hits'][0]['id']
        #print Search_Docs_ID

        # If folder exists but not document
        if Search_Docs['totalHits'] == 0 or Search_Docs['hits'][0]['score'] < 90 :
            
            print "pas d'occurence"
            
            # Create document inside the good folder
            Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Folder_research[0]['id'])
            print "nouveau document crée dans dossier existant"

        else :
            
            print "une occurence trouvée"
            
            Search_Docs_ID = Search_Docs['hits'][0]['id']

            # Update the document in the good folder
            Upload_Docs = Docs.upload(path, SID, Search_Docs_ID, filename)


    Logger.logout(SID)

    context = {"birthcertificate":birthcertificate,
               "path":path,
               "folderId" : folderId,
                   }
                   
    return render(request, 'BC_PDF.html', context)