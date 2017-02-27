# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import force_text
from django_countries.fields import CountryField

###############################################
# Choix à l'utilisateur pour le sexe du maire #
###############################################

SEX_CHOICES = (
    ('Masculin', 'Masculin'),
    ('Feminin', 'Féminin')
)

TITLE_CHOICES = (
    ('Mr', 'Monsieur'),
    ('Mlle', 'Mademoiselle'),
    ('Mme','Madame'),
    ('Dr','Docteur'),
    ('Me','Maître'),
)

INSTITUTION_CHOICES = (
    ('Mairie','Mairie'),
    ('Prefecture','Préfécture'),
    ('Autre','Autre')
)

DEVISE_CHOICES = (
    ('EUR','EUR (€)'),
    ('USD','USD ($)'),
    ('CFA','CFA')
)

MANDAT_CHOICES = (
    ('2011','2011'),
    ('2012','2012'),
    ('2013','2013'),
    ('2014','2014'),
    ('2015','2015'),
    ('2016','2016'),
    ('2017','2017'),
    ('2018','2018'),
    ('2019','2019'),
    ('2020','2020'),
    ('2021','2021'),
    ('2022','2022'),
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025'),
    ('2026','2026'),
    ('2027','2027'),
    ('2028','2028'),
    ('2029','2029'),
    ('2030','2030'),
    ('2031','2031')
)

####################################################################################
#           Création d'une table permettant de renseigner toutes les               #
#                 informations concernant la mairie et le maire                    #
####################################################################################

class Mairie(models.Model):

    institution = models.CharField(max_length=30, choices=INSTITUTION_CHOICES, null=False, verbose_name='Nom/Enseigne/Raison Sociale')
    adress = models.CharField(max_length=30, null=False, verbose_name='Adresse')
    zip = models.IntegerField(verbose_name='Code Postal', null=False)
    city = models.CharField(max_length=30, verbose_name='Ville', null=False)
    country = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays', null=False)
    department = models.CharField(max_length=30, verbose_name='Département/Canton')
    devise = models.CharField(max_length=30, choices=DEVISE_CHOICES, null=False, verbose_name='Devise')
    fixe = models.CharField(max_length=30, verbose_name='Téléphone Fixe', null=False)
    fax = models.CharField(max_length=30, verbose_name='Fax', blank=True)
    mail = models.CharField(max_length=40, verbose_name = 'Mail', null=False)
    web = models.CharField(max_length=40, verbose_name = 'Site Web')
    title = models.CharField(max_length=12,choices=TITLE_CHOICES, verbose_name='Civilité du maire', null=False)
    lastname = models.CharField(max_length=30, verbose_name='Nom de famille du maire', null=False)
    firstname = models.CharField(max_length=30, verbose_name='Prénom(s) du maire', null=False)
    sex = models.CharField(max_length=8, choices=SEX_CHOICES, verbose_name='Sexe du maire', null=False)
    debut = models.CharField(max_length=8, choices=MANDAT_CHOICES, verbose_name='Début du mandat', null=False)
    fin = models.CharField(max_length=8, choices=MANDAT_CHOICES, verbose_name='Fin du mandat', null=False)