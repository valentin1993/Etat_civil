#-*- coding: utf-8 -*-

import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from models import Person, CountryField
from BirthCertificate.models import BirthCertificate
from forms import PersonForm, PersonForm2
from django.views.generic.edit import UpdateView
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa

import Logger, Search, Folds, Docs, Buffer, EnterSearch

from chartit import DataPool, Chart

from django.db.models import Count
from django_countries import countries

import time
from random import randint
from django.contrib import messages 

import Global_variables



@login_required
def Identity_Home(request) :
    
    return render(request, 'Identity_home.html')

def Chartview(request) :

    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Person.objects.values('city').annotate(nombre = Count('city'))},
              'terms': [
                'city',
                'nombre']}
             ])
 
    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':{
                  'city': [
                    'nombre']
                  }}],
            chart_options =
              {'title': {
                   'text': "Nombre d'habitants par ville"},
                'xAxis': {
                    'title': {
                       'text': 'Villes'}}})


    ds = \
        DataPool(
           series=
            [{'options': {
               'source': Person.objects.values('birthcountry').annotate(nombre = Count('birthcountry'))},
              'terms': [
                'birthcountry',
                'nombre']}
             ])
 
    #Step 2: Create the Chart object
    cht2 = Chart(
            datasource = ds,
            series_options =
              [{'options':{
                  'type': 'column',
                  'stacking': False},
                'terms':{
                  'birthcountry': [
                    'nombre']
                  }}],
            chart_options =
              {'title': {
                   'text': "Visualisation globale des Pays de Naissance"},
                'xAxis': {
                    'title': {
                       'text': 'Pays de Naissance'}}})


    ds2 = \
        DataPool(
           series=
            [{'options': {
               'source': Person.objects.values('sex').annotate(nombre = Count('sex'))},
              'terms': [
                'sex',
                'nombre']}
             ])
 
    #Step 2: Create the Chart object
    cht3 = Chart(
            datasource = ds2,
            series_options =
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                  'sex': [
                    'nombre']
                  }}],
            chart_options =
              {'title': {
                   'text': "Proportion Homme/Femme"},
                'xAxis': {
                    'title': {
                       'text': 'Sexe'}}})

    return render(request, 'statistics.html', {'charts': [cht, cht2, cht3],})

@login_required
def Identity_Form(request) :
    
    success = False

    if request.method == 'POST':

        form = PersonForm(request.POST or None)

        if form.is_valid() :   # Vérification sur la validité des données
            post = form.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('treated', kwargs={'id': post.id}))

        else:
            messages.error(request, "Le formulaire est invalide !")
    
    else:
        form = PersonForm()

    return render(request, 'form_Identity.html', {"form" : form})

@login_required
def Identity_Form_unique_number(request) :
    
    validity = []
    submission = []
    #User fill some fields
    query_social_number = request.GET.get('social_number')

    success = False
    
    if request.method == 'POST':
            
        form = PersonForm2(request.POST or None)

        if form.is_valid() :   # Vérification sur la validité des données
            post = form.save()
            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('treated2', kwargs={'id': post.id}))
            
        else:
            messages.error(request, "Le formulaire est invalide !")

    elif request.method == 'GET':
        
        form = PersonForm2()

        if query_social_number :
            if BirthCertificate.objects.filter(social_number = query_social_number).exists() == True :
                
                individu = get_object_or_404(BirthCertificate, social_number = query_social_number)
                messages.success(request, 'Le numéro unique existe !')

                form.fields['lastname'].initial = individu.lastname
                form.fields['firstname'].initial = individu.firstname
                form.fields['birthday'].initial = individu.birthday
                form.fields['birthcity'].initial = individu.birthcity
                form.fields['birthcountry'].initial = individu.birthcountry
                form.fields['sex'].initial = individu.sex
                form.fields['social_number'].initial = individu.social_number

            elif BirthCertificate.objects.filter(social_number = query_social_number).exists() == False :
                
                validity = False
                messages.error(request, "Le numéro unique est invalide !")
                
 
    context = {
        "form" : form,
        "validity" : validity,
        "submission" : submission
        
    }

    return render(request, 'form_Identity2.html', context)

@login_required
def Identity_Resume_unique_number(request, id) :
    
    person = get_object_or_404(Person, pk=id)

    context = {
            "person" : person,
    }

    return render(request, 'identity_resume2.html', context)

@login_required
def Identity_Resume(request, id) :
    
    person = get_object_or_404(Person, pk=id)

    obj = BirthCertificate.objects.filter(firstname=person.firstname, lastname=person.lastname, birthday=person.birthday, birthcity=person.birthcity)

    if obj:
        sc_obj = obj[0] #check if multiple objects are there, means obj[1]
        person.social_number = sc_obj.social_number
        person.save()

    else :

        #Homme = 1 / Femme = 2
        sex_number = []
        if person.sex == 'Masculin' :
            sex_number = 1
            print sex_number
        else :
            sex_number = 2
            print sex_number

        #Récupère année de naissance
        birthyear_temp = str(person.birthday.year)
        birthyear_temp2 = str(birthyear_temp.split(" "))
        birthyear = birthyear_temp2[4] + birthyear_temp2[5]

        #Récupère mois de naissance
        birthmonth_temp = person.birthday.month
        if len(str(birthmonth_temp)) == 1 :
            birthmonth = '0' + str(birthmonth_temp)
        else :
            birthmonth = birthmonth_temp

        #Récupère N° Mairie (ici récupère nom mais sera changé en n°)
        birth_mairie = person.birthmairie
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
        person.social_number = social_number
        person.save()

    context = {
                "person" : person,
                "social_number" :social_number,
    }

    return render(request, 'identity_resume.html', context)

@login_required
def Identity_Researching(request) :
    
    folderId = None
    success = False
    error = False
    
    #######################
    # Display some arrays #
    #######################

    persons = Person.objects.order_by("-id")
    person = persons[:3] #The 3 last created forms
    person_France = persons.filter(country=64)[:3] #The 3 last created form with BirthCity = France

    ##########################
    # People searching n° ID #
    ##########################

    query_lastname_ID = request.GET.get('q1ID')
    query_firstname_ID = request.GET.get('q1bisID')

    if query_firstname_ID and query_lastname_ID :
        
        query_ID_list = Person.objects.filter(lastname__iexact=query_lastname_ID, firstname__iexact=query_firstname_ID)
        if len(query_ID_list) != 0 :
            messages.success(request, 'Miracle .. Vous avez un résultat !')
        else :
            messages.error(request, "Oh non .. Vous n'avez aucun résultat !")
        

    elif query_firstname_ID :
        
        query_ID_list = Person.objects.filter(lastname__iexact=query_firstname_ID)
        if len(query_ID_list) != 0 :
            messages.success(request, 'Miracle .. Vous avez un résultat !')
        else :
            messages.error(request, "Oh non .. Vous n'avez aucun résultat !")

    elif query_lastname_ID :
        
        query_ID_list = Person.objects.filter(lastname__iexact=query_lastname_ID)
        if len(query_ID_list) != 0 :
            messages.success(request, 'Miracle .. Vous avez un résultat !')
        else :
            messages.error(request, "Oh non .. Vous n'avez aucun résultat !")

    else :
        query_ID_list = Person.objects.none() # == []



    ##############################################
    # People searching process in DatasystemsDOC #
    ##############################################

    query_lastname = request.GET.get('q1')
    query_firstname = request.GET.get('q1bis')
    query_social_number = request.GET.get('q1social')

    if query_lastname and query_firstname and query_social_number:
        
        query_lastname_list = Person.objects.filter(lastname__iexact=query_lastname, firstname__iexact=query_firstname, social_number__iexact=query_social_number) 

        social_number2 = query_social_number.replace(" ", "")
        title = str(query_lastname + "_" + query_firstname + "_" + social_number2)


        ##########################################
        # Look if people directory already exist #
        ##########################################

        url = Global_variables.GED_url.url + '/services/rest/folder/listChildren?folderId=8552450'
        payload = {'folderId': 8552450}

        headers = {'Accept': 'application/json'}
        r = requests.get(url,  params=payload, headers=headers, auth=('etatcivil', '100%EC67'))

        rbody = r.content
        data = json.loads(rbody)

        longueur = len(data)

        i=0
        list = []

        while i < longueur :
            
            if data[i]["name"] == title :
                
                list = [data[i]]

            i = i+1

        ############################################
        # We have correspondance, use ID directory #
        ############################################

        if len(list) == 1 :
            
            folderId = list[0]["id"]

        else : 

            return HttpResponseRedirect(reverse('searched'))

    else :
        query_lastname_list = Person.objects.none() # == []

        # messages.error(request, "Individu non trouvé et/ou formulaire invalide !")


    context = {
        "person" : person,
        "query_lastname_ID" : query_lastname_ID,
        "query_firstname_ID": query_firstname_ID,
        "query_ID_list" : query_ID_list,
        # "social_number2" : social_number2,
        "person_France" : person_France,
        "query_lastname" : query_lastname,
        # "query_lastname2" : query_lastname2,
        "query_firstname" : query_firstname,
        # "query_firstname2" : query_firstname2,
        "query_social_number" : query_social_number,
        "query_lastname_list" : query_lastname_list,
        "folderId" : folderId,
        }
   
    return render(request, 'resume.html', context)

@login_required
def Identity_Update(request) :
    
    
    # Partie qui recherche une fiche par nom
    query_lastname = request.GET.get('q4')
    query_firstname = request.GET.get('q4bis')
    query_birthday = request.GET.get('q4ter')
    if query_lastname and query_firstname and query_birthday :
        query_lastname_list = Person.objects.filter(lastname__icontains=query_lastname, firstname__icontains=query_firstname, birthday__iexact=query_birthday)    
    else :
        query_lastname_list = Person.objects.none() # == []


    form = PersonForm(request.POST or None, instance = query_lastname_list.first())

    if form.is_valid():
        if 'save' in request.POST :
            post = form.save()
            return HttpResponseRedirect(reverse('home'))

    if "Retour" in request.POST :
        return HttpResponseRedirect(reverse('accueil'))
    
    template_name = 'edit.html'

    context = {
        "query_lastname" : query_lastname,
        "query_firstname" : query_firstname,
        "query_birthday" : query_birthday,
        "query_lastname_list" : query_lastname_list,
        "form": form
    }
    return render(request, template_name, context)

@login_required
def Identity_Deleting(request) :
    
    # Partie qui recherche une fiche par nom
    query_lastname = request.GET.get('q6')
    query_firstname = request.GET.get('q6bis')
    query_birthday = request.GET.get('q6ter')
    
    if query_lastname and query_firstname and query_birthday :
        query_lastname_list = Person.objects.filter(lastname__icontains=query_lastname, firstname__icontains=query_firstname, birthday__iexact=query_birthday)    
    else :
        query_lastname_list = Person.objects.none() # == []

    form = PersonForm(request.POST or None, instance = query_lastname_list.first())
    
    if "Supprimer" in request.POST :
        form = Person.objects.filter(pk=query_lastname_list).delete()
        return HttpResponseRedirect(reverse('home'))
    
    template_name = 'delete.html'

    context = {
        "query_lastname" : query_lastname,
        "query_firstname" : query_firstname,
        "query_birthday" : query_birthday,
        "query_lastname_list" : query_lastname_list,
        "form":form
    }
    return render(request, template_name, context)

@login_required
def Identity_PDF(request, id) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID

    folderId = None

    person = get_object_or_404(Person, pk=id)

    data = {"person" :person}

    template = get_template('Identity_raw.html') # A modifier : template pdf généré
    html  = template.render(Context(data))

    social_number = str(Person.objects.get(pk=id).social_number.encode('utf-8'))
    social_number_2 = social_number.replace(" ", "")

    filename_directory = str(Person.objects.get(pk=id).lastname.encode('utf-8')) + "_" + str(Person.objects.get(pk=id).firstname.encode('utf-8')) + "_" + social_number_2
    filename_init = 'Fiche_Individuelle_' + filename_directory 
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

        print Create_Folds

        folderId = Create_Folds['id']

        print "dossier créé :" + str(folderId)

        # Create document inside the new folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = folderId )
        print "document ajouté dans dossier créé"


    #################
    # Folder exists #
    #################

    # If folder already exist
    else :
        
        folderId = Folder_research[0]['id']
        print folderId
        
        print "dossier existe déjà : " + str(folderId)
        
        # Search if document already exist inside by comparing expression
        # Search_Docs = Search.find(SID, expression = filename_init, folderId = Folder_research[0]['id'])
        Search_Docs = EnterSearch.find_parameters(SID, title=filename_init)

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
            print Create_Docs

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

    context = {"person":person,
               "path":path,
               "folderId":folderId,
    }
                   

    return render(request, 'Identity_PDF.html', context) # Template page générée après PDF
