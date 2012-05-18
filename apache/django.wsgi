import os
import sys

path = 'Users/zouf/Sites/rateout-2'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'rateout.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
