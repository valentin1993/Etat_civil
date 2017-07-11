# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import force_text
from django_countries.fields import CountryField
from Identity.models import Individu

###############################################
# Choix à l'utilisateur pour le sexe du maire #
###############################################


CHOIX_INSTITUTIONS = (
    ('Mairie','Mairie'),
    (u'Préfecture','Préfecture'),
    ('Douane','Douane'),
    (u'Impôts',u'Impôts'),
    ('Autre','Autre')
)


####################################################################################
#           Création d'une table permettant de renseigner toutes les               #
#                 informations concernant la mairie et le maire                    #
####################################################################################

class InformationsInstitution(models.Model):

    Institution = models.CharField(max_length=30, choices=CHOIX_INSTITUTIONS, null=False, verbose_name="Type d'institution")
    Adresse = models.CharField(max_length=30, null=False, verbose_name='Adresse')
    Zip = models.IntegerField(verbose_name='Code Postal', null=False)
    Ville = models.CharField(max_length=30, verbose_name='Ville', null=False)
    Pays = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays', null=False)
    Region = models.CharField(max_length=30, verbose_name='Région')
    TelephoneFixe = models.CharField(max_length=30, verbose_name='Téléphone Fixe', null=False)
    Fax = models.CharField(max_length=30, verbose_name='Fax', blank=True, null=True)
    Email = models.CharField(max_length=40, verbose_name='Email', blank=True, null=True)

    def save(self, *args, **kwargs):
        for field_name in ['Ville' ,'Region', 'Pays']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())

        super(InformationsInstitution, self).save(*args, **kwargs)