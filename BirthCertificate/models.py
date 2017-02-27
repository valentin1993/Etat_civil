#-*- coding: utf-8 -*-

from django.db import models
from Identity.models import Identity
from django.utils.encoding import force_text
from django_countries.fields import CountryField

######################################
# Choix à l'utilisateur pour le sexe #
######################################

SEX_CHOICES = (
    ('Masculin', 'Masculin'),
    ('Feminin', 'Feminin')
)
    
####################################################################################
# Création d'une table permettant de renseigner toutes les informations concernant #
#               l'enfant et reprise des champs pour les parents                    #
####################################################################################

class BirthCertificate(models.Model):

    lastname = models.CharField(max_length=30, null=False, verbose_name='Nom de famille')
    firstname = models.CharField(max_length=30, null=False, verbose_name='Prénom(s)')
    sex = models.CharField(max_length=8, choices=SEX_CHOICES, verbose_name='Sexe')
    birthday = models.DateField(null=False, verbose_name='Date de naissance')
    birthhour = models.TimeField(null=True, verbose_name='Heure de naissance')
    birthcity = models.CharField(max_length=30, null=False, verbose_name='Ville de naissance')
    birthcountry = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays de naissance')
    fk_parent1 = models.ForeignKey(Identity, related_name='ID_Parent1', verbose_name='ID parent1', null=False)
    fk_parent2 = models.ForeignKey(Identity, related_name='ID_Parent2', verbose_name='ID parent2', null=False)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
            for field_name in ['lastname', 'birthcity']:
                val = getattr(self, field_name, False)
                if val:
                    setattr(self, field_name, val.upper())

            for field_name in ['firstname']:
                val = getattr(self, field_name, False)
            if val:
                new_val = []
                words = val.split()
                for x in words:
                    x = x.capitalize()
                    new_val.append(x)
                val = " ".join(new_val)
                setattr(self, field_name, val.capitalize())

            super(BirthCertificate, self).save(*args, **kwargs)
            