import os
import sys

path = '/home/zouf/nightout'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nightout.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
