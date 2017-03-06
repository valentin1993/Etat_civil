#-*- coding: utf-8 -*-

import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import Identity
from .forms import IdentityForm
from django.views.generic.edit import UpdateView
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa

import Logger, Search, Folds, Docs, Buffer, EnterSearch



@login_required
def Identity_Home(request) :

    return render(request, 'Identity_home.html')

@login_required
def Identity_Form(request) :

    form = IdentityForm(request.POST or None)
    template_name = 'form_Identity.html'

    if form.is_valid() :    
        # if '_preview' in request.POST :
        #     post = form.save(commit=False)
        #     template_name = 'preview.html'

        if '_save' in request.POST :
            post = form.save()
            return HttpResponseRedirect(reverse('treated', kwargs={'id': post.id}))

    return render(request, template_name, {"form" : form})

@login_required
def Identity_Resume(request, id) :
    
    identity = get_object_or_404(Identity, pk=id)
    return render(request, 'identity_resume.html', {"identity" : identity})

@login_required
def Identity_Researching(request) :
    
    folderId = None
    
    #######################
    # Display some arrays #
    #######################

    identitys = Identity.objects.order_by("-id")
    identity = identitys[:3] #The 3 last created forms
    identity_France = identitys.filter(country=64)[:3] #The 3 last created form with BirthCity = France

    ############################
    # People searching process #
    ############################

    query_lastname = request.GET.get('q1')
    query_firstname = request.GET.get('q1bis')
    query_birthday = request.GET.get('q1ter')

    if query_lastname and query_firstname and query_birthday :
        
        query_lastname_list = Identity.objects.filter(lastname__contains=query_lastname, firstname__contains=query_firstname, birthday__contains=query_birthday) 

        title = str(query_lastname + "_" + query_firstname + "_" + query_birthday)

        ##########################################
        # Look if people directory already exist #
        ##########################################

        url = 'https://demoged.datasystems.fr:8090/services/rest/folder/listChildren?folderId=8552450'
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
        query_lastname_list = Identity.objects.none() # == []


    context = {
        "identity" : identity,
        "identity_France" : identity_France,
        "query_lastname" : query_lastname,
        "query_firstname" : query_firstname,
        "query_birthday" : query_birthday,
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
        query_lastname_list = Identity.objects.filter(lastname__icontains=query_lastname, firstname__icontains=query_firstname, birthday__iexact=query_birthday)    
    else :
        query_lastname_list = Identity.objects.none() # == []


    form = IdentityForm(request.POST or None, instance = query_lastname_list.first())

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
        query_lastname_list = Identity.objects.filter(lastname__icontains=query_lastname, firstname__icontains=query_firstname, birthday__iexact=query_birthday)    
    else :
        query_lastname_list = Identity.objects.none() # == []

    form = IdentityForm(request.POST or None, instance = query_lastname_list.first())
    
    if "Supprimer" in request.POST :
        form = Identity.objects.filter(pk=query_lastname_list).delete()
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

    identity = get_object_or_404(Identity, pk=id)

    data = {"identity" : identity}

    template = get_template('Identity_raw.html') # A modifier : template pdf généré
    html  = template.render(Context(data))


    filename_directory = str(Identity.objects.get(pk=id).lastname.encode('utf-8')) + "_" + str(Identity.objects.get(pk=id).firstname.encode('utf-8')) + "_" + str(Identity.objects.get(pk=id).birthday)
    filename_init = 'Fiche_Individuelle_' + filename_directory 
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

        print "dossier créé"

        # Create document inside the new folder
        Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Create_Folds['id'] )
        print "document ajouté dans dossier créé"

    #################
    # Folder exists #
    #################

    # If folder already exist
    else :
        
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


    #Logger.logout(SID)

    context = {"identity":identity,
               "path":path,
               "folderId":folderId,
    }
                   

    return render(request, 'Identity_PDF.html', context) # Template page générée après PDF