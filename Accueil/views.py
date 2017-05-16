# Copyright (C) 2017     Valentin JUNGBLUTH  <valentin@datasystems.fr>
# Copyright (C) 2017     Alexis MOLTER       <amolter@datasystems.fr>

# This script lets to define views functions for "Accueil"

#-*- coding: utf-8 -*-

from django.shortcuts import render


def Choice(request):
    return render(request, 'Choice.html')


def Accueil(request):
    return render(request, 'Accueil.html')

def Test(request):
    return render(request, 'test.html')
