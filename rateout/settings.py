# Django settings for nightout project.
from S3 import CallingFormat
import os
import socket
DEBUG = True

TEMPLATE_DEBUG = DEBUG
BASE_DIR = os.path.abspath(os.path.dirname(__file__))+'/..'

#add your admin name here
ADMINS = (
     ('Matt Zoufaly', 'matt@allsortz.com'),
)

DEV_BOXES = ['hydralisk'] # add your dev computer here


#true if we're on the servers for deployment. In other words, any computer but
# the dev computers

if socket.gethostname() in DEV_BOXES:
    DEPLOY = False
else:
    DEPLOY = True



EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'errors@allsortz.com'
EMAIL_HOST_PASSWORD = 'sendserrors'
EMAIL_PORT = 587


MANAGERS = ADMINS

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
CELERY_IMPORTS = ("ratings.tasks", )
CELERY_RESULT_BACKEND = "amqp"


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID='AKIAJNT6HH4SMZYBZJKQ'
AWS_SECRET_ACCESS_KEY='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'
AWS_STORAGE_BUCKET_NAME='rateoutimages'
AWS_CALLING_FORMAT=CallingFormat.SUBDOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#import djcelery


#djcelery.setup_loader()


##old settings


if DEPLOY:
#use amazon RDS
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'nightout2',                      # Or path to database file if using sqlite3.
            'USER': 'zouf',                      # Not used with sqlite3.
            'PASSWORD': 'zoufzouf',                  # Not used with sqlite3.
            'HOST': 'rateoutdb-mysql.carvpvtur6or.us-east-1.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'nightout2',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'new-password',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }   
    }
    
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1



# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"


#dont use AWS for debug

STATIC_ROOT = BASE_DIR+'/static/'


LOG_FILE = STATIC_ROOT+'/log.txt'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"

if not DEPLOY:
    STATIC_URL='/static/'
else:
    STATIC_URL='http://rateoutimages.s3-website-us-east-1.amazonaws.com/'
    
DATASET_LOCATION = BASE_DIR+'/data_import/michigan_dataset.json'
RESULTS_DIR = '/tmp/'
CLIB_DIR = BASE_DIR+'/clib'

PYTHON_PATH = BASE_DIR+'/clib'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	  ("css", BASE_DIR+ "/css"),
	  ("js", BASE_DIR+ "/js"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v%m(kt379ic)zf+2p@6vn(ke6!@t=l$$%b)u5=3z0^q@psbh04'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rateout.urls'

# URL of the login page.
LOGIN_URL = '/accounts/login/'


#haystack search plugin
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}


# Python dotted path to the WSGI application used by Django's runserver.
#WSGI_APPLICATION = 'rateout.wsgi.application'

TEMPLATE_DIRS = (
	BASE_DIR+'/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
	'ratings',
    'data_import',
    'recommendation',
	'registration', 
	 'celery',
     'djcelery',
     'storages',
     'comments',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
	'django.contrib.contenttypes',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

ACCOUNT_ACTIVATION_DAYS = 7

#import logging
#logging.basicConfig(
#	level=logging.DEBUG,
#	format='%(asctime)s %(levelname)s %(message)s',
#	filename='/tmp/django.log',
#	filemode='w'
#)



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR+'/logs/mylog.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'allsortz_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR+'/logs/allsortz_ratings.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR+'/logs/django_request.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
         'send_email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'ratings':{
             'handlers': ['allsortz_handler', 'send_email'], #sends email on errors
            'level': 'DEBUG',
            'propagate': True      
            },
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
