#-*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import force_text
from django_countries.fields import CountryField

##########################################
# Choix à l'utilisateur pour la civilité #
##########################################

TITLE_CHOICES = (
    ('Mr', 'Monsieur'),
    ('Mlle', 'Mademoiselle'),
    ('Mme','Madame'),
    ('Dr','Docteur'),
    ('Me','Maître'),
)

######################################
# Choix à l'utilisateur pour le sexe #
######################################

SEX_CHOICES = (
    ('Masculin', 'Masculin'),
    ('Feminin', 'Feminin')
)


####################################################################################
# Création d'une table permettant de renseigner toutes les informations concernant #
#                les parents et reprise de celles des enfants                      #
####################################################################################

class Attestation_Recensement(models.Model):

    social_number = models.CharField(max_length=30, null=True, verbose_name='numero social', unique=True)
    title = models.CharField(max_length=12,choices=TITLE_CHOICES, verbose_name='Civilité')
    lastname = models.CharField(max_length=30, verbose_name='Nom de famille')
    firstname = models.CharField(max_length=30, verbose_name='Prénom(s)')
    sex = models.CharField(max_length=8, choices=SEX_CHOICES, verbose_name='Sexe')
    birthday = models.DateField(verbose_name='Date de naissance')
    birthcity = models.CharField(max_length=30, verbose_name='Ville de naissance')
    birthcountry = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays de naissance')
    adress = models.CharField(max_length=30, verbose_name='Adresse', null=True)
    city = models.CharField(max_length=30, verbose_name='Ville')
    country = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays')
    mairie = models.CharField(max_length=30, null=False, verbose_name='Mairie', default=' ')
    created = models.DateTimeField(auto_now_add=True) 


    def save(self, *args, **kwargs):
        for field_name in ['lastname', 'birthcity', 'city']:
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

        super(Attestation_Recensement, self).save(*args, **kwargs)


    def __unicode__(self):
         return '%s %s %s %s %s %s %s %s %s %s %s %s' % (self.adress, self.social_number, self.id, self.title, self.lastname, self.firstname, self.sex, self.birthday, self.birthcity, self.birthcountry,
                                                                     self.city, self.country)