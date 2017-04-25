from django.conf import settings
from Configurations.models import Theme
from fabric.api import run

def GetTheme(request):
    return {'mytheme' : Theme.objects.values_list('favorite_theme').last()[0].encode("ascii")}

from datetime import datetime

def get_infos(request):
    date_actuelle = datetime.now()
    return {'date_actuelle': date_actuelle}

def Test(request):
    number = "1."
    i=0
    # if run("sudo git push -u origin master") :
    #     i=i+1
    # else :
    #     i
    return {'test' : number + str(i)}

