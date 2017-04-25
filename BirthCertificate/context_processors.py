from django.conf import settings
from Configurations.models import Theme

#from django.core.cache import cache

def GetTheme(request):
    return {'mytheme' : Theme.objects.values_list('favorite_theme').last()[0].encode("ascii")}

# def cached_queries(request):
#     return {'VarLastname' : cache.get('VarLastname')}