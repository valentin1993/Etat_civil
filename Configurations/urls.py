from django.conf.urls import url
from Configurations import views

urlpatterns = [
    url(r'^Theme/', views.ChoiceTheme, name="theme"),
    url(r'^Help/', views.Help, name="help"),
]
