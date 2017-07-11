#coding:utf-8

from django.db import models
from django.utils.encoding import force_text
from django_countries.fields import CountryField
from Identity.models import *


######################################
# Choix à l'utilisateur pour le sexe #
######################################

CHOIX_SEXE = (
    ('Masculin', 'Masculin'),
    (u'Féminin', u'Féminin')
)

CHOIX_TITRE = (
    ('Monsieur', 'Monsieur'),
    ('Mademoiselle', 'Mademoiselle'),
    ('Madame','Madame'),
    ('Docteur','Docteur'),
    (u'Maître',u'Maître'),
)

CHOIX_STATUT = (
    (u'Célibataire', u'Célibataire'),
    (u'Marié(e)', u'Marié(e)'),
    (u'Divorcé(e)', u'Divorcé(e)'),
    ('Veuf/Veuve', 'Veuf/Veuve'),
)

CHOIX_ETAT = (
    ('Vivant', 'Vivant'), 
    (u'Décédé', u'Décédé')
)

CHOIX_ETAT_SOCIETE = (
    (u'En activité', u'En activité'),
    (u'Clos', u'Clos')
)

CHOIX_TVA = (
    ('Oui', 'Oui'),
    (u'Non', u'Non')
)

CHOIX_SOCIETE = (
    ('Administration', 'Administration'),
    ('Autre', 'Autre'),
    ('Grand Compte','Grand Compte'),
    ('Grossiste', 'Grossiste'),
    ('PME/PMI', 'PME/PMI'),
    ('Revendeur','Revendeur'),
    ('Startup','Startup'),
    ('TPE','TPE')
)

CHOIX_EFFECTIF = (
    ('1-5', '1-5'),
    ('6-10', '6-10'),
    ('11-50','11-50'),
    ('51-100', '51-100'),
    ('101-500', '101-500'),
    ('> 500','> 500')
)


########################################################
# Création d'une table permettant de renseigner toutes #
# les informations concernant les personnes physiques  #                  
########################################################

def upload_location(instance, filename) :
    return "%s/%s" %(Individu.id, filename)

class Individu(models.Model):

    NumeroIdentification = models.CharField(max_length=30, null=True, verbose_name='Numéro Identification physique', unique=True)
    Civilite = models.CharField(max_length=12,choices=CHOIX_TITRE, verbose_name='Civilité')
    NomJeuneFille = models.CharField(max_length=30, verbose_name='Nom de jeune fille', blank=True)
    Nom = models.CharField(max_length=30, verbose_name='Nom de famille')
    Prenom = models.CharField(max_length=30, verbose_name='Prénom(s)')
    Sexe = models.CharField(max_length=30, choices=CHOIX_SEXE, verbose_name='Sexe')
    Statut = models.CharField(max_length=30, choices=CHOIX_STATUT, verbose_name="Statut civil")
    DateNaissance = models.DateField(verbose_name='Date de naissance')
    VilleNaissance = models.CharField(max_length=30, verbose_name='Ville de naissance')
    PaysNaissance = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays de naissance')
    Nationalite1 = models.CharField(max_length=30, verbose_name='Nationalité 1')
    Nationalite2 = models.CharField(max_length=30, verbose_name='Nationalité 2', null=True, blank=True)
    Profession = models.CharField(max_length=30, verbose_name='Profession')
    Adresse = models.CharField(max_length=30, verbose_name='Adresse')
    Ville = models.CharField(max_length=30, verbose_name='Ville')
    Zip = models.IntegerField(verbose_name='Code Postal')
    Pays = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays')
    Mail = models.CharField(max_length=30, verbose_name='Email', blank=True)
    Telephone = models.CharField(max_length=20, verbose_name='Téléphone', blank=True)
    Creation = models.DateTimeField(auto_now_add=True)
    InformationsInstitution = models.CharField(max_length=30, null=False, verbose_name='Informations Institution')
    Utilisateur = models.CharField(max_length=100, null=False, verbose_name="Utilisateur", default=" ")
    Etat = models.CharField(max_length=30, choices=CHOIX_ETAT, default=" ", null=False, verbose_name="Etat")
    Image = models.ImageField(upload_to='pictures/', null=True, blank=True, width_field=None, height_field=None, verbose_name="Photo Identité")
    CarteIdentite = models.ImageField(upload_to='Carte_Identite/', null=True, blank=True, width_field=None, height_field=None, verbose_name="Carte Identité")

    def save(self, *args, **kwargs):
        for field_name in ['NomJeuneFille' ,'Nom', 'VilleNaissance', 'Nationalite1', 'Nationalite2', 'Ville', 'Profession']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())

        for field_name in ['Prenom']:
            val = getattr(self, field_name, False)
            if val:
                new_val = []
                words = val.split()
                for x in words:
                    x = x.capitalize()
                    new_val.append(x)
                val = " ".join(new_val)
                setattr(self, field_name, val.capitalize())

        super(Individu, self).save(*args, **kwargs)
            

    def __unicode__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.NumeroIdentification, self.Civilite, self.NomJeuneFille ,self.Nom, self.Statut, self.Prenom, 
                                                                            self.Sexe, self.DateNaissance, self.VilleNaissance, self.PaysNaissance, self.Nationalite1, self.Nationalite2, 
                                                                            self.Profession, self.Adresse, self.Ville, self.Zip, self.Pays, self.Mail, self.Telephone, self.Etat, 
                                                                            self.InformationsInstitution, self.Image, self.Utilisateur, self.CarteIdentite)


class Societe(models.Model):


    Nom = models.CharField(null= False, max_length=30, verbose_name='Nom de Société')
    Etat = models.CharField(max_length = 30, choices = CHOIX_ETAT_SOCIETE, null=False, verbose_name="Etat")
    Adresse = models.CharField(max_length=30, verbose_name='Adresse')
    Ville = models.CharField(max_length=30, verbose_name='Ville')
    Zip = models.IntegerField(verbose_name='Code Postal')
    Region = models.CharField(max_length=30, verbose_name='Région')
    Pays = CountryField(blank_label='Sélectionner un pays', verbose_name='Pays')
    Mail = models.CharField(max_length=40, verbose_name='Email')
    Web = models.CharField(max_length=40, verbose_name='Site Web')
    Telephone = models.CharField(max_length=20, verbose_name='Téléphone Fixe')
    Fax = models.CharField(max_length=20, verbose_name='Fax')
    SIREN = models.BigIntegerField(verbose_name='N° SIREN')
    SIRET = models.BigIntegerField(verbose_name='N° SIRET')
    NAF_APE = models.CharField(max_length=5, verbose_name='Code NAF-APE')
    RCS = models.CharField(max_length = 30, verbose_name='Code RCS')
    CHOIX_TVA = models.CharField(max_length = 30, choices=CHOIX_TVA, verbose_name='Assujeti à la TVA')
    TVA = models.CharField(max_length=13, verbose_name='N° TVA Intracommunautaire')
    Type = models.CharField(max_length = 30, choices = CHOIX_SOCIETE, verbose_name = 'Type de Société')
    Effectif = models.CharField(max_length = 30, choices = CHOIX_EFFECTIF, verbose_name = 'Effectif')
    Capital = models.IntegerField(verbose_name = 'Capital de la Société (euros)')
    Responsable = models.ForeignKey(Individu, related_name='Responsable_Societe', verbose_name='Responsable', null=False, to_field='NumeroIdentification')
    Creation = models.DateTimeField(auto_now_add=True)
    InformationsInstitution = models.CharField(max_length=30, null=False, verbose_name='Informations Institution')
    Utilisateur = models.CharField(max_length=100, null=False, verbose_name="Utilisateur", default=" ")

    def save(self, *args, **kwargs):
        for field_name in ['Nom', 'Ville', 'Region']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())

        super(Societe, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode (self.id, self.Nom, self.Etat, self.Adresse, self.Ville, self.Zip, self.Region, 
                                                                            self.Pays, self.Mail, self.Web, self.Telephone, self.Fax, self.SIREN, self.SIRET, 
                                                                            self.NAF_APE, self.RCS, self.CHOIX_TVA, self.TVA, self.Type, self.Effectif, self.Capital, 
                                                                            self.Creation, self.InformationsInstitution, self.Utilisateur, self.Responsable)
