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

import Logger, Search, Folds, Docs, Buffer, EnterSearch


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

    query_lastname_father = request.GET.get('lastname_father')
    query_lastname_mother = request.GET.get('lastname_mother')

    if request.method == 'POST':
        
        if Bform.is_valid() :   # Vérification sur la validité des données
            post = Bform.save()
            return HttpResponseRedirect(reverse('BC_treated', kwargs={'id': post.id}))

    else:
        Bform = BirthCertificateForm()

        parent1 = Identity.objects.filter(lastname__icontains=query_lastname_father)
        parent2 = Identity.objects.filter(lastname__icontains=query_lastname_mother)
        Bform = BirthCertificateForm(request.POST or None)
        Bform.fields['fk_parent1'].queryset = parent1.filter(sex="Masculin")
        Bform.fields['fk_parent2'].queryset = parent2.filter(sex="Feminin")

    context = {
        "Bform" : Bform,
        "query_lastname" : query_lastname_father,
        "query_lastname_mother" : query_lastname_mother,
    }

    return render(request, 'BC_form.html', context)


        
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
        
    ########################
    # Folder doesn't exist #
    ########################

    # If folder doesn't exist
    if Folder_research == [] :
        
        print "dossier n'existe pas"
        
        # Create Folder in "Individus" Folder
        Create_Folds = Folds.create(SID, name = filename_directory, parentId = 8552450)
        DocID = Create_Folds[0]['id']

        print DocID

        print "dossier créé"

        # Create document inside the new folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Create_Folds['id'] )
        print "document ajouté dans dossier créé"

    #################
    # Folder exists #
    #################

    # If folder already exist
    else :
        
        DocID = Folder_research[0]['id']
        print DocID
        print "dossier existe déjà"
        
        # Search if document already exist inside by comparing expression
        # Search_Docs = Search.find(SID, expression = filename_init, folderId = Folder_research[0]['id'])
        Search_Docs = EnterSearch.find_parameters(SID, title=filename_init)
        print Search_Docs
        print "Recherche des occurences de documents"

        #Search_Docs_ID = Search_Docs['hits'][0]['id']
        #print Search_Docs_ID

            ############################
            # Folder exists but no doc #
            ############################

        # If folder exists but not document
        if len(Search_Docs) == 0 :
            
            print "nombre d'élément dans la liste : " + str(len(Search_Docs))
            
            # Create document inside the good folder
            Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Folder_research[0]['id'])
            print "nouveau document crée dans dossier existant"

            #############################
            # Folder exists and doc too #
            #############################

        else :
            
            print "Nombre d'occurence trouvée : " + str(len(Search_Docs))
            
            Search_Docs_ID = Search_Docs[0]['id']

            # Update the document in the good folder
            Upload_Docs = Docs.upload(path, SID, Search_Docs_ID, filename)


    Logger.logout(SID)

    context = {"birthcertificate":birthcertificate,
               "path":path,
               "folderId" : folderId,
               "Search_Docs_ID" : Search_Docs_ID,
               "DocID" : DocID,
              }
                   
    return render(request, 'BC_PDF.html', context)