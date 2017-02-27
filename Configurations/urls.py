from django.conf.urls import url
from Configurations import views

urlpatterns = [
    url(r'^options/', views.ChoiceTheme, name="options"),
]
