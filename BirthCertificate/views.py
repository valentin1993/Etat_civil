#-*- coding: utf-8 -*-

import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from models import BirthCertificate
from Identity.models import Person
from Mairie.models import Mairie
from .forms import BirthCertificateForm, BirthCertificateForm2
from django.db import connection
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.contrib import messages 
from random import randint

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


    query_social_number_father = request.GET.get('social_number_father')
    query_social_number_mother = request.GET.get('social_number_mother')

    success = False

    if request.method == 'POST':
        
        form = BirthCertificateForm(request.POST or None)

        if form.is_valid() :   # Vérification sur la validité des données
            post = form.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('BC_treated', kwargs={'id': post.id}))

        else:
            messages.error(request, "Le formulaire est invalide !")

    else:
        form = BirthCertificateForm()

        parent1 = Person.objects.filter(social_number=query_social_number_father)
        parent2 = Person.objects.filter(social_number=query_social_number_mother)

        form = BirthCertificateForm(request.POST or None)
        form.fields['fk_parent1'].queryset = parent1
        form.fields['fk_parent2'].queryset = parent2

    context = {
        "form" : form,
        "query_social_number_father" : query_social_number_father,
        "query_social_number_mother" : query_social_number_mother,
    }

    return render(request, 'BC_form.html', context)

@login_required
def BirthCertificate_Form_unique_number(request) :
    
    validity = []
    submission = []
    #User fill some fields
    query_social_number = request.GET.get('social_number')
    query_social_number_father = request.GET.get('social_number_father')
    query_social_number_mother = request.GET.get('social_number_mother')

    success = False
    
    if request.method == 'POST':
            
        form = BirthCertificateForm2(request.POST or None)

        if form.is_valid() :   # Vérification sur la validité des données
            post = form.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('BC_treated2', kwargs={'id': post.id}))
            
        else:
            messages.error(request, "Le formulaire est invalide !")

    elif request.method == 'GET':
        
        form = BirthCertificateForm2()
        
        parent1 = Person.objects.filter(social_number=query_social_number_father)
        parent2 = Person.objects.filter(social_number=query_social_number_mother)

        if query_social_number :
            if Person.objects.filter(social_number = query_social_number).exists() == True :
                
                individu = get_object_or_404(Person, social_number = query_social_number)
                messages.success(request, 'Le numéro unique existe !')

                form.fields['fk_parent1'].queryset = parent1
                form.fields['fk_parent2'].queryset = parent2
                form.fields['lastname'].initial = individu.lastname
                form.fields['firstname'].initial = individu.firstname
                form.fields['birthday'].initial = individu.birthday
                form.fields['birthcity'].initial = individu.birthcity
                form.fields['birthcountry'].initial = individu.birthcountry
                form.fields['sex'].initial = individu.sex
                form.fields['social_number'].initial = individu.social_number

            elif Person.objects.filter(social_number = query_social_number).exists() == False :
                
                validity = False
                messages.error(request, "Le numéro unique est invalide !")
                

    context = {
        "form" : form,
        "validity" : validity,
        "submission" : submission
        
    }

    return render(request, 'BC_form2.html', context)


@login_required
def BirthCertificate_Resume_unique_number(request, id) :
    
    birthcertificate = get_object_or_404(BirthCertificate, pk=id)

    context = {
            "birthcertificate" : birthcertificate,
    }

    return render(request, 'BC_resume2.html', context)
        
@login_required
def BirthCertificate_Resume(request, id) :
    
    birthcertificate = get_object_or_404(BirthCertificate, pk=id)
        
    #Homme = 1 / Femme = 2
    sex_number = []
    if birthcertificate.sex == 'Masculin' :
        sex_number = 1
        print sex_number
    else :
        sex_number = 2
        print sex_number

    #Récupère année de naissance
    birthyear_temp = str(birthcertificate.birthday.year)
    birthyear_temp2 = str(birthyear_temp.split(" "))
    birthyear = birthyear_temp2[4] + birthyear_temp2[5]

    #Récupère mois de naissance
    birthmonth_temp = birthcertificate.birthday.month
    if len(str(birthmonth_temp)) == 1 :
        birthmonth = '0' + str(birthmonth_temp)
    else :
        birthmonth = birthmonth_temp

    #Récupère N° Mairie (ici récupère nom mais sera changé en n°)
    birth_mairie = birthcertificate.mairie
    print birth_mairie

    #Génère un nombre aléaloire :
    key_temp = randint(0,999999)
    if len(str(key_temp)) == 1 :
        key = '00000' + str(key_temp)
    elif len(str(key_temp)) == 2 :
        key = '0000' + str(key_temp)
    elif len(str(key_temp)) == 3 :
        key = '000' + str(key_temp)
    elif len(str(key_temp)) == 4 :
        key = '00' + str(key_temp)
    elif len(str(key_temp)) == 5 :
        key = '0' + str(key_temp)
    else :
        key = key_temp
    print key

    social_number = str(sex_number) + ' ' + str(birthyear) + ' ' + str(birthmonth) + ' ' + str(birth_mairie) + ' - ' + str(key) 
    print social_number

    #Mise à jour du champ numéro sécurité social
    birthcertificate.social_number = social_number
    birthcertificate.save()

    context = {
            "birthcertificate" : birthcertificate,
    }

    return render(request, 'BC_resume.html', context)

@login_required
def BirthCertificate_PDF(request, id) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID
    
    folderId = None

    birthcertificate = get_object_or_404(BirthCertificate, pk=id)

    data = {"birthcertificate" : birthcertificate}

    template = get_template('BC_raw.html')
    html  = template.render(Context(data))

    social_number = str(BirthCertificate.objects.get(pk=id).social_number.encode('utf-8'))
    social_number_2 = social_number.replace(" ", "")

    filename_directory = str(BirthCertificate.objects.get(pk=id).lastname.encode('utf-8')) + "_" + str(BirthCertificate.objects.get(pk=id).firstname.encode('utf-8')) + "_" + social_number_2
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
        folderId = Create_Folds[0]['id']

        print folderId

        print "dossier créé"

        # Create document inside the new folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Create_Folds['id'] )
        print "document ajouté dans dossier créé"

    #################
    # Folder exists #
    #################

    # If folder already exist
    else :
        
        folderId = Folder_research[0]['id']
        print folderId
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

    for element in glob.glob(path) :
            os.remove(element)

    Logger.logout(SID)

    context = {"birthcertificate":birthcertificate,
               "path":path,
               "folderId" : folderId,
              }
                   
    return render(request, 'BC_PDF.html', context)