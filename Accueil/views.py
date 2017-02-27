#-*- coding: utf-8 -*-

import os
from django.shortcuts import render, reverse

def Accueil(request) :
        
    return render(request, 'Accueil.html')
