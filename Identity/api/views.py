from rest_framework.generics import (
	CreateAPIView,
	UpdateAPIView,
	DestroyAPIView,
	ListAPIView, 
	RetrieveAPIView,
	)

from Identity.models import Individu

from Identity import Individu_Recherche 

from .serializers import (
	IndividuSerializer, 
	IndividuDetailSerializer, 
	IndividuCreateSerializer,
	IndividuUpdateSerializer,
	#IndividuResearchSerializer,
	)

class IndividuListAPIView(ListAPIView) :
	queryset = Individu.objects.all()
	serializer_class = IndividuSerializer

class IndividuCreateAPIView(CreateAPIView) :
	queryset = Individu.objects.all()
	serializer_class = IndividuCreateSerializer

class IndividuDetailAPIView(RetrieveAPIView):
	queryset = Individu.objects.all()
	serializer_class = IndividuDetailSerializer

class IndividuUpdateAPIView(UpdateAPIView) :
	queryset = Individu.objects.all()
	serializer_class = IndividuUpdateSerializer

class IndividuDeleteAPIView(DestroyAPIView) :
	queryset = Individu.objects.all()
	serializer_class = IndividuSerializer

# class IndividuResearchAPIView(ListAPIView) :
# 	queryset = Individu_Recherche.Recherche_Filter()
# 	serializer_class = IndividuResearchSerializer