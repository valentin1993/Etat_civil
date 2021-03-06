#-*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from .forms import ConnexionForm
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from log.models import LoggedUsers



def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return HttpResponseRedirect(reverse('accueil'))
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion.html', locals())

def deconnexion(request):
    
    logout(request)

    return redirect(reverse('choice'))


def ConnectedUsers(request) :

    logged_users=LoggedUsers.objects.all()

    logged_users_number = LoggedUsers.objects.all().count()

    context = {
        "logged_users":logged_users,
        "logged_users_number":logged_users_number,
    }

    return render(request, "UtilisateursConnectes.html", context)
