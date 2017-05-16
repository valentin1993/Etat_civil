#-*- coding: utf-8 -*-

import requests, os, json, glob 
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from Recensement.models import Attestation_Recensement
from Mairie.models import Mairie 
from Identity.models import Person

from Recensement.forms import Attestation_Recensement_Form
from Identity.forms import PersonForm
from Mairie.forms import MairieForm

from django.views.generic.edit import UpdateView
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext

from datetime import datetime
from dateutil.relativedelta import relativedelta

import Logger, Search, Folds, Docs, Buffer, EnterSearch

from django.contrib import messages 

import Global_variables 


@login_required
def Recensement_array(request) :

    today = datetime.now()
    age_16 = (today - relativedelta(years=16))

    mairie = Mairie.objects.all().last()

    result = Person.objects.filter(birthday__year = age_16.year, city__iexact=mairie.city)

    paginator = Paginator(result, 3)
    page = request.GET.get('page', 1)

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    context = {
    "Person":Person,
    "mairie":mairie,
    "age_16":age_16,
    "datetime" : datetime,
    "result" : result,
    "PageNotAnInteger":PageNotAnInteger,
    }


    return render(request, 'Recensement_resume.html', context)

@login_required
def Liste_Recensement_PDF(request) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID

    today = datetime.now()
    age_16 = (today - relativedelta(years=16))

    mairie = mairie = Mairie.objects.all().last()

    result = Person.objects.filter(birthday__year = age_16.year, city__iexact=mairie.city)

    data = {"mairie" : mairie, "result":result, "today":today}

    template = get_template('Recensement_raw.html')
    html  = template.render(Context(data))

    filename_dir = 'Recensement'
    filename_temp = 'Recensement_' + str(today.year) 
    filename = filename_temp + '.pdf'
    
    path = Global_variables.Individu_path.path + filename
    
    file = open(path, "w+b") 
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.close()

    ###############################
    # Queries with DatasystemsDOC #
    ###############################

    # Search if folder exists or not 
    Folder_research = Search.find_folder(SID, filename_dir)
        
    ########################
    # Folder doesn't exist #
    ########################

    # If folder doesn't exist
    if Folder_research == [] :
        
        print "dossier n'existe pas"
        
        # Create Folder in "Individus" Folder
        Create_Folds = Folds.create(SID, name = filename_dir, parentId = 8552449)
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
        Search_Docs = EnterSearch.find_parameters(SID, title=filename_temp)
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

    context = {
        "mairie":mairie,
        "result":result,
        "DocID" : DocID,
    }

    return render(request, 'Recensement.html', context) # Template page générée après PDF

@login_required
def Attestation_Recensement_Formulary(request) :
    
    query_social_number = request.GET.get('social_number')

    success = False 

    if request.method == 'POST':
        
        form = Attestation_Recensement_Form(request.POST or None)

        if form.is_valid() :    
            post = form.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('Rtreated', kwargs={'id': post.id}))

        else:
            messages.error(request, "Le formulaire est invalide !")

    elif request.method == 'GET':
    
        form = Attestation_Recensement_Form()
        
        if query_social_number :
            if Person.objects.filter(social_number = query_social_number).exists() == True :
                
                individu = get_object_or_404(Person, social_number = query_social_number)
                messages.success(request, 'Le numéro unique existe !')

                form.fields['title'].initial = individu.title
                form.fields['lastname'].initial = individu.lastname
                form.fields['firstname'].initial = individu.firstname
                form.fields['birthday'].initial = individu.birthday
                form.fields['birthcity'].initial = individu.birthcity
                form.fields['birthcountry'].initial = individu.birthcountry
                form.fields['adress'].initial = individu.adress
                form.fields['city'].initial = individu.city
                form.fields['country'].initial = individu.country
                form.fields['sex'].initial = individu.sex
                form.fields['social_number'].initial = individu.social_number

            elif BirthCertificate.objects.filter(social_number = query_social_number).exists() == False :

                messages.error(request, "Le numéro unique est invalide ou déjà existant !")
                

    context = {
        "form" : form
    }

    return render(request, 'form_Recensement.html', context)

@login_required
def Attestation_Recensement_Resume(request, id) :
    
    ar = get_object_or_404(Attestation_Recensement, pk=id)
    return render(request, 'attestation_recensement_resume.html', {"ar" :ar})

@login_required
def Attestation_Recensement_PDF(request, id) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID

    ar = get_object_or_404(Attestation_Recensement, pk=id)
    mairie = mairie = Mairie.objects.all().last()

    data = {"ar" : ar, "mairie":mairie}

    template = get_template('Attestation_Recensement_raw.html')
    html  = template.render(Context(data))

    social_number = str(Attestation_Recensement.objects.get(pk=id).social_number.encode('utf-8'))
    social_number_2 = social_number.replace(" ", "")

    filename_directory = str(Attestation_Recensement.objects.get(pk=id).lastname.encode('utf-8')) + "_" + str(Attestation_Recensement.objects.get(pk=id).firstname.encode('utf-8')) + "_" + social_number_2
    filename_init = 'Attestation_Recensement_' + filename_directory 
    filename = filename_init + '.pdf'
    
    path = Global_variables.Individu_path.path + filename
    
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

            print Search_Docs

            # Update the document in the good folder
            Upload_Docs = Docs.upload(path, SID, Search_Docs_ID, filename)


    Logger.logout(SID)

    context = {"ar":ar,
               "path":path,
               "DocID" : DocID,
                   }
                   
    return render(request, 'Recensement_PDF.html', context)
