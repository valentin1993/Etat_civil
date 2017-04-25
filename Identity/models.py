#coding:utf-8

from django.db import models
from django.utils.encoding import force_text
from django_countries.fields import CountryField


######################################
# Choix à l'utilisateur pour le sexe #
######################################

SEX_CHOICES = (
    ('Masculin', 'Masculin'),
    (u'Féminin', u'Féminin')
)
##########################################
# Choix à l'utilisateur pour la civilité #
##########################################

TITLE_CHOICES = (
    ('Mr', 'Monsieur'),
    ('Mlle', 'Mademoiselle'),
    ('Mme','Madame'),
    ('Dr','Docteur'),
    ('Me',u'Maître'),
)

STATUS_CHOICES = (
    (u'Célibataire', u'Célibataire'),
    (u'Marié(e)', u'Marié(e)'),
    (u'Divorcé(e)', u'Divorcé(e)'),
    ('Veuf/Veuve', 'Veuf/Veuve'),
)


####################################################################################
# Création d'une table permettant de renseigner toutes les informations concernant #
#                les parents et reprise de celles des enfants                      #
####################################################################################

class Person(models.Model):

    social_number = models.CharField(max_length=30, null=True, verbose_name='numero social', unique=True)
    title = models.CharField(max_length=12,choices=TITLE_CHOICES, verbose_name='Civilité')
    young_girl_lastname = models.CharField(max_length=30, verbose_name='Nom de jeune fille', blank=True)
    lastname = models.CharField(max_length=30, verbose_name='Nom de famille')
    firstname = models.CharField(max_length=30, verbose_name='Prénom(s)')
    sex = models.CharField(max_length=30, choices=SEX_CHOICES, verbose_name='Sexe')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name="Statut civil")
    birthday = models.DateField(verbose_name='Date de naissance')
    birthcity = models.CharField(max_length=30, verbose_name='Ville de naissance')
    birthcountry = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays de naissance')
    birthmairie = models.CharField(max_length=30, verbose_name='Mairie de naissance')
    nationality = models.CharField(max_length=30, verbose_name='Nationalité')
    job = models.CharField(max_length=30, verbose_name='Profession')
    adress = models.CharField(max_length=30, verbose_name='Adresse')
    city = models.CharField(max_length=30, verbose_name='Ville')
    zip = models.IntegerField(verbose_name='Code Postal')
    country = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays')
    mail = models.CharField(max_length=30, verbose_name='Email', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Téléphone', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    mairie = models.CharField(max_length=30, null=False, verbose_name='Mairie', default=' ')


    def save(self, *args, **kwargs):
        for field_name in ['young_girl_lastname' ,'lastname', 'birthcity', 'nationality', 'city', 'birthmairie']:
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

        super(Person, self).save(*args, **kwargs)
            

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.title, self.young_girl_lastname ,self.lastname, self.status, self.firstname, self.sex, self.birthday, self.birthcity, self.birthcountry,
                                                                             self.birthmairie, self.nationality, self.job, self.adress, self.city, self.zip, self.country, self.mail, self.phone)

