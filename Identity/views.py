#-*- coding: utf-8 -*-

#Import from Project file 
from models import Individu, CountryField
from forms import *
from Informations import *
from DatasystemsCORE import settings
import Ville
import Global_variables
import Individu_Recherche 
import Logger, Search, Folds, Docs, Buffer

#Import from Django
from django.shortcuts import render, reverse, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.template.loader import get_template
from django.template import Context
from django.db.models import Count
from django_countries import countries
from django.contrib import messages 


#Import from others lib
import requests, os, json, glob
from xhtml2pdf import pisa
import re 
from chartit import DataPool, Chart
import time, datetime
from random import randint
import cStringIO as StringIO
from cgi import escape


###################################################################################################################################################################################################

def link_callback(uri, rel):
    if uri.find('chart.apis.google.com') != -1:
        return uri
    return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

###################################################################################################################################################################################################

@login_required
def Identity_Choice(request) :

    return render(request, 'Identity_Choice.html')

###################################################################################################################################################################################################

@login_required
def Identity_Home(request) :
    
    return render(request, 'Identity_home.html')

###################################################################################################################################################################################################

@login_required
def Chartview(request) :

    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Individu.objects.values('Ville').annotate(nombre = Count('Ville'))},
              'terms': [
                'Ville',
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
                  'Ville': [
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
               'source': Individu.objects.values('PaysNaissance').annotate(nombre = Count('PaysNaissance'))},
              'terms': [
                'PaysNaissance',
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
                  'PaysNaissance': [
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
               'source': Individu.objects.values('Sexe').annotate(nombre = Count('Sexe'))},
              'terms': [
                'Sexe',
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
                  'Sexe': [
                    'nombre']
                  }}],
            chart_options =
              {'title': {
                   'text': "Proportion Homme/Femme"},
                'xAxis': {
                    'title': {
                       'text': 'Sexe'}}})

    return render(request, 'Identity_Statistics.html', {'charts': [cht, cht2, cht3],})

###################################################################################################################################################################################################

@login_required
def Identity_Individu_Form(request) :

    #################################################################
    #               Initialisation des variables                    #
    success = False
    query_Nom_ID = query_Prenom_ID = query_VilleNaissance_ID = None
    #################################################################


    if 'recherche' in request.GET:
        
        query_Nom_ID = request.GET.get('q1NomID')
        query_Prenom_ID = request.GET.get('q1PrenomID')
        query_VilleNaissance_ID = request.GET.get('q1VilleNaissanceID')

        sort_params = {}

        Individu_Recherche.set_if_not_none(sort_params, 'Nom__icontains', query_Nom_ID)
        Individu_Recherche.set_if_not_none(sort_params, 'Prenom__icontains', query_Prenom_ID)
        Individu_Recherche.set_if_not_none(sort_params, 'VilleNaissance__icontains', query_VilleNaissance_ID)

        query_ID_list = Individu.objects.filter(**sort_params) 


    else :
        query_ID_list = Individu.objects.none()


    if request.method == 'POST':

        form = IndividuFormulaire(request.POST or None, request.FILES or None)

        if form.is_valid() :
            post = form.save(commit=False)
            for element in settings.BDD :
                post.save(using=element, force_insert=True)

            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('IndividuResume', kwargs={'id': post.id}))

        else:
            messages.error(request, "Le formulaire est invalide !")
        
    else :
        form = IndividuFormulaire()
        form.fields['Utilisateur'].initial = request.user.last_name + " " + request.user.first_name

    context = {
        "form" : form,
        "Individu" : Individu,
        "query_Nom_ID" : query_Nom_ID,
        "query_Prenom_ID" : query_Prenom_ID,
        "query_VilleNaissance_ID" : query_VilleNaissance_ID,
        "query_ID_list" : query_ID_list,
    }

    return render(request, 'Identity_Individu_Form.html', context)

###################################################################################################################################################################################################


@login_required
def Identity_Societe_Form(request) :
    
    query_Responsable = request.GET.get('Responsable')
    
    success = False

    if request.method == 'POST':

        form = SocieteFormulaire(request.POST or None)

        if form.is_valid() :   # Vérification sur la validité des données
            post = form.save(commit=False)
            for element in settings.BDD :
                post.save(using=element, force_insert=True)

            messages.success(request, 'Le formulaire a été enregistré !')
            return HttpResponseRedirect(reverse('SocieteResume', kwargs={'id': post.id}))

        else:
            messages.error(request, "Le formulaire est invalide !")
    
    else:
        form = SocieteFormulaire()

        Responsable = Individu.objects.filter(NumeroIdentification=query_Responsable)
        form.fields['Responsable'].queryset = Responsable
        form.fields['Utilisateur'].initial = request.user.last_name + " " + request.user.first_name

    return render(request, 'Identity_Societe_Form.html', {"form" : form, "query_Responsable" : query_Responsable})

###################################################################################################################################################################################################

@login_required
def Identity_Individu_Resume(request, id) :
    
    personne = get_object_or_404(Individu, pk=id)

    obj = Individu.objects.filter (
                                        Prenom=personne.Prenom, 
                                        Nom=personne.Nom, 
                                        DateNaissance=personne.DateNaissance, 
                                        VilleNaissance=personne.VilleNaissance
                                        )

    if obj:
        sc_obj = obj[0] #check if multiple objects are there, means obj[1]
        
        #Homme = 1 / Femme = 2
        sex_number = []
        if personne.Sexe == 'Masculin' :
            sex_number = 1
        else :
            sex_number = 2

        #Récupère année de naissance
        birthyear_temp = str(personne.DateNaissance.year)
        birthyear_temp2 = str(birthyear_temp.split(" "))
        birthyear = birthyear_temp2[4] + birthyear_temp2[5]

        #Récupère mois de naissance
        birthmonth_temp = personne.DateNaissance.month
        if len(str(birthmonth_temp)) == 1 :
            birthmonth = '0' + str(birthmonth_temp)
        else :
            birthmonth = birthmonth_temp

        #Récupère N° Ville de Naissance
        birth_city = Ville.Villes[personne.VilleNaissance]
        print birth_city

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

        birth_country = personne.PaysNaissance
        birth_country_id = None
        print birth_country
        if birth_country == "CM" :
            birth_country_id = 1
        else :
            birth_country_id = 2


        NumeroIdentification = str(sex_number) + str(birthyear) + str(birthmonth) + '-' + str(birth_city) + '-' + str(key) + '-' + str(birth_country_id)

        #Mise à jour du champ numéro sécurité social
        personne.NumeroIdentification = NumeroIdentification

        if personne.Image != "" :
            NewImageName = 'pictures/' + str(personne.Nom) +'_'+ str(personne.Prenom) +'_'+  NumeroIdentification + '.jpg'
            print NewImageName

            FilePath = settings.MEDIA_ROOT # /Media
            print FilePath
            FilePathOLD = settings.MEDIA_ROOT + str(personne.Image)
            print FilePathOLD
            FilePathNEW = settings.MEDIA_ROOT + NewImageName
            print FilePathNEW

            file = os.path.exists(FilePath)
            if file :
                os.rename(FilePathOLD, FilePathNEW)

            personne.Image = NewImageName


        if personne.CarteIdentite != "" :
            NewCarteName = 'Carte_Identite/' + 'Carte_Identite_' + str(personne.Nom) +'_'+ str(personne.Prenom) +'_'+  NumeroIdentification + '.jpg'
            print NewCarteName

            FilePath = settings.MEDIA_ROOT 
            print FilePath
            FilePathOLD = settings.MEDIA_ROOT + str(personne.CarteIdentite)
            print FilePathOLD
            FilePathNEW = settings.MEDIA_ROOT + NewCarteName
            print FilePathNEW

            file = os.path.exists(FilePath)
            if file :
                os.rename(FilePathOLD, FilePathNEW)

            personne.CarteIdentite = NewCarteName
        

        else :
            pass

        for element in settings.BDD :
            personne.save(using=element)

    context = {
                "personne" : personne,
                "NumeroIdentification" : NumeroIdentification,
    }

    return render(request, 'Identity_Individu_Resume.html', context)

###################################################################################################################################################################################################

@login_required
def Identity_Societe_Resume(request, id) :
        
    societe = get_object_or_404(Societe, pk=id)

    context = {
            "societe" : societe,
    }

    return render(request, 'Identity_Societe_Resume.html', context)


###################################################################################################################################################################################################


@login_required
def Identity_Individu_Researching(request) :


    folderId = None
    success = False
    error = False
    recherche = None
        
        #######################
        # Display some arrays #
        #######################
    
    persons = Individu_Recherche.Recherche_Order(Individu, "-id")
    person_France = persons.filter(Pays=64)
    
   
        #############################################
        # People searching n° Numero Identification #
        #############################################

    if 'recherche' in request.GET:
    
        query_lastname_ID = request.GET.get('q1ID')
        query_firstname_ID = request.GET.get('q1bisID')
        query_naissance_ID = request.GET.get('q1terID')

        sort_params = {}

        Individu_Recherche.set_if_not_none(sort_params, 'Nom__icontains', query_lastname_ID)
        Individu_Recherche.set_if_not_none(sort_params, 'Prenom__icontains', query_firstname_ID)
        Individu_Recherche.set_if_not_none(sort_params, 'VilleNaissance__icontains', query_naissance_ID)

        query_ID_list = Individu_Recherche.Recherche_Filter(Individu, sort_params)

        context = {
            "query_lastname_ID" : query_lastname_ID,
            "query_firstname_ID": query_firstname_ID,
            "query_ID_list" : query_ID_list,
            "query_naissance_ID" : query_naissance_ID,
            }

        return render(request, 'Identity_Individu_Recherche.html', context)



        ##############################################
        # People searching process in DatasystemsDOC #
        ##############################################

    query_lastname = request.GET.get('q1')
    query_firstname = request.GET.get('q1bis')
    query_social_number = request.GET.get('q1social')

    if query_lastname and query_firstname and query_social_number:
            
        query_lastname_list = Individu.objects.filter(Nom__iexact=query_lastname, Prenom__iexact=query_firstname, NumeroIdentification__iexact=query_social_number) 

        social_number2 = query_social_number.replace(" ", "")
        title = str(query_lastname + "_" + query_firstname + "_" + social_number2)


    ##########################################
    # Look if people directory already exist #
    ##########################################

        url = Global_variables.GED_url.url + '/services/rest/folder/listChildren?folderId=11304975'
        payload = {'folderId': 11304975}

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
            return HttpResponseRedirect(reverse('Recherche'))

    else :
        query_lastname_list = Individu.objects.none() # == []


    context = {
        "persons" : persons,
        "person" : persons[:3],
        #"query_lastname_ID" : query_lastname_ID,
        #"query_firstname_ID": query_firstname_ID,
        #"query_ID_list" : query_ID_list,
        #"query_naissance_ID" : query_naissance_ID,
        "person_France" : person_France,
        "query_lastname" : query_lastname,
        "query_firstname" : query_firstname,
       # "query_firstname2" : query_firstname2,
        "query_social_number" : query_social_number,
        "query_lastname_list" : query_lastname_list,
        "folderId" : folderId,
        }
   
    return render(request, 'Identity_Individu_Recherche.html', context)

###################################################################################################################################################################################################

@login_required
def Identity_Societe_Researching(request) :
    
    folderId = None
    success = False
    error = False
    
    #######################
    # Display some arrays #
    #######################

    societe = Societe.objects.order_by("-id")
    societes = societe[:3] #The 3 last created forms
    societe_France = societe.filter(Pays=64)[:3] #The 3 last created form with BirthCity = France

    ##########################
    # People searching SIRET #
    ##########################

    query_name_ID = request.GET.get('q1ID')
    query_ville_ID = request.GET.get('q1bisID')

    if query_name_ID and query_ville_ID :
        
        query_ID_list = Societe.objects.filter(
                                                Nom__icontains=query_name_ID, 
                                                Ville__icontains=query_ville_ID)
        if len(query_ID_list) != 0 :
            messages.success(request, 'Miracle .. Vous avez un résultat !')
        else :
            messages.error(request, "Oh non .. Vous n'avez aucun résultat !")

    elif query_name_ID or query_ville_ID :
        
        query_ID_list = Societe.objects.filter(
                                                Nom__icontains=query_lastname_ID, 
                                                Ville__icontains=query_firstname_ID)
        if len(query_ID_list) != 0 :
            messages.success(request, 'Miracle .. Vous avez un résultat !')
        else :
            messages.error(request, "Oh non .. Vous n'avez aucun résultat !")

    else :
        query_ID_list = Societe.objects.none() # == []

    ##############################################
    # People searching process in DatasystemsDOC #
    ##############################################

    query_name = request.GET.get('q1')
    query_SIRET = request.GET.get('q1bis')

    if query_name and query_SIRET :
        
        query_societe_list = Societe.objects.filter(Nom__iexact=query_name, SIRET__iexact=query_SIRET) 
        #print query_societe_list
        #query_societe_list = get_object_or_404(Societe, SIRET=query_SIRET)
        #print query_societe_list

        #query_societe_list2 = Societe.objects.filter(Nom__icontains=query_name, SIRET__iexact=query_SIRET)


        # social_number2 = query_social_number.replace(" ", "")
        title = str(query_name + "_" + query_SIRET)


        ##########################################
        # Look if people directory already exist #
        ##########################################

        url = Global_variables.GED_url.url + '/services/rest/folder/listChildren?folderId=11304976'
        payload = {'folderId': 11304976}

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
            return HttpResponseRedirect(reverse('SocieteRecherche'))

    else :
        query_societe_list = Societe.objects.none() # == []
        #query_societe_list2 = Societe.objects.none()


    context = {
        "societe" : societe,
        "query_name_ID" : query_name_ID,
        "query_ville_ID": query_ville_ID,
        "query_ID_list" : query_ID_list,
        "query_SIRET" : query_SIRET,
        "societe_France" : societe_France,
        "query_name" : query_name,
        "query_societe_list" : query_societe_list,
        #"query_societe_list2" : query_societe_list2,
        "folderId" : folderId,
        }
   
    return render(request, 'Identity_Societe_Recherche.html', context)

###################################################################################################################################################################################################

@login_required
def Identity_Societe_Recherche_Fraude(request) :
    
    query_Individu = None

    query_NumeroIdentification = request.GET.get('q1ID')
    NombreSociete = None

    if query_NumeroIdentification :
            
        query_ID_list = Societe.objects.filter(Responsable=query_NumeroIdentification)
        try :
            query_Individu = Individu.objects.get(NumeroIdentification=query_NumeroIdentification)

        except Individu.DoesNotExist :
            HttpResponseRedirect(reverse('SocieteRechercheFraude'))

        NombreSociete = Societe.objects.filter(Responsable=query_NumeroIdentification).count()
            
        if len(query_ID_list) != 0 :
            messages.success(request, 'Miracle .. Vous avez un résultat !')
        else :
            messages.error(request, "Oh non .. Vous n'avez aucun résultat !")

    else :
        query_ID_list = Societe.objects.none() # == []


    context = {
        "query_NumeroIdentification": query_NumeroIdentification,
        "query_ID_list" : query_ID_list,
        "NombreSociete" : NombreSociete,
        "query_Individu" : query_Individu,
        }

    return render(request, 'Identity_Societe_Recherche_Fraude.html', context)

###################################################################################################################################################################################################

@login_required
def Identity_Consultation_PDF(request) :
    
    query_id_ID = request.GET.get('q1idID')

    if query_id_ID :

        personne = get_object_or_404(Individu, pk = query_id_ID )

        institution = InformationsInstitution.objects.last()

        data = {"personne" :personne, "institution" : institution}

        template = get_template('Identity_Individu_Consultation_raw.html') # A modifier : template pdf généré
        html  = template.render(Context(data))
        result = StringIO.StringIO()

        filename = str(personne.Nom) +  "_" + str(personne.Prenom) +  "_" + str(personne.NumeroIdentification)

        path = Global_variables.Individu_path.path + filename + ".pdf"

        with open(path, "w+b") as file :
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), file, link_callback=link_callback)
        file.close()

        image_data = open(path, "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")

    context = {
        "query_id_ID" : query_id_ID,
    }

    return render(request, 'Identity_Consultation_PDF.html', context)

###################################################################################################################################################################################################

@login_required
def Identity_Societe_Consultation_PDF(request) :
    
    query_SIRET = request.GET.get('q1idID')

    if query_SIRET :

        societe = get_object_or_404(Societe, SIRET = query_SIRET )

        institution = InformationsInstitution.objects.last()

        data = {"societe" : societe, "institution" : institution}

        template = get_template('Identity_Societe_Consultation_raw.html') # A modifier : template pdf généré
        html  = template.render(Context(data))
        result = StringIO.StringIO()

        filename = str(Societe.Nom) +  "_" + str(Societe.SIRET) 

        path = Global_variables.Societe_path.path + filename + ".pdf"

        with open(path, "w+b") as file :
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), file, link_callback=link_callback)
        file.close()

        image_data = open(path, "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")

    context = {
        "query_SIRET" : query_SIRET,
    }

    return render(request, 'Identity_Societe_Consultation_PDF.html', context)

###################################################################################################################################################################################################

@login_required
def Identity_Update(request) :
    
    # Partie qui recherche une fiche par nom
    query_numero = request.GET.get('q4')

    if query_numero:
        query_numero_list = Individu.objects.filter(NumeroIdentification__iexact=query_numero)    
    else :
        query_numero_list = Individu.objects.none() # == []


    form = IndividuFormulaire(request.POST or None, instance = query_numero_list.first())

    if form.is_valid() :
        if 'save' in request.POST :
            post = form.save(commit=False)
            for element in settings.BDD :
                post.save(using=element)
            return HttpResponseRedirect(reverse('Home'))

    if "Retour" in request.POST :
        return HttpResponseRedirect(reverse('accueil'))
    
    template_name = 'Identity_Edition.html'

    context = {
        "query_numero" : query_numero,
        "form": form
    }
    return render(request, template_name, context)

###################################################################################################################################################################################################

@login_required 
def Identity_Deleting(request) : 

    query_number = request.GET.get('q6') 

    if query_number : 
        query_number_list = Individu.objects.filter(NumeroIdentification__iexact=query_number) 
    else : 
        query_number_list = Individu.objects.none() 

    instance = query_number_list.first() 
    form = IndividuFormulaire(request.POST or None, instance = query_number_list.first()) 

    if "Supprimer" in request.POST : 
        id_to_delete = list(query_number_list.values_list('id', flat=True)) 
        for element in settings.BDD : 
            form = Individu.objects.using(element).filter(pk__in=id_to_delete).delete() 

        return HttpResponseRedirect(reverse('Home'))
    
    template_name = 'Identity_Suppression.html'

    context = {
        "query_number" : query_number,
        "form":form
    }
    return render(request, template_name, context)

###################################################################################################################################################################################################

@login_required
def Identity_Individu_PDF(request, id) :
    
    SID = Logger.login("etatcivil", "100%EC67")

    folderId = None

    personne = get_object_or_404(Individu, pk=id)
    institution = get_object_or_404(InformationsInstitution)

    data = {"personne" :personne, "institution":institution}

    template = get_template('Identity_Individu_raw.html') # A modifier : template pdf généré
    html  = template.render(Context(data))
    result = StringIO.StringIO()

    NumeroIdentification = str(Individu.objects.get(pk=id).NumeroIdentification.encode('utf-8'))
    NumeroIdentification_2 = NumeroIdentification.replace(" ", "")

    filename_directory = str(Individu.objects.get(pk=id).Nom.encode('utf-8')) + "_" + str(Individu.objects.get(pk=id).Prenom.encode('utf-8')) + "_" + NumeroIdentification_2
    filename_init = 'Fiche_Identification_' + filename_directory 
    filename = filename_init + '.pdf'

    filename_Image_init = filename_directory + '.jpg'
    filename_Image = 'Photo_Identité_' + filename_directory + '.jpg'

    filename_CarteIdentite_init = filename_directory + '.jpg'
    filename_CarteIdentite = 'Carte_Identite_' + filename_directory + '.jpg'
    
    path = Global_variables.Individu_path.path + filename
    path_Image = Global_variables.Individu_Image_path.path + filename_Image_init
    path_CarteIdentite = Global_variables.Individu_CarteIdentite_path.path + filename_CarteIdentite


    file = open(path, "w+b")
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), file, link_callback=link_callback)
    file.close()
    print " "

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
        
        print "Le dossier " + filename_directory + " n'existe pas"
        
        # Create Folder in "Individus" Folder
        Create_Folds = Folds.create(SID, name = filename_directory, parentId = 11304975)

        folderId = Create_Folds['id']
        
        print "Le dossier " + filename_directory + " a été créé avec le n° " + str(folderId)
        print " "
        # Create document inside the new folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = folderId )
        Create_Docs_Image = Docs.create(path_Image, SID, fileName = filename_Image, folderId = folderId )
        Create_Docs_CarteIdentite = Docs.create(path_CarteIdentite, SID, fileName = filename_CarteIdentite, folderId = folderId )
        print "Les documents ajoutés dans dossier " + filename_directory + " sont : " + filename + " + " + filename_Image  + " + " + filename_CarteIdentite
        print " "

    #################
    # Folder exists #
    #################

    # If folder already exist
    else :
        
        folderId = Folder_research[0]['id']
        
        print "Le dossier " + filename_directory + " existe déjà sous le n° : " + str(folderId)
        print " "
        Search_Docs = Search.find_doc(SID, filename = filename)
        Search_Docs_Image = Search.find_doc(SID, filename = filename_Image)
        Search_Docs_CarteIdentite = Search.find_doc(SID, filename = filename_CarteIdentite)

        print "Recherche des occurences de documents : " 
        print "     - " + filename 
        print "     - " + filename_Image
        print "     - " + filename_CarteIdentite
        print " "
        #Search_Docs_ID = Search_Docs['hits'][0]['id']
        #print Search_Docs_ID

            ############################
            # Folder exists but no doc #
            ############################

        # If folder exists but not document
        if len(Search_Docs) == 0 :
            
            print "Nombre de document dans la liste : " + str(len(Search_Docs))
            
            # Create document inside the good folder
            Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Folder_research[0]['id'])
            print "Le document " + filename + " a été ajouté dans le dossier " + filename_directory
            print " "
            #############################
            # Folder exists and doc too #
            #############################

        else :
            
            print "Nombre d'occurence trouvée pour " + filename + " : " + str(len(Search_Docs))
            
            Search_Docs_ID = Search_Docs[0]['id']

            # Update the document in the good folder
            Upload_Docs = Docs.upload(path, SID, Search_Docs_ID, filename)
            print "Le document " + filename + " a été mis à jour dans le dossier " + filename_directory
            print " "


        if len(Search_Docs_Image) == 0 :
            
            print "nombre d'élément dans la liste : " + str(len(Search_Docs_Image))
            
            # Create document inside the good folder
            Create_Docs_Image = Docs.create(path_Image, SID, fileName = filename_Image, folderId = Folder_research[0]['id'])
            print "Le document " + filename_Image + " a été ajouté dans le dossier " + filename_directory
            print " "
            #############################
            # Folder exists and doc too #
            #############################

        else :
            
            print "Nombre d'occurence trouvée pour " + filename_Image + " : " + str(len(Search_Docs_Image))
            
            Search_Docs_ID_Image = Search_Docs_Image[0]['id']

            # Update the document in the good folder
            Upload_Docs_Image = Docs.upload(path_Image, SID, Search_Docs_ID_Image, filename_Image)
            print "Le document " + filename_Image + " a été mis à jour dans le dossier " + filename_directory
            print " "

        if len(Search_Docs_CarteIdentite) == 0 :
            
            print "nombre d'élément dans la liste : " + str(len(Search_Docs_CarteIdentite))
            
            # Create document inside the good folder
            Create_Docs_CarteIdentite = Docs.create(path_CarteIdentite, SID, fileName = filename_CarteIdentite, folderId = Folder_research[0]['id'])
            print "Le document " + filename_CarteIdentite + " a été ajouté dans le dossier " + filename_directory
            print " "
            #############################
            # Folder exists and doc too #
            #############################

        else :
            
            print "Nombre d'occurence trouvée pour " + filename_CarteIdentite + " : " + str(len(Search_Docs_CarteIdentite))
            
            Search_Docs_ID_CarteIdentite = Search_Docs_CarteIdentite[0]['id']

            # Update the document in the good folder
            Upload_Docs_CarteIdentite = Docs.upload(path_CarteIdentite, SID, Search_Docs_ID_CarteIdentite, filename_CarteIdentite)
            print "Le document " + filename_CarteIdentite + " a été mis à jour dans le dossier " + filename_directory
            print " "

    for element in glob.glob(path) :
            os.remove(element)


    Logger.logout(SID)

    context = {"personne":personne,
               "path":path,
               "folderId":folderId,
               "settings.MEDIA_ROOT" : settings.MEDIA_ROOT
    }
                   

    return render(request, 'Identity_Individu_PDF.html', context) # Template page générée après PDF


###################################################################################################################################################################################################


@login_required
def Identity_Societe_PDF(request, id) :
    
    SID = Logger.login("etatcivil", "100%EC67")
    print SID

    folderId = None

    societe = get_object_or_404(Societe, pk=id)

    data = {"societe" :societe}

    template = get_template('Identity_Societe_raw.html') # A modifier : template pdf généré
    html  = template.render(Context(data))

    SIRET = str(Societe.objects.get(pk=id).SIRET)
    SIRET_2 = SIRET.replace(" ", "")

    Nom_temp = str(Societe.objects.get(pk=id).Nom.encode('utf-8'))
    Nom = Nom_temp.replace(" ","_")

    filename_directory = Nom + "_" + SIRET_2
    filename_init = 'Fiche_Identification_' + filename_directory 
    filename = filename_init + '.pdf'
    
    path = Global_variables.Societe_path.path + filename

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
        Create_Folds = Folds.create(SID, name = filename_directory, parentId = 11304976)

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
        # Search_Docs = EnterSearch.find_parameters(SID, title=filename_init)
        Search_Docs = Search.find_doc(SID, filename = filename)

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

    context = {"societe":societe,
               "path":path,
               "folderId":folderId,
    }
                   

    return render(request, 'Identity_Societe_PDF.html', context) # Template page générée après PDF


###################################################################################################################################################################################################


@login_required
def Identity_UpdateCivility(request):
    
    individu = "Non renseigné"
    form = None

    try :
    
        query_social_number = request.GET.get('social_number')
        
        if query_social_number :
            query_social_number_list = Individu.objects.filter(NumeroIdentification__iexact=query_social_number)
            individu = query_social_number_list[:1].get()
            
        else :
            query_social_number_list = Individu.objects.none() # == []

        form = IndividuFormCivility(request.POST or None, request.FILES or None, instance = query_social_number_list.first())
        
        form.fields['Utilisateur'].initial = request.user.last_name + " " + request.user.first_name

        if form.is_valid() :
            SID = Logger.login("etatcivil", "100%EC67")
            if 'save' in request.POST :

                if 'Image' in request.FILES:
                    form.Image = request.FILES['Image']

                    folderId = None

                    filename_directory = str(individu.Nom) + "_" + str(individu.Prenom) + "_" + str(individu.NumeroIdentification)

                    filename_Image_init = filename_directory + '.jpg'
                    filename_Image = u'Photo_Identité_' + filename_directory + '.jpg'
                    
                    if os.path.exists(Global_variables.Individu_Image_path.path + filename_Image_init) :
                        print filename_Image_init + ' existe'
                        delete_file = os.remove(Global_variables.Individu_Image_path.path + filename_Image_init)
                    
                    else :
                        print 'Le document ' + filename_Image_init + " n'existe pas"

                    path_Image = Global_variables.Individu_Image_path_RAW.path + filename_Image_init

                    Search_Docs_Image = Search.find_doc(SID, filename = filename_Image)

                    print "Recherche des occurences de documents : " 
                    print "     - " + filename_Image
                    print " "

                        ##################
                        # Folder exists  #
                        ##################

                        # If folder exists with document
                    if len(Search_Docs_Image) != 0 :
                            
                        print "Nombre d'occurence trouvee pour " + filename_Image + " : " + str(len(Search_Docs_Image))
                            
                        Search_Docs_ID_Image = Search_Docs_Image[0]['id']

                        # Update the document in the good folder
                        Upload_Docs_Image = Docs.upload(path_Image, SID, Search_Docs_ID_Image, filename_Image)
                        print "Le document " + filename_Image + u" a été mis à jour dans le dossier " + filename_directory
                        print " "

                        #step4 = time.clock()

                    else :
    
                        print "nombre d'élément dans la liste : " + str(len(Search_Docs_CarteIdentite))

                        Folder_research = Search.find_folder(SID, filename_directory)
            
                        # Create document inside the good folder
                        Create_Docs_CarteIdentite = Docs.create(path_CarteIdentite, SID, fileName = filename_CarteIdentite, folderId = Folder_research[0]['id'])
                        print "Le document " + filename_CarteIdentite + " a été ajouté dans le dossier " + filename_directory
                        print " "


                    for element in glob.glob(path_Image) :
                        os.remove(element)


                print "################################################"


                if 'CarteIdentite' in request.FILES:
                    form.CarteIdentite = request.FILES['CarteIdentite']

                    #SID = Logger.login("etatcivil", "100%EC67")

                    folderId = None

                    filename_directory = str(individu.Nom) + "_" + str(individu.Prenom) + "_" + str(individu.NumeroIdentification)

                    filename_CarteIdentite_init = filename_directory + '.jpg'
                    filename_CarteIdentite = 'Carte_Identite_' + filename_directory + '.jpg'

                    #print Global_variables.Individu_CarteIdentite_path.path + filename_CarteIdentite

                    #print Global_variables.Individu_CarteIdentite_path.path + filename_CarteIdentite
                    
                    if os.path.exists(Global_variables.Individu_CarteIdentite_path.path + filename_CarteIdentite) :
                        print filename_CarteIdentite + ' existe'
                        delete_file = os.remove(Global_variables.Individu_CarteIdentite_path.path + filename_CarteIdentite)
                    
                    else :
                        print 'Le document ' + filename_CarteIdentite + " n'existe pas"

                    path_CarteIdentite = Global_variables.Individu_CarteIdentite_path_RAW.path + filename_CarteIdentite

                    #Folder_research = Search.find_folder(SID, filename_directory)

                    #if Folder_research != [] :
                        
                        #folderId = Folder_research[0]['id']
            
                        #print "Le dossier " + filename_directory + u" existe déjà sous le n° : " + str(folderId)
                        #print " "
                    Search_Docs_CarteIdentite = Search.find_doc(SID, filename = filename_CarteIdentite)

                    print "Recherche des occurences de documents : " 
                    print "     - " + filename_CarteIdentite
                    print " "

                        ##################
                        # Folder exists  #
                        ##################

                        # If folder exists but not document
                    if len(Search_Docs_CarteIdentite) != 0 :
                            
                        print "Nombre d'occurence trouvee pour " + filename_CarteIdentite + " : " + str(len(Search_Docs_CarteIdentite))
                            
                        Search_Docs_ID_CarteIdentite = Search_Docs_CarteIdentite[0]['id']

                        # Update the document in the good folder
                        Upload_Docs_CarteIdentite = Docs.upload(path_CarteIdentite, SID, Search_Docs_ID_CarteIdentite, filename_CarteIdentite)
                        print "Le document " + filename_CarteIdentite + u" a été mis à jour dans le dossier " + filename_directory
                        print " "

                    else :

                        print "nombre d'élément dans la liste : " + str(len(Search_Docs_CarteIdentite))
            
                        Folder_research = Search.find_folder(SID, filename_directory)
                        # Create document inside the good folder
                        Create_Docs_CarteIdentite = Docs.create(path_CarteIdentite, SID, fileName = filename_CarteIdentite, folderId = Folder_research[0]['id'])
                        print "Le document " + filename_CarteIdentite + " a été ajouté dans le dossier " + filename_directory
                        print " "
                            

                            #Logger.logout(SID)

                    for element in glob.glob(path_CarteIdentite) :
                        os.remove(element)

                print "################################################"


                for element in settings.BDD :
                    post = form.save(commit=False)
                    post.save(using=element)

                return HttpResponseRedirect(reverse('Home'))
            Logger.logout(SID)
                
                
    except Individu.DoesNotExist :
            form = IndividuFormCivility()

    

    context = {
        "query_social_number" : query_social_number,
        "query_social_number_list" : query_social_number_list,
        "individu" : individu,
        "form": form
    }
    return render(request, "Identity_UpdateCivility.html", context)

###################################################################################################################################################################################################

@login_required
def Identity_UpdateCoordonates(request):
    
    individu = "Non renseigné"
    form = None

    try :
    
        query_social_number = request.GET.get('social_number')
        
        if query_social_number :
            query_social_number_list = Individu.objects.filter(NumeroIdentification__iexact=query_social_number)
            individu = query_social_number_list[:1].get()

        else :
            query_social_number_list = Individu.objects.none() # == []

        
        form = IndividuFormCoordonates(request.POST or None, instance = query_social_number_list.first())

        form.fields['Utilisateur'].initial = request.user.last_name + " " + request.user.first_name

        if form.is_valid():
            if 'save' in request.POST :
                for element in settings.BDD :
                    post = form.save(commit=False)
                    post.save(using=element)
                return HttpResponseRedirect(reverse('Home'))
    
    except Individu.DoesNotExist :
            individu = "L'individu n'existe pas"

    context = {
        "query_social_number" : query_social_number,
        "query_social_number_list" : query_social_number_list,
        "individu" : individu,
        "form": form
    }
    return render(request, "Identity_UpdateCoordonates.html", context)

###################################################################################################################################################################################################

@login_required
def Identity_UpdateContact(request):
    
    individu = "Non renseigné"
    form = None

    try :
    
        query_social_number = request.GET.get('social_number')
        
        if query_social_number :
            query_social_number_list = Individu.objects.filter(NumeroIdentification__iexact=query_social_number)
            individu = query_social_number_list[:1].get()
            
        else :
            query_social_number_list = Individu.objects.none() # == []

        form = IndividuFormContact(request.POST or None, instance = query_social_number_list.first())
        form.fields['Utilisateur'].initial = request.user.last_name + " " + request.user.first_name
            
        if form.is_valid():
            if 'save' in request.POST :
                for element in settings.BDD :
                    post = form.save(commit=False)
                    post.save(using=element)
                return HttpResponseRedirect(reverse('Home'))
    
    except Individu.DoesNotExist :
            individu = "L'individu n'existe pas"

    context = {
        "query_social_number" : query_social_number,
        "query_social_number_list" : query_social_number_list,
        "individu" : individu,
        "form": form
    }
    return render(request, "Identity_UpdateContact.html", context)

