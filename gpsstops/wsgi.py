"""
WSGI config for gpsstops project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site
# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/var/www/vhosts/bennyapp.com/httpdocs/django-app/django-app-venv/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/vhosts/bennyapp.com/httpdocs/django-app/gpsstops')
sys.path.append('/var/www/vhosts/bennyapp.com/httpdocs/django-app/gpsstops/gpsstops/')



from site import addsitedir
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpsstops.settings")

# Activate your virtual env
#activate_env=os.path.expanduser("/var/www/vhosts/bennyapp.com/httpdocs/django-app/django-app-venv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()