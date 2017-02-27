#-*- coding: utf-8 -*-

import os
from django.shortcuts import render, reverse

#Test de fonction
def Accueil(request) :
        
    return render(request, 'Accueil.html')
