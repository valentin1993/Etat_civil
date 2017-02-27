#-*- coding: utf-8 -*-

import requests, os, json, glob
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from Recensement.models import Attestation_Recensement
from Mairie.models import Mairie 
from Identity.models import Identity

from Recensement.forms import Attestation_Recensement_Form
from Identity.forms import IdentityForm
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


@login_required
def Recensement_array(request) :

    today = datetime.now()
    age_16 = (today - relativedelta(years=16))

    mairie = get_object_or_404(Mairie)

    result = Identity.objects.filter(birthday__year = age_16.year, city__iexact=mairie.city)

    paginator = Paginator(result, 3)
    page = request.GET.get('page', 1)

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    context = {
    "Identity":Identity,
    "mairie":mairie,
    "age_16":age_16,
    "datetime" : datetime,
    "result" : result,
    "PageNotAnInteger":PageNotAnInteger,
    }


    return render(request, 'Recensement_resume.html', context)

@login_required
def Liste_Recensement_PDF(request) :

    today = datetime.now()
    age_16 = (today - relativedelta(years=16))

    mairie = get_object_or_404(Mairie)

    result = Identity.objects.filter(birthday__year = age_16.year, city__iexact=mairie.city)

    data = {"mairie" : mairie, "result":result, "today":today}

    template = get_template('Recensement_raw.html')
    html  = template.render(Context(data))

    filename_temp = 'Recensement_' + str(today.year) 
    filename = filename_temp + '.pdf'
    path = '/Users/valentinjungbluth/Desktop/Django/Individus/' + filename

    
    file = open(path, "w+b") 
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.close()

    url = 'https://demoged.datasystems.fr:8090/services/rest/document/list'
    payload = {'folderId': 8978476}

    headers = {'Accept': 'application/json'}
    r = requests.get(url,  params=payload, headers=headers, auth=('etatcivil', '100%EC67'))

    rbody = r.content
    data = json.loads(rbody)

    longueur = len(data)

    i=0
    list = []

    while i < longueur :
        
        if data[i]["title"] == filename_temp :
            
            list = [data[i]]
        i = i+1


    if len(list) == 0 :

        payload = '{{ "language":"fr","fileName":"{0}","folderId": "8978476" }}'.format(filename)  
        upfile = path
        files = { 
        'document': (None, payload, 'application/json'),
        'content': (os.path.basename(upfile), open(upfile, 'rb'), 'application/octet-stream')
        } 
        url = 'https://demoged.datasystems.fr:8090/services/rest/document/create'
        headers = {'Content-Type': 'multipart/form-data'}
        r = requests.post(url, files=files, headers=headers, auth=('etatcivil', '100%EC67'))

        for element in glob.glob(path) :
            os.remove(element)

        list[:] = []

    else :
        
    
        data = {"docId": 9011342, "filename":filename, "language": "fr"}
        upfile = path

        files = { 
        'filedata': (os.path.basename(upfile), open(upfile, 'rb'), 'application/octet-stream')
        } 
        url = 'https://demoged.datasystems.fr:8090/services/rest/document/upload'
        headers = {'Content-Type': 'multipart/form-data'}
        r = requests.post(url, files=files, data=data, headers=headers, auth=('etatcivil', '100%EC67'))

        for element in glob.glob(path) :
            os.remove(element)


    context = {
        "mairie":mairie,
        "result":result,
    }

    return render(request, 'Recensement.html', context) # Template page générée après PDF

@login_required
def Attestation_Recensement_Formulary(request) :

    if request.method == 'POST':
        
        form = Attestation_Recensement_Form(request.POST or None)

        if form.is_valid() :    
            if 'save' in request.POST :
                post = form.save()
                return HttpResponseRedirect(reverse('Rtreated', kwargs={'id': post.id}))

    else :
        form = Attestation_Recensement_Form()
        

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
    mairie = get_object_or_404(Mairie)

    data = {"ar" : ar, "mairie":mairie}

    template = get_template('Attestation_Recensement_raw.html')
    html  = template.render(Context(data))


    filename_directory = str(Attestation_Recensement.objects.get(pk=id).lastname.encode('utf-8')) + "_" + str(Attestation_Recensement.objects.get(pk=id).firstname.encode('utf-8')) + "_" + str(Attestation_Recensement.objects.get(pk=id).birthday)
    filename_init = 'Attestation_Recensement_' + filename_directory 
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
        Search_Docs = EnterSearch.find_parameters(SID, filename_init)
        print Search_Docs
        print "Recherche des occurences de documents"

        # for element in Search_Docs :
        #     if Search_Docs['hits'][0]['fileName'] == filename :
        #Search_Docs_ID = Search_Docs['hits'][0]['id']
        #print Search_Docs_ID

        # If folder exists but not document
        if Search_Docs[0]['title'] != filename_init :
            
            print "pas d'occurence"
            
            # Create document inside the good folder
            Create_Docs = Docs.create(path, SID, fileName = filename, folderId = Folder_research[0]['id'])
            print "nouveau document crée dans dossier existant"

        else :
            
            print "une occurence trouvée"
            
            Search_Docs_ID = Search_Docs[0]['id']

            # Update the document in the good folder
            Upload_Docs = Docs.upload(path, SID, Search_Docs_ID, filename)


    Logger.logout(SID)

    context = {"ar":ar,
               "path":path,
                   }
                   
    return render(request, 'Recensement_PDF.html', context)