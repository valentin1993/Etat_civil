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
    
    
    today = datetime.datetime.now()
    query_naissance_list = BirthCertificate.objects.filter(created__icontains=today.year).order_by('lastname')
    mairie = get_object_or_404(Mairie, pk=Mairie.objects.last().id)

    data = {"mairie" : mairie, "query_naissance_list":query_naissance_list, "today":today}

    template = get_template('Table_raw.html')
    html  = template.render(Context(data))

    filename_temp = 'Table_annuelle_Naissance_' + str(today.year) 
    filename = filename_temp + '.pdf'
    path = '/Users/valentinjungbluth/Desktop/Django/Individus/' + filename

    
    file = open(path, "w+b") 
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.close()

    url = 'https://demoged.datasystems.fr:8090/services/rest/document/list'
    payload = {'folderId': 8978466}

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

        payload = '{{ "language":"fr","fileName":"{0}","folderId": "8978466" }}'.format(filename)  
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
    
        data = {"docId": 9011288, "filename":filename, "language": "fr"}
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
        "query_naissance_list":query_naissance_list,
    }

    return render(request, 'Table.html', context) # Template page générée après PDF