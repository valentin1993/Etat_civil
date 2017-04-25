#-*- coding: utf-8 -*-

import os
from django.shortcuts import render, reverse, redirect

def Choice (request) :
    
    return render(request, 'choice.html')

def Accueil(request) :
        
    return render(request, 'Accueil.html')
