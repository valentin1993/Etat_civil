#-*- coding: utf-8 -*-

import os
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from .forms import ThemeForm
from .models import Theme

def ChoiceTheme(request) :
    
    if request.method == 'POST':
        
        form = ThemeForm(request.POST or None)

        if form.is_valid():
            post = form.save()
    
            return HttpResponseRedirect(reverse('accueil'), {"form":form})

    else:
        form = ThemeForm()

    context = {
        "form":form,
    }
        
    return render(request, 'Theme.html', context)

def Help(request) :

    return render(request, 'Help.html')