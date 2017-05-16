from datetime import datetime
from Configurations.models import Theme


def GetTheme(request):
    return {'mytheme' : Theme.objects.values_list('favorite_theme').last()[0].encode("ascii")}


def get_infos(request):
    date_actuelle = datetime.now()
    return {'date_actuelle': date_actuelle}

def Test(request):
    number = "1."
    i=0
    return {'test' : number + str(i)}

def GED_url (request) :
    return {'GED_url' : "http://demoged.datasystems.fr:8080"}
