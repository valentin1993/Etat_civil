from django.conf import settings
from Configurations.models import Theme

def GetTheme(request):
    return {'mytheme' : Theme.objects.values_list('favorite_theme').last()[0].encode("ascii")}

