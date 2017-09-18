# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-14 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Individu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NumeroIdentification', models.CharField(max_length=30, null=True, unique=True, verbose_name=b'Numero Identification physique')),
                ('Civilite', models.CharField(choices=[(b'Monsieur', b'Monsieur'), (b'Mademoiselle', b'Mademoiselle'), (b'Madame', b'Madame'), (b'Docteur', b'Docteur'), ('Ma\xeetre', 'Ma\xeetre')], max_length=12, verbose_name=b'Civilit\xc3\xa9')),
                ('NomJeuneFille', models.CharField(blank=True, max_length=30, verbose_name=b'Nom de jeune fille')),
                ('Nom', models.CharField(max_length=30, verbose_name=b'Nom de famille')),
                ('Prenom', models.CharField(max_length=30, verbose_name=b'Pr\xc3\xa9nom(s)')),
                ('Sexe', models.CharField(choices=[(b'Masculin', b'Masculin'), ('F\xe9minin', 'F\xe9minin')], max_length=30, verbose_name=b'Sexe')),
                ('Statut', models.CharField(choices=[('C\xe9libataire', 'C\xe9libataire'), ('Mari\xe9(e)', 'Mari\xe9(e)'), ('Divorc\xe9(e)', 'Divorc\xe9(e)'), (b'Veuf/Veuve', b'Veuf/Veuve')], max_length=30, verbose_name=b'Statut civil')),
                ('DateNaissance', models.DateField(verbose_name=b'Date de naissance')),
                ('VilleNaissance', models.CharField(max_length=30, verbose_name=b'Ville de naissance')),
                ('PaysNaissance', django_countries.fields.CountryField(max_length=2, verbose_name=b'Pays de naissance')),
                ('Nationalite1', models.CharField(max_length=30, verbose_name=b'Nationalit\xc3\xa9 1')),
                ('Nationalite2', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Nationalit\xc3\xa9 2')),
                ('Profession', models.CharField(max_length=30, verbose_name=b'Profession')),
                ('Adresse', models.CharField(max_length=30, verbose_name=b'Adresse')),
                ('Ville', models.CharField(max_length=30, verbose_name=b'Ville')),
                ('Zip', models.IntegerField(verbose_name=b'Code Postal')),
                ('Pays', django_countries.fields.CountryField(max_length=2, verbose_name=b'Pays')),
                ('Mail', models.CharField(blank=True, max_length=30, verbose_name=b'Email')),
                ('Telephone', models.CharField(blank=True, max_length=20, verbose_name=b'T\xc3\xa9l\xc3\xa9phone')),
                ('Creation', models.DateTimeField(auto_now_add=True)),
                ('Utilisateur', models.CharField(default=b' ', max_length=100, verbose_name=b'Utilisateur')),
                ('Etat', models.CharField(choices=[(b'Vivant', b'Vivant'), ('D\xe9c\xe9d\xe9', 'D\xe9c\xe9d\xe9')], default=b' ', max_length=30, verbose_name=b'Etat')),
                ('Image', models.ImageField(blank=True, default=b' ', upload_to=b'pictures/', verbose_name=b'Photo Identit\xc3\xa9')),
                ('CarteIdentite', models.ImageField(blank=True, default=b' ', upload_to=b'Carte_Identite/', verbose_name=b'Carte Identit\xc3\xa9')),
            ],
        ),
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=30, verbose_name=b'Nom de Soci\xc3\xa9t\xc3\xa9')),
                ('Etat', models.CharField(choices=[('En activit\xe9', 'En activit\xe9'), ('Clos', 'Clos')], max_length=30, verbose_name=b'Etat')),
                ('Adresse', models.CharField(max_length=30, verbose_name=b'Adresse')),
                ('Ville', models.CharField(max_length=30, verbose_name=b'Ville')),
                ('Zip', models.IntegerField(verbose_name=b'Code Postal')),
                ('Region', models.CharField(max_length=30, verbose_name=b'R\xc3\xa9gion')),
                ('Pays', django_countries.fields.CountryField(max_length=2, verbose_name=b'Pays')),
                ('Mail', models.CharField(max_length=40, verbose_name=b'Email')),
                ('Web', models.CharField(max_length=40, verbose_name=b'Site Web')),
                ('Telephone', models.CharField(max_length=20, verbose_name=b'T\xc3\xa9l\xc3\xa9phone Fixe')),
                ('Fax', models.CharField(max_length=20, verbose_name=b'Fax')),
                ('SIREN', models.BigIntegerField(verbose_name=b'N\xc2\xb0 SIREN')),
                ('SIRET', models.BigIntegerField(verbose_name=b'N\xc2\xb0 SIRET')),
                ('NAF_APE', models.CharField(max_length=5, verbose_name=b'Code NAF-APE')),
                ('RCS', models.CharField(max_length=30, verbose_name=b'Code RCS')),
                ('CHOIX_TVA', models.CharField(choices=[(b'Oui', b'Oui'), ('Non', 'Non')], max_length=30, verbose_name=b'Assujeti \xc3\xa0 la TVA')),
                ('TVA', models.CharField(max_length=13, verbose_name=b'N\xc2\xb0 TVA Intracommunautaire')),
                ('Type', models.CharField(choices=[(b'Administration', b'Administration'), (b'Autre', b'Autre'), (b'Grand Compte', b'Grand Compte'), (b'Grossiste', b'Grossiste'), (b'PME/PMI', b'PME/PMI'), (b'Revendeur', b'Revendeur'), (b'Startup', b'Startup'), (b'TPE', b'TPE')], max_length=30, verbose_name=b'Type de Soci\xc3\xa9t\xc3\xa9')),
                ('Effectif', models.CharField(choices=[(b'1-5', b'1-5'), (b'6-10', b'6-10'), (b'11-50', b'11-50'), (b'51-100', b'51-100'), (b'101-500', b'101-500'), (b'> 500', b'> 500')], max_length=30, verbose_name=b'Effectif')),
                ('Capital', models.IntegerField(verbose_name=b'Capital de la Soci\xc3\xa9t\xc3\xa9 (euros)')),
                ('Creation', models.DateTimeField(auto_now_add=True)),
                ('InformationsInstitution', models.CharField(max_length=30, verbose_name=b'Informations Institution')),
                ('Utilisateur', models.CharField(default=b' ', max_length=100, verbose_name=b'Utilisateur')),
                ('Responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Responsable_Societe', to='Identity.Individu', to_field=b'NumeroIdentification', verbose_name=b'Responsable')),
            ],
        ),
    ]
