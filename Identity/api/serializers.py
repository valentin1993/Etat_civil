from rest_framework import serializers 

from Identity.models import Individu
from Identity.views import Identity_Individu_Resume


class IndividuSerializer(serializers.ModelSerializer) :
	class Meta :
		model = Individu
		fields = [
			'id',
			'NumeroIdentification',
			'Nom',
			'Prenom',
		]

class IndividuDetailSerializer(serializers.ModelSerializer) :
	class Meta :
		model = Individu
		fields = [
			'id',
			'NumeroIdentification',
			'Civilite',
			'Nom',
			'Prenom',
			'Sexe',
			'Statut',
			'DateNaissance',
			'VilleNaissance',
			'PaysNaissance',
			'Nationalite1',
			'Nationalite2',
			'Profession',
			'Adresse',
			'Ville',
			'Zip',
			'Pays',
			'Mail',
			'Telephone',
			'Creation',
			'InformationsInstitution',
			'Utilisateur',
			'Etat',
			'Image',
			'CarteIdentite',
		]


class IndividuCreateSerializer(serializers.ModelSerializer) :
	class Meta :
		model = Individu
		fields = [
			#'id',
			#'NumeroIdentification',
			'Etat',
			'Civilite',
			'Nom',
			'Prenom',
			'Sexe',
			'Statut',
			'DateNaissance',
			'VilleNaissance',
			'PaysNaissance',
			'Nationalite1',
			'Nationalite2',
			'Profession',
			'Adresse',
			'Ville',
			'Zip',
			'Pays',
			'Mail',
			'Telephone',
			'Image',
			'CarteIdentite',
			]

	def create(self, validated_data):
	    obj = Individu.objects.create(**validated_data)
	    Identity_Individu_Resume(self.context.get('request'), obj.id)
	    return obj


class IndividuUpdateSerializer(serializers.ModelSerializer) :
	class Meta :
		model = Individu
		fields = [
			'Adresse',
			'Ville',
			'Zip',
			'Pays',
			'Mail',
			'Telephone',
		]

# class IndividuResearchSerializer(serializers.ModelSerializer) :
# 	class Meta :
# 		model = Individu
# 		fields = [
# 			'id',
# 			'NumeroIdentification',
# 			'Nom',
# 			'Prenom',
# 			'VilleNaissance',
# 		]


	

