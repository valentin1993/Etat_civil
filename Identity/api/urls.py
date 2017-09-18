from django.conf.urls import url
from django.contrib import admin

from .views import (
	IndividuCreateAPIView,
	IndividuListAPIView, 
	IndividuDetailAPIView, 
	IndividuUpdateAPIView, 
	IndividuDeleteAPIView,
	#IndividuResearchAPIView,
	)

urlpatterns = [
	url(r'^$', IndividuListAPIView.as_view() , name="IndividuList"),
	url(r'^(?P<pk>\d+)/$', IndividuDetailAPIView.as_view() , name="Detail"),
	url(r'^create/$', IndividuCreateAPIView.as_view() , name="Create"),
	url(r'^(?P<pk>\d+)/edit/$', IndividuUpdateAPIView.as_view() , name="Update"),
	url(r'^(?P<pk>\d+)/delete/$', IndividuDeleteAPIView.as_view() , name="Delete"),
	#url(r'^search/$', IndividuResearchAPIView.as_view() , name="Search"),

]