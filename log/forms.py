#log/forms.py
from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.core.files.images import get_image_dimensions

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

