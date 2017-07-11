class GED_url :
    
    url = "http://demoged.datasystems.fr:8080"

class Individu_path :
    
    path = '/Users/valentinjungbluth/Desktop/Django/Individus/'

class Individu_Image_path :
    
    path = '/Users/valentinjungbluth/Desktop/Django/DatasystemsCore/Media/pictures/'

class Individu_Image_path_RAW :
        
    path = '/Users/valentinjungbluth/Desktop/Django/DatasystemsCore/Media/pictures_RAW/'

class Individu_CarteIdentite_path :
    
    path = '/Users/valentinjungbluth/Desktop/Django/DatasystemsCore/Media/Carte_Identite/'

class Individu_CarteIdentite_path_RAW :
        
    path = '/Users/valentinjungbluth/Desktop/Django/DatasystemsCore/Media/Carte_Identite_RAW/'

class Societe_path :
    
    path = '/Users/valentinjungbluth/Desktop/Django/Societes/'

SECRET_KEY = 'r$7_)2pb&z9*+)ho98^gnxs9ee^$zi^13(r0$+kooth!x(_l=3'

ALLOWED_HOSTS = []

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DS_Core',
        'USER': 'osx',
        'PASSWORD': '100%django',
        'HOST': '172.30.10.115',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET innodb_strict_mode=1',
            'sql_mode': 'traditional',
        }
    },

    'DS_Douane': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DS_Douane',
        'USER': 'osx',
        'PASSWORD': '100%django',
        'HOST': '172.30.10.115',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET innodb_strict_mode=1',
            'sql_mode': 'traditional',
        }
    },

    'DS_Impots': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DS_Impots',
        'USER': 'osx',
        'PASSWORD': '100%django',
        'HOST': '172.30.10.115',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET innodb_strict_mode=1',
            'sql_mode': 'traditional',
        }
    },

    'DS_Finance': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DS_Finance',
        'USER': 'osx',
        'PASSWORD': '100%django',
        'HOST': '172.30.10.115',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET innodb_strict_mode=1',
            'sql_mode': 'traditional',
        }
    },
}